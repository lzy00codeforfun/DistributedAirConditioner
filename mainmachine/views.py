from django.shortcuts import render
from django.http import HttpResponse
from .models import Request,RoomStatusDao
import threading
import time
#from ..log.models import Log
MainStatus = {"open":1,"init_param":2,"run":3,"close":4}
RoomStatus = {"unregister":1,"registed":2,"waiting":"3","serving":4,"done":5}
RoomIdListSetting = ("309c","310c","311c","312c","fc")

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json
class RoomStatusLazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, RoomStatusDao):
            return str(obj)
        return super().default(obj)

def getFieldJson(jsons):
    """
        transform the origin database model serial json-str to
        the json data needed by the front-end
    :param jsons: the serial json-str from the origin
    :return: json-form data
    """
    jsons = json.loads(jsons)
    res = []
    for js in jsons:
        tmp = js["fields"]
        tmp.pop("time")
        status_zh = {1:"未入住",2:"关机",3:"等待中",4:"服务中",5:"待机"}
        status_zh_str = {"1": "未入住", "2": "关机", "3": "等待中", "4": "服务中", "5": "待机"}
        if type(tmp["status"]) == int:
            tmp["status"] = status_zh[tmp["status"]]
        elif type(tmp["status"]) == str:
            tmp["status"] = status_zh_str[tmp["status"]]
        res.append(tmp)
    dict = {}
    dict["message"] = "OK"
    dict["result"] = res
    print("dict {}".format(dict))
    ret = json.dumps(dict)

    return ret



class MainMachine:
    def __init__(self):
        self.status=MainStatus["open"]
        self.high_speed_fee = None
        self.low_speed_fee = None
        self.middle_speed_fee = None
        self.lowest_temper = None
        self.highest_temper = None
        self.default_temper = None
        self.default_speed = None
        self.default_mode = None
        self.cur_run = 0
        self.simulator = None


    def ServingRoom(self):      # 更新当秒的温度,控制到达温度的空调进入等待

        RunningRoom = RoomStatusDao.objects.filter(status=4)
        count = 0
        for room in RunningRoom:
            # 此段修改日志可以不使用，可以在request的时候直接创建log
            # if room.is_log == True:
            #     Log()
            #     room.is_log = False
            if room.target_temper > room.current_temper:
                room.status = RoomStatus["done"]
                room.service_time += time.time()-room.time
                room.time = time.time()
                room.fee_rate = 0
                #Log()           # 停止服务的log
                #StartTemperMonitor()
                room.save()
                continue
            room.current_temper -= 0.005 #dropTemper()
            room.save()
            count = count + 1
        if count != 3:
            WaitingRoom = RoomStatusDao.objects.filter(status=3)
            if len(WaitingRoom) != 0:
                WaitingRoom[0].status = 4
                WaitingRoom[0].current_temper -= 0.005#dropTemper()
                WaitingRoom[0].time=time.time()
                #Log()
                WaitingRoom[0].save()
        return

    def ScheduleWaitingRoom(self):
        global RoomStatus
        WaitingRoom = RoomStatusDao.objects.filter(status=3).order_by("speed")
        cnt_wait = len(WaitingRoom)
        if cnt_wait != 0:
            RunningRoom = RoomStatusDao.objects.filter(status=4).order_by("-speed").order_by("time")
            count = len(RunningRoom)
            if count <3:
                WaitingRoom[0].status = RoomStatus["serving"]
                WaitingRoom[0].time = time.time()
                WaitingRoom[0].current_temper -= 0.005
                WaitingRoom[0].save()
                #Log()
            elif int(RunningRoom[0].speed)< int(WaitingRoom[0].speed) or ( int(RunningRoom[0].speed)== int(WaitingRoom[0].speed) and (time.time()-float(WaitingRoom[0].time))>120  ):
                RunningRoom[0].status = RoomStatus["waiting"]
                RunningRoom[0].service_time += time.time()-RunningRoom[0].time
                RunningRoom[0].time = time.time()
                RunningRoom[0].save()
                #Log()
                WaitingRoom[0].status = RoomStatus["serving"]
                WaitingRoom[0].time = time.time()
                WaitingRoom[0].current_temper -= 0.005
                WaitingRoom[0].save()
                #Log()
        return

    def get_default(self):
        return {"highest_temper": self.highest_temper, "lowest_temper": self.lowest_temper,
                "high_speed_fee": self.high_speed_fee, "low_speed_fee": self.low_speed_fee,
                "default_temper": self.default_temper, "default_speed":self.default_speed,
                "mode":self.default_mode,"middle_speed_fee":self.middle_speed_fee}




    def run(self):
        global MainStatus
        while self.status != MainStatus["close"]:
            # 每秒更新 当前服务队列的房间温度，（更新房间温度，如果房间温度到达目标温度，则从调度队列中换出） 从数据库中筛选出正在服务的房间（running）
            self.ServingRoom()

            #在这个模拟调度的过程中，就不需要去获取请求。只需要观察等待队列即可。


            self.ScheduleWaitingRoom()

            # test
            # print(" 1 ")
            time.sleep(2)


    def init_param(self,u_tem,l_tem,low_speed_fee, middle_speed_fee,high_speed_fee, d_tem, d_spd, mode):
        global MainStatus
        if self.status < MainStatus["open"]:
            return HttpResponse("error no open")
        self.low_speed_fee = low_speed_fee
        self.middle_speed_fee = middle_speed_fee
        self.high_speed_fee = high_speed_fee
        self.lowest_temper = l_tem
        self.highest_temper = u_tem
        self.default_temper = d_tem
        self.default_speed = d_spd
        self.default_mode = mode
        self.status = MainStatus["init_param"]
        return

    def Close(self):
        global MainStatus
        self.status = MainStatus["close"]
        RoomStatusDao.objects.all().delete()
        return


MainM = None


# 开机
def openMainMachine(request):
    global MainM
    global MainStatus
    global RoomIdListSetting
    print("MainMachine open")
    MainM = MainMachine()
    MainM.status= MainStatus["open"]
    RoomStatusDao.objects.all().delete()
    for rid in RoomIdListSetting:
        rl = RoomStatusDao.create(room_id=rid)
        rl.save()
    dict = {}
    dict["message"]="OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret,content_type="application/json")

# 初始化参数
# InitParam?highest_temper=30&lowest_temper=16&highest_speed=3&lowest_speed=1&default_temper=24&default_speed=2&default_mode=1
def init_param(request):
    print("init_param")
    global MainM
    u_tem=request.GET.get("highest_temper")
    l_tem = request.GET.get("lowest_temper")
    middle_speed_fee = request.GET.get("middle_speed_fee")
    low_speed_fee = request.GET.get("low_speed_fee")
    high_speed_fee = request.GET.get("high_speed_fee")
    d_tem = request.GET.get("default_temper")
    d_spd = request.GET.get("default_speed")
    mode = request.GET.get("mode")
    print(u_tem,l_tem,low_speed_fee, middle_speed_fee,high_speed_fee, d_tem, d_spd, mode)
    MainM.init_param(u_tem,l_tem,low_speed_fee, middle_speed_fee,high_speed_fee, d_tem, d_spd, mode)
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")

def get_default_url(request):
    global MainM
    ret = MainM.get_default()
    print(ret)
    return HttpResponse(ret)

def StartUp(request):
    global MainM
    MainM.simulator = threading.Thread(target=MainM.run)
    MainM.simulator.start()
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")

def Close(request):
    global MainM
    MainM.Close()
    print("mainmachine close")
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")

def get_default():
    global MainM
    print("get default from MainM to Slaver")
    return MainM.get_default()

def check_room_state(request):
    rj = serialize('json', RoomStatusDao.objects.all(), cls=RoomStatusLazyEncoder)
    rj = getFieldJson(rj)
    print(rj)
    return HttpResponse(content=rj, content_type="application/json")