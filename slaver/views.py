from django.shortcuts import render
from django.http import HttpResponse
#from .models import Request,RoomStatusDao
import sys
sys.path.append("..")
from mainmachine.models import  RoomStatusDao
from mainmachine.views import get_default
import threading
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json
from Logger.apps import Logger
logger = Logger()
class RoomStatusLazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, RoomStatusDao):
            return str(obj)
        return super().default(obj)
# Create your views here.

fee = None
hl_temper =None
def getFieldJson_single_room(jsons):
    """
        transform the origin database model serial json-str to
        the json data needed by the front-end
    :param jsons: the serial json-str from the origin
    :return: json-form data
    """
    global fee
    global hl_temper
    if fee == None:
        settings = get_default()
        fee = []
        hl_temper = []
        hl_temper.append(settings['highest_temper'])
        hl_temper.append(settings['lowest_temper'])
        fee.append(settings['low_speed_fee'])
        fee.append(settings['middle_speed_fee'])
        fee.append(settings['high_speed_fee'])
    jsons = json.loads(jsons)
    jsons = jsons[0]
    print(jsons)
    js = jsons
    tmp = js["fields"]
    tmp.pop("time")
    status_zh = {1:"未入住",2:"关机",3:"等待中",4:"服务中",5:"待机"}
    status_zh_str = {"1": "未入住", "2": "关机", "3": "等待中", "4": "服务中", "5": "待机"}
    if type(tmp["status"]) == int:
        tmp["status"] = status_zh[tmp["status"]]
    elif type(tmp["status"]) == str:
        tmp["status"] = status_zh_str[tmp["status"]]
    if tmp["speed"] != None:
        tmp["fee_rate"]=fee[tmp["speed"]]
    tmp["fee"] = round(float(tmp["fee"]),2)
    tmp["current_temper"] = round(float(tmp["current_temper"]),2)
    tmp["highest_temper"]=hl_temper[0]
    tmp["lowest_temper"]=hl_temper[1]
    dict = {}
    dict["message"] = "OK"
    dict["result"] = tmp
    ret = json.dumps(dict)
    return ret


MainStatus = {"open":1,"init_param":2,"run":3,"close":4}
RoomStatus = {"unregister":1,"registed":2,"waiting":"3","serving":4,"done":5}
maxserving = 2

def GetNowTime():
    return time.time()


def Log( room_id, temper, speed, status, log_type, flag):
    global logger
    dict = {}
    dict["roomid"] = room_id
    dict['temperature'] = temper
    dict['windspeed'] = speed
    dict['status'] = status
    dict['logtype'] = log_type
    dict['flag'] = flag
    logger.addLog(dict)
def RequestUpdateTemper(request):
    global RoomStatus
    global maxserving
    room = RoomStatusDao.objects.get(room_id=request.GET.get("room_id"))
    room.target_temper = request.GET.get("target_temper")
    if room.status == RoomStatus["serving"]:
        room.save()
        if room.mode == 0:
            Log(room.room_id, room.target_temper, room.speed, "COLD",
                     "LOG_DISPATCH", "change_status")
        else:
            Log(room.room_id, room.target_temper, room.speed, "HOT",
                     "LOG_DISPATCH", "change_status")
       
    elif room.status != RoomStatus["done"]:
        roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("speed","time")
        count = len(roomlist)
        if count < maxserving:
            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", "dispatch_on")
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", "dispatch_on")
           
        else:
            if roomlist[0].speed < int(room.speed):
                room.status = RoomStatus["serving"]
                room.time = GetNowTime()
                room.save()
                if room.mode == 0:
                    Log(room.room_id, room.target_temper, room.speed, "COLD",
                        "LOG_DISPATCH", "dispatch_on")
                else:
                    Log(room.room_id, room.target_temper, room.speed, "HOT",
                        "LOG_DISPATCH", "dispatch_on")
                
                roomlist[0].status = RoomStatus["waiting"]
                roomlist[0].service_time += time.time()-roomlist[0].time
                roomlist[0].time = GetNowTime()
                roomlist[0].save()
                Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, None, "LOG_DISPATCH", "air_out/dispatch")
            else:
                room.status = RoomStatus["waiting"]
                room.time = GetNowTime()
                room.save()
    else:
        room.save()
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")


# slaver/change_speed?room_id=312c&speed=3
def RequestUpdateSpeed(request):
    global RoomStatus
    global maxserving
    room = RoomStatusDao.objects.get(room_id=request.GET.get("room_id"))
    room.speed = request.GET.get("speed")
    if room.status == RoomStatus["done"]:
        room.save()
    elif room.status == RoomStatus["serving"]:
    #    room.speed = request.GET.get("speed")
        room.save()
        WaitingRoom = RoomStatusDao.objects.filter(status=RoomStatus["waiting"]).order_by("speed", "time")
        if len(WaitingRoom) != 0:
            if room.speed<WaitingRoom[0].speed or ( room.speed == WaitingRoom[0].speed and time.time()-WaitingRoom[0].time > 120 ):
                WaitingRoom[0].status = 4
               # WaitingRoom[0].current_temper = changeTemper(WaitingRoom[0].mode, WaitingRoom[0].current_temper,
               #                                              WaitingRoom[0].speed)
               # WaitingRoom[0].fee = self.changeFee(WaitingRoom[0].speed, WaitingRoom[0].fee)
                WaitingRoom[0].time = time.time()
                if WaitingRoom[0].mode == 0:
                    Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper, WaitingRoom[0].speed, "COLD", "LOG_DISPATCH", "dispatch_on")
                else:
                    Log(WaitingRoom[0].room_id, WaitingRoom[0].target_temper, WaitingRoom[0].speed, "HOT", "LOG_DISPATCH", "dispatch_on")
                # Log()
                WaitingRoom[0].save()

                room.status = RoomStatus["waiting"]
                room.service_time += time.time() - room.time
                room.time = time.time()
                room.save()
                Log(room.room_id, room.target_temper, room.speed, None,
                         "LOG_DISPATCH", "air_out/dispatch")
        if room.mode == 0:
            Log(room.room_id, room.target_temper, room.speed, "COLD",
                "LOG_DISPATCH", "change_status")
        else:
            Log(room.room_id, room.target_temper, room.speed, "HOT",
                "LOG_DISPATCH","change_status")
      
    else:
        roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("speed","time")
        count = len(roomlist)
        if count < maxserving:
            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", "dispatch_on")
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", "dispatch_on")
        else:
            if roomlist[0].speed < int(room.speed):
                room.status = RoomStatus["serving"]
                room.time = GetNowTime()
                room.save()
                if room.mode == 0:
                    Log(room.room_id, room.target_temper, room.speed, "COLD",
                        "LOG_DISPATCH", "dispatch_on")
                else:
                    Log(room.room_id, room.target_temper, room.speed, "HOT",
                        "LOG_DISPATCH", "dispatch_on")
                
                roomlist[0].status = RoomStatus["waiting"]
                roomlist[0].service_time += time.time()-roomlist[0].time
                roomlist[0].time = GetNowTime()
                roomlist[0].save()
                Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, None,
                         "LOG_DISPATCH", "air_out/dispatch")
            else:
                room.status = RoomStatus["waiting"]
                room.time = GetNowTime()
                room.save()

    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")

# slaver/RequestOn?room_id=310c
def RequestOpen(request):
    global RoomStatus
    global maxserving
    room = RoomStatusDao.objects.get(room_id = request.GET.get("room_id"))
    settings = get_default()
    if room.status == RoomStatus["registed"]:
        # room.status = RoomStatus["waiting"]
        room.target_temper = settings["default_temper"]
        room.speed = settings["default_speed"]
        room.mode = settings["mode"]
        cur_temper = request.GET.get("current_temper")
        room.current_temper = request.GET.get("current_temper")
        room.save()
        
        Log(room.room_id, room.target_temper, room.speed, None, "LOG_OTHER", "request_on")
        roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("speed","time")
        count = len(roomlist)
        if (float(cur_temper) <= room.target_temper and room.mode == 0) or (
                float(cur_temper) >= room.target_temper and room.mode == 1):
            room.status = RoomStatus["done"]
            room.save()
            ret = serialize('json', RoomStatusDao.objects.filter(room_id=request.GET.get("room_id")),
                            cls=RoomStatusLazyEncoder)
            ret = getFieldJson_single_room(ret)
            return HttpResponse(content=ret, content_type="application/json")
        if count < maxserving:

            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", "dispatch_on")
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", "dispatch_on")
        else:
            if roomlist[0].speed < int(room.speed):
                room.status = RoomStatus["serving"]
                room.time = GetNowTime()
                room.save()
                if room.mode == 0:
                    Log(room.room_id, room.target_temper, room.speed, "COLD",
                        "LOG_DISPATCH", "dispatch_on")
                else:
                    Log(room.room_id, room.target_temper, room.speed, "HOT",
                        "LOG_DISPATCH", "dispatch_on")
             
                roomlist[0].status = RoomStatus["waiting"]
                roomlist[0].service_time += time.time() - roomlist[count-1].time
                roomlist[0].time = GetNowTime()
                roomlist[0].save()
                Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, None, "LOG_DISPATCH", "air_out/dispatch")
            else:
                room.status = RoomStatus["waiting"]
                room.time = GetNowTime()
                room.save()
    elif room.status ==RoomStatus["done"]:
        room.current_temper = request.GET.get("current_temper")
        room.save()
        roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("speed","time")
        count = len(roomlist)
        if count < maxserving:
            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", "dispatch_on")
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", "dispatch_on")
        else:
            if roomlist[0].speed < int(room.speed):
                room.status = RoomStatus["serving"]
                room.time = GetNowTime()
                room.save()
                if room.mode == 0:
                    Log(room.room_id, room.target_temper, room.speed, "COLD",
                        "LOG_DISPATCH", "dispatch_on")
                else:
                    Log(room.room_id, room.target_temper, room.speed, "HOT",
                        "LOG_DISPATCH", "dispatch_on")
                
                roomlist[0].status = RoomStatus["waiting"]
                roomlist[0].service_time += time.time() - roomlist[0].time
                roomlist[0].time = GetNowTime()
                roomlist[0].save()
                Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, None, "LOG_DISPATCH", "air_out/dispatch")
            else:
                room.status = RoomStatus["waiting"]
                room.time = GetNowTime()
                room.save()
    elif room.status == RoomStatus["unregister"]:
        dict ={}
        dict["message"]="Failed"
        dict["result"]=None
        return HttpResponse(content=json.dumps(dict), content_type="application/json")
    else:
        dict ={}
        dict["message"]="Already open now"
        dict["result"]=None
        return HttpResponse(content=json.dumps(dict), content_type="application/json")

    ret = serialize('json', RoomStatusDao.objects.filter(room_id = request.GET.get("room_id")), cls=RoomStatusLazyEncoder)
    ret = getFieldJson_single_room(ret)
    return HttpResponse(content=ret, content_type="application/json")


# slaver/RequestOff?room_id=
# 是否需要消除温度 待完善
def RequestClose(request):
    global RoomStatus
    room = RoomStatusDao.objects.get(room_id=request.GET.get("room_id"))

    if room.status == RoomStatus["serving"]:
        room.service_time += time.time() - room.time
        room.time = time.time()
    room.status = RoomStatus["registed"]
    room.save()
    Log(room.room_id, room.target_temper, room.speed, None, "LOG_OTHER", "request_off")
    Log(room.room_id, room.target_temper, room.speed, None, "LOG_DISPATCH", "dispatch_off")
    
    print("room {} closed ".format(request.GET.get("room_id")))
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")


def RequestFee(request):

    ret = serialize('json', RoomStatusDao.objects.filter(room_id=request.GET.get("room_id")), cls=RoomStatusLazyEncoder)
    ret = getFieldJson_single_room(ret)
    return HttpResponse(content=ret, content_type="application/json")

def ChechIn(request):
    #room_id = request.GET.get("room_id")
    room_id = request.GET.get("room_id")
    dict = {}
    print("check_in {}".format(room_id))
    dict["message"] = "OK"
    dict["result"] = None
    Log(room_id, None, None, None, "LOG_OTHER", "check_in")
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")

def CheckOut(request):
    room_id = request.GET.get("room_id")
    room = RoomStatusDao.objects.get(room_id=room_id)
    if room.status != RoomStatus["registed"]:
        room.status = RoomStatus["registed"]
        Log(room.room_id, room.target_temper, room.speed, None, "LOG_OTHER", "request_off")
        Log(room.room_id, room.target_temper, room.speed, None, "LOG_DISPATCH", "dispatch_off")
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    Log(room_id, None, None, None, "LOG_OTHER", "check_out")
    return HttpResponse(content=ret, content_type="application/json")
