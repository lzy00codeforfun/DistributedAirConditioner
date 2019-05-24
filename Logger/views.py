from django.shortcuts import HttpResponse,JsonResponse,FileResponse,Http404
from Logger import apps
import json

def test(request):
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
	file = open("report.csv", "a+")
	file.write(data)
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



def LoggerPrintInvoice(request):
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





