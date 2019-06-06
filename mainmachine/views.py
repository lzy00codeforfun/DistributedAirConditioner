from django.shortcuts import render
from django.http import HttpResponse
from .models import Request,RoomStatusDao
import threading
import time
import sys
sys.path.append("..")
from Logger.apps import Logger
MainStatus = {"open":1,"init_param":2,"run":3,"close":4}
RoomStatus = {"unregister":1,"registed":2,"waiting":"3","serving":4,"done":5}
RoomIdListSetting = ("309c","310c","311c","312c","f3")

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json
class RoomStatusLazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, RoomStatusDao):
            return str(obj)
        return super().default(obj)

fee_rate = []
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
        if tmp["speed"]!=None:
            tmp["fee_rate"] = fee_rate[tmp["speed"]]
        if type(tmp["status"]) == int:
            tmp["status"] = status_zh[tmp["status"]]
        elif type(tmp["status"]) == str:
            tmp["status"] = status_zh_str[tmp["status"]]
        if tmp["fee"] != None:
            tmp["fee"] = round(float(tmp["fee"]), 2)
        if tmp["current_temper"] != None:
            tmp["current_temper"] = round(float(tmp["current_temper"]), 2)
        res.append(tmp)

    dict = {}
    dict["message"] = "OK"
    dict["result"] = res
    #print("dict {}".format(dict))
    ret = json.dumps(dict)

    return ret
def changeTemper(mode,temper,speed):
    if mode == 0:
        flag = 1
    else:
        flag = -1
    speed = speed+1
    if speed == 1:
        temper -= 0.333333333/60
    elif speed == 2:
        temper -= 0.5/60
    else:
        temper -= 1.0/60
    #temper -= 0.5 * speed / 60  # dropTemper()
    return temper




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
        self.logger = Logger()
        self.maxserving = 3
    def changeFee(self,speed, fee):
        if speed == 0:
            tmp = float(self.low_speed_fee) / 60
        elif speed == 1:
            tmp = float(self.middle_speed_fee) / 60
        elif speed == 2:
            tmp = float(self.high_speed_fee) / 60
        return fee + tmp

    def Log(self,room_id,temper,speed,status,log_type,flag):
        dict = {}
        dict["roomid"]=room_id
        dict['temperature']=temper
        dict['windspeed']=speed
        dict['status']=status
        dict['logtype']=log_type
        dict['flag']=flag
        self.logger.addLog(dict)

    def ServingRoom(self):      # 更新当秒的温度,控制到达温度的空调进入等待

        RunningRoom = RoomStatusDao.objects.filter(status=4)
        count = 0
        for room in RunningRoom:
            if ((room.target_temper >= room.current_temper )and room.mode == 0) or ((room.target_temper <= room.current_temper) and room.mode == 1):
                room.status = RoomStatus["done"]
                room.service_time += time.time()-room.time
                room.time = time.time()
                room.fee_rate = 0
                self.Log(room.room_id,room.target_temper,room.speed,None,"LOG_DISPATCH","air_out")
                #Log()           # 停止服务的log
                #StartTemperMonitor()
                room.save()
                continue
            room.current_temper = changeTemper(room.mode,room.current_temper,room.speed)
            room.fee = self.changeFee(room.speed,room.fee)
            room.save()
            count = count + 1
        if count != self.maxserving:
            WaitingRoom = RoomStatusDao.objects.filter(status=3)
            if len(WaitingRoom) != 0:
                WaitingRoom[0].status = 4
                WaitingRoom[0].current_temper = changeTemper(WaitingRoom[0].mode, WaitingRoom[0].current_temper, WaitingRoom[0].speed)
                WaitingRoom[0].fee = self.changeFee(WaitingRoom[0].speed, WaitingRoom[0].fee)
                WaitingRoom[0].time=time.time()
                if WaitingRoom[0].mode == 0:
                    self.Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper, WaitingRoom[0].speed, "COLD", "LOG_DISPATCH", "dispatch_on")
                else:
                    self.Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper,WaitingRoom[0].speed, "HOT", "LOG_DISPATCH", "dispatch_on")
                #Log()
                WaitingRoom[0].save()
        return

    def ScheduleWaitingRoom(self):
        global RoomStatus
        WaitingRoom = RoomStatusDao.objects.filter(status=3).order_by("speed")
        cnt_wait = len(WaitingRoom)
        if cnt_wait != 0:
            RunningRoom = RoomStatusDao.objects.filter(status=4).order_by("speed","time")
            count = len(RunningRoom)
            if count <self.maxserving:
                WaitingRoom[0].status = RoomStatus["serving"]
                WaitingRoom[0].time = time.time()
                WaitingRoom[0].current_temper = changeTemper(WaitingRoom[0].mode, WaitingRoom[0].current_temper,
                                                             WaitingRoom[0].speed)
                WaitingRoom[0].fee = self.changeFee(WaitingRoom[0].speed, WaitingRoom[0].fee)
                WaitingRoom[0].save()
                if WaitingRoom[0].mode == 0:
                    self.Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper,WaitingRoom[0].speed, "COLD", "LOG_DISPATCH", "dispatch_on")
                else:
                    self.Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper, WaitingRoom[0].speed, "HOT", "LOG_DISPATCH", "dispatch_on")
                #Log()
            elif int(RunningRoom[0].speed)< int(WaitingRoom[0].speed) or ( int(RunningRoom[0].speed)== int(WaitingRoom[0].speed) and (time.time()-float(WaitingRoom[0].time))>120  ):
                RunningRoom[0].status = RoomStatus["waiting"]
                RunningRoom[0].service_time += time.time()-RunningRoom[0].time
                RunningRoom[0].time = time.time()
                RunningRoom[0].save()
                self.Log(RunningRoom[0].room_id, RunningRoom[0].target_temper, RunningRoom[0].speed, None,"LOG_DISPATCH","air_out/dispatch")
                #Log()
                WaitingRoom[0].status = RoomStatus["serving"]
                WaitingRoom[0].time = time.time()
                WaitingRoom[0].current_temper = changeTemper(WaitingRoom[0].mode, WaitingRoom[0].current_temper,
                                                             WaitingRoom[0].speed)
                WaitingRoom[0].fee = self.changeFee(WaitingRoom[0].speed, WaitingRoom[0].fee)
                WaitingRoom[0].save()
                if WaitingRoom[0].mode == 0:
                    self.Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper,WaitingRoom[0].speed, "COLD", "LOG_DISPATCH", "dispatch_on")
                else:
                    self.Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper, WaitingRoom[0].speed, "HOT", "LOG_DISPATCH", "dispatch_on")
                #Log()
        return

    def get_default(self):
        tem_dict = {"highest_temper": float(self.highest_temper), "lowest_temper": float(self.lowest_temper),
                "high_speed_fee": float(self.high_speed_fee), "low_speed_fee": float(self.low_speed_fee),
                "default_temper": float(self.default_temper), "default_speed":float(self.default_speed),
                "mode":int(self.default_mode),"middle_speed_fee":float(self.middle_speed_fee)}
        print(tem_dict)
        return tem_dict




    def run(self):
        global MainStatus
        while self.status != MainStatus["close"]:
            pre = time.time()
            # print(pre)
            # 每秒更新 当前服务队列的房间温度，（更新房间温度，如果房间温度到达目标温度，则从调度队列中换出） 从数据库中筛选出正在服务的房间（running）
            self.ServingRoom()
            #在这个模拟调度的过程中，就不需要去获取请求。只需要观察等待队列即可。


            self.ScheduleWaitingRoom()
            t = time.time()
            # test
            # print(" 1 ")
            if t-pre < 1 :
                time.sleep(1-(t-pre))


    def init_param(self,u_tem,l_tem,low_speed_fee, middle_speed_fee,high_speed_fee, d_tem, d_spd, mode):
        global MainStatus
        global fee_rate

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
        fee_rate.append(low_speed_fee)
        fee_rate.append(middle_speed_fee)
        fee_rate.append(high_speed_fee)
        print("type self.low {}".format(type(self.low_speed_fee)))
        with open("init_fee.txt","w") as f:
            print("write text")
            f.write(str(high_speed_fee)+"\n")
            f.write(str(middle_speed_fee)+"\n")
            f.write(str(low_speed_fee)+"\n")
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
    with open("Logger/rdr.txt","w") as f:
        f.write("0")
        f.close()
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
    hr = HttpResponse(content=ret,content_type="application/json")
    # hr["Access-Control-Allow-Origin"] = "*"
    # hr["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # hr["Access-Control-Max-Age"] = "1000"
    # hr["Access-Control-Allow-Headers"] = "*"
    print(hr.content)
    print(hr)
    return hr

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
