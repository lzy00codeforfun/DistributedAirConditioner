from django.shortcuts import HttpResponse
from Logger import apps
import json

def test(request):
	return render(request, "test.html")


def LoggerRequestParser(request):
	method = request.GET.get("method", None)
	method_type = request.GET.get("type", None)

	params = ['roomid', 'btime', 'userid','time']
	processInfo = {}
	for key in params:
		processInfo[key] = request.GET.get(key, None)

	stat = apps.Statistic(method_type, processInfo)

	if method == 'query':
		return stat.handleStatProcess()
	elif method == 'print':
		stat.handleStatProcess()
		return stat.printStatResult()
	else:
		return HttpResponse("Method Not Found.")


def Logger_queryreport(request):
	rooms = request.GET.get("rooms", None).split('-')
	date  = request.GET.get("date" , None)
	report_type = request.GET.get("type", None)

	reports = ""
	if report_type == "day":
		for room in rooms:
			room_report = {}
			data = models.RunLog.objects.filter(currenttime__startswith = date, 
												roomid = room)
			for d in data:
				print(d.__dict__)

	return render(request, "test.html", {"test1":reports})




