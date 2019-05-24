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
logger = Logger
class RoomStatusLazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, RoomStatusDao):
            return str(obj)
        return super().default(obj)
# Create your views here.
def getFieldJson_single_room(jsons):
    """
        transform the origin database model serial json-str to
        the json data needed by the front-end
    :param jsons: the serial json-str from the origin
    :return: json-form data
    """
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
    dict = {}
    dict["message"] = "OK"
    dict["result"] = tmp
    ret = json.dumps(dict)
    return ret


MainStatus = {"open":1,"init_param":2,"run":3,"close":4}
RoomStatus = {"unregister":1,"registed":2,"waiting":"3","serving":4,"done":5}

def GetNowTime():
    return time.time()


def Log( room_id, temper, speed, status, log_type, flag):
    global logger
    dict = {}
    dict["room_id"] = room_id
    dict['temperature'] = temper
    dict['windspeed'] = speed
    dict['status'] = status
    dict['logtype'] = log_type
    dict['flag'] = flag
    logger.addLog(dict)
def RequestUpdateTemper(request):
    global RoomStatus
    room = RoomStatusDao.objects.get(room_id=request.GET.get("room_id"))
    room.target_temper = request.GET.get("target_temper")
    if room.status == RoomStatus["serving"]:
        room.save()
        if room.mode == 0:
            Log(room.room_id, room.target_temper, room.speed, "COLD",
                     "LOG_DISPATCH", 0)
        else:
            Log(room.room_id, room.target_temper, room.speed, "HOT",
                     "LOG_DISPATCH", 0)
        #Log()  温度改变
    else:
        roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("speed","time")
        count = len(roomlist)
        if count < 3:
            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", 0)
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", 0)
            #Log()
        else:
            if roomlist[0].speed < int(room.speed):
                room.status = RoomStatus["serving"]
                room.time = GetNowTime()
                room.save()
                if room.mode == 0:
                    Log(room.room_id, room.target_temper, room.speed, "COLD",
                        "LOG_DISPATCH", 0)
                else:
                    Log(room.room_id, room.target_temper, room.speed, "HOT",
                        "LOG_DISPATCH", 0)
                #Log()
                roomlist[0].status = RoomStatus["waiting"]
                roomlist[0].service_time += time.time()-roomlist[0].time
                roomlist[0].time = GetNowTime()
                roomlist[0].save()
                Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, "OUT", "LOG_DISPATCH", 0)
                #Log()
            else:
                room.status = RoomStatus["waiting"]
                room.time = GetNowTime()
                room.save()

    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")


# slaver/change_speed?room_id=312c&speed=3
def RequestUpdateSpeed(request):
    global RoomStatus
    room = RoomStatusDao.objects.get(room_id=request.GET.get("room_id"))
    room.speed = request.GET.get("speed")
    if room.status == RoomStatus["serving"]:
    #    room.speed = request.GET.get("speed")
        room.save()
        if room.mode == 0:
            Log(room.room_id, room.target_temper, room.speed, "COLD",
                "LOG_DISPATCH", 0)
        else:
            Log(room.room_id, room.target_temper, room.speed, "HOT",
                "LOG_DISPATCH", 0)
        #Log()
    else:
        roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("speed","time")
        count = len(roomlist)
        if count < 3:
            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", 0)
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", 0)
            #Log()
        else:
            if roomlist[0].speed < int(room.speed):
                room.status = RoomStatus["serving"]
                room.time = GetNowTime()
                room.save()
                if room.mode == 0:
                    Log(room.room_id, room.target_temper, room.speed, "COLD",
                        "LOG_DISPATCH", 0)
                else:
                    Log(room.room_id, room.target_temper, room.speed, "HOT",
                        "LOG_DISPATCH", 0)
                #Log()
                roomlist[0].status = RoomStatus["waiting"]
                roomlist[0].service_time += time.time()-roomlist[0].time
                roomlist[0].time = GetNowTime()
                roomlist[0].save()
                Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, "OUT", "LOG_DISPATCH", 0)
                #Log()
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
    room = RoomStatusDao.objects.get(room_id = request.GET.get("room_id"))
    settings = get_default()
    # room.status = RoomStatus["waiting"]
    room.target_temper = settings["default_temper"]
    room.speed = settings["default_speed"]
    room.mode = settings["mode"]
    room.current_temper = request.GET.get("current_temper")
    room.save()
    # Log() 请求开机
    Log(room.room_id, room.target_temper, room.speed, "ON", "LOG_DISPATCH", 0)
    roomlist = RoomStatusDao.objects.filter(status=RoomStatus["serving"]).order_by("-speed").order_by(
        "time")
    count = len(roomlist)
    if count < 3:
        room.status = RoomStatus["serving"]
        room.time = GetNowTime()
        room.save()
        if room.mode == 0:
            Log(room.room_id, room.target_temper, room.speed, "COLD",
                "LOG_DISPATCH", 0)
        else:
            Log(room.room_id, room.target_temper, room.speed, "HOT",
                "LOG_DISPATCH", 0)
        #Log()
    else:
        if roomlist[0].speed < int(room.speed):
            room.status = RoomStatus["serving"]
            room.time = GetNowTime()
            room.save()
            if room.mode == 0:
                Log(room.room_id, room.target_temper, room.speed, "COLD",
                    "LOG_DISPATCH", 0)
            else:
                Log(room.room_id, room.target_temper, room.speed, "HOT",
                    "LOG_DISPATCH", 0)
            #Log() # dispatch log
            roomlist[0].status = RoomStatus["waiting"]
            roomlist[0].service_time += time.time() - roomlist[count-1].time
            roomlist[0].time = GetNowTime()
            roomlist[0].save()
            Log(roomlist[0].room_id, roomlist[0].target_temper, roomlist[0].speed, "OUT", "LOG_DISPATCH", 0)
            #Log()
        else:
            room.status = RoomStatus["waiting"]
            room.time = GetNowTime()
            room.save()
    ret = serialize('json', RoomStatusDao.objects.filter(room_id = request.GET.get("room_id")), cls=RoomStatusLazyEncoder)
    #print(ret)
    ret = getFieldJson_single_room(ret)
    ret = json.loads(ret)
    ret["result"]["highest_temper"]=settings["highest_temper"]
    ret["result"]["lowest_temper"]=settings["lowest_temper"]
    ret = json.dumps(ret)
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
    Log(room.room_id, room.target_temper, room.speed, "OFF", "LOG_DISPATCH", 0)
    #Log()
    print("room {} closed ".format(request.GET.get("room_id")))
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")


def RequestFee(request):

    ret = serialize('json', RoomStatusDao.objects.get(request.GET.get("room_id")), cls=RoomStatusLazyEncoder)
    ret = getFieldJson_single_room(ret)
    return HttpResponse(content=ret, content_type="application/json")

def ChechIn(request):
    room_id = request.GET.get("room_id")
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")

def CheckOut(request):
    dict = {}
    dict["message"] = "OK"
    dict["result"] = None
    ret = json.dumps(dict)
    return HttpResponse(content=ret, content_type="application/json")