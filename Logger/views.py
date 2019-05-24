from django.shortcuts import HttpResponse
from django.http import JsonResponse,FileResponse,Http404
from Logger import apps
import json
from django.shortcuts import render
from Logger import models

def test(request):
	logInfo = {'roomid':'309c', 'temperature':25, 'windspeed':2, 'status':"HOT", 'logtype':'LOG_OTHER', 'flag':"check_out"}
	models.RunLog.objects.create(**logInfo)
	return render(request, "test.html")

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
	data = stat.printStatResult()
	file = open("report.csv", "w") 
	file.write(data)
	file.close()
	file = open("report.csv","rb")
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="report.csv"'

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

	stat.handleStatProcess()
	data = stat.printStatResult()
	file = open("invoice.csv", "a+")
	file.write(data)
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="invoice.csv"'

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
	data = stat.printStatResult()
	file = open("record.csv", "a+")
	file.write(data)
	response = FileResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="record.csv"'

	return response



