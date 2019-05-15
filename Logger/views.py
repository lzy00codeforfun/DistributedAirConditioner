from django.shortcuts import render
from django.shortcuts import HttpResponse

from django.shortcuts import redirect
def test(request):
	return render(request, "test.html")

# 统一用GET方式
def controller(request):
	method = request.GET.get("method", None)
	if not method:
		return HttpResponse("params \"method\" must be included.")

	if method == "query":
		return Logger_query(request)
	elif method == "insert":
		pass

	#return HttpResponse("Hello, I'm Logger.Controller!")
	#return render(request, "test.html", {"data":user_list})

def Logger_query(request):
	rooms = request.GET.get("rooms", None)
	date  = request.GET.get("date" , None)
	report_type = request.GET.get("type", None)

	msg = "rooms:{},date:{},report_type:{}".format(rooms, date, report_type)

	return render(request, "test.html", {"test1":msg})


