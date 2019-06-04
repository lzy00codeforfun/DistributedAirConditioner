from django.db import models
import django.utils.timezone as timezone

class RunLog(models.Model):
	currenttime = models.DateTimeField(default=timezone.now)#(auto_now_add=True)
	roomid = models.CharField(max_length = 20,default="None")
	temperature = models.FloatField(default=-1)
	windspeed = models.IntegerField(default=-1)
	status = models.CharField(max_length = 20,default="None")
	logtype = models.CharField(max_length = 20,default="None")
	flag = models.CharField(max_length = 30,default="None")

