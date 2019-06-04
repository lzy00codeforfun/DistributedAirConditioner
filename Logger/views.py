from django.shortcuts import HttpResponse
from django.http import JsonResponse,FileResponse,Http404
from Logger import apps
from django.utils.http import urlquote
import json
from django.shortcuts import render
from Logger import models

def test(request):
	p = ['roomid','temperature','windspeed','status','logtype','flag']
	logInfo = {}
	for k in p:
		logInfo[k] = request.GET.get(k, None)
	#logInfo = {'roomid':'309c', 'temperature':25, 'windspeed':2, 'status':"HOT", 'logtype':'LOG_OTHER', 'flag':"check_out"}
	models.RunLog.objects.create(**logInfo)
	return JsonResponse(logInfo)

def LoggerQueryReport(request):
	qtype = request.GET.get("qtype", None)  
	roomid = request.GET.get("room_id", None)
	date = request.GET.get("date", None)

	stat = apps.Statistic(qtype, {'roomid':roomid, 'btime':date})
	ret = {'message':'OK'}

	ret ["result"] = stat.handleStatProcess()
	
	return JsonResponse(ret)

def LoggerPrintReport(request):
	qtype = request.GET.get("qtype", None)
	roomid = request.GET.get("room_id", None)
	date = request.GET.get("date", None)

	stat = apps.Statistic(qtype, {'roomid':roomid, 'btime':date})

	stat.handleStatProcess()
	filename = stat.printStatResult()

	file = open("downloads/"+filename, "rb")
	response = FileResponse(file)
	response['Content-Disposition'] = 'attachment;filename="{}"'.format(urlquote(filename))

	return response

def LoggerQueryInvoice(request):
	roomid = request.GET.get('room_id', None)
	stat = apps.Statistic("invoice", {'roomid':roomid})
	ret = {'message':'OK'}

	ret ["result"] = stat.handleStatProcess()
	
	return JsonResponse(ret)

def LoggerPrintInvoice(request):
	roomid = request.GET.get('room_id', None)
	stat = apps.Statistic("invoice", {'roomid':roomid})

	stat.handleStatProcess("print")
	filename = stat.printStatResult()

	file = open("downloads/"+filename, "rb")
	response = FileResponse(file)
	response['Content-Disposition'] = 'attachment;filename="{}"'.format(urlquote(filename))

	return response


def LoggerQueryRdr(request):
	roomid = request.GET.get('room_id', None)
	stat = apps.Statistic("record", {'roomid':roomid})
	ret = {'message':'OK'}

	ret ["result"] = stat.handleStatProcess()
	
	return JsonResponse(ret)


def LoggerPrintRdr(request):
	roomid = request.GET.get('room_id', None)
	stat = apps.Statistic("record", {'roomid':roomid})

	stat.handleStatProcess()
	filename = stat.printStatResult()

	file = open("downloads/"+filename, "rb")
	response = FileResponse(file)
	response['Content-Disposition'] = 'attachment;filename="{}"'.format(urlquote(filename))

	return response





