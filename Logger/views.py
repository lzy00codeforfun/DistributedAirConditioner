from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from Logger import models
from django.utils.dateparse import parse_date
import json




def controller(request):
	method = request.GET.get("method", None)
	if not method:
		return HttpResponse("params \"method\" must be included.")

	if method == "queryreport":
		return Logger_queryreport(request)
	elif method == "insert":
		return Logger_insert(request)

	#return HttpResponse("Hello, I'm Logger.Controller!")
	#return render(request, "test.html", {"data":user_list})

'''
rooms: -分隔
date：报表开始时间 Y-M-D
type：day/week/month
'''
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

def Logger_insert(request):
	props = ['userid', 'roomid', 
			 'temperature', 'windspeed', 'status']

	params = {}
	for key in props:
		params[key] = request.GET.get(key, None)

	models.RunLog.objects.create(**params)

	temp = ""
	for key in props:
		temp += "{}:{}\n".format(key, params[key])
	return render(request, "test.html", {"test1":temp})


