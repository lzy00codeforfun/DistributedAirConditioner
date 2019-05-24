from django.shortcuts import render
from django.http import HttpResponse
from . import models

def index(request):
    return HttpResponse("okok")
# Create your views here.

def insert(request):
    models.test.objects.create(name='liuzhaoyan',phone=10086)
    results = models.test.objects.all()

    print(results)
    print(type(results))
    return HttpResponse("type {}".format(results[1].name))