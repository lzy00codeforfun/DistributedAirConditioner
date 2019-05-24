from django.db import models
import django.utils.timezone as timezone

class RunLog(models.Model):
	currenttime = models.DateTimeField(default=timezone.now)#(auto_now_add=True)
	roomid = models.CharField(max_length = 20)
	temperature = models.FloatField()
	windspeed = models.IntegerField()
	status = models.CharField(max_length = 20)
	logtype = models.CharField(max_length = 20)
	flag = models.CharField(max_length = 30)

