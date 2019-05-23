from django.shortcuts import HttpResponse,JsonResponse,FileResponse,Http404
from Logger import apps
import json

def test(request):
	return render(request, "test.html")


def LoggerRequestParser(request):
	method = request.GET.get("method", None)
	method_type = request.GET.get("type", None)

	params = ['roomid', 'btime' ,'time']
	processInfo = {}
	for key in params:
		processInfo[key] = request.GET.get(key, None)

	stat = apps.Statistic(method_type, processInfo)
	ret = {"message":"OK"}

	if method == 'query':
		stat.handleStatProcess()
		ret["result"] = stat.__lastStatResult
		return JsonResponse(ret)
	elif method == 'print':
		stat.handleStatProcess()
		data = stat.printStatResult()
		file = open("report.csv", "a+")
		file.write(data)
	    response = FileResponse(file)
	    response['Content-Type'] = 'application/octet-stream'
	    response['Content-Disposition'] = 'attachment;filename="report.csv"'
        return response
	else:
		return Http404






