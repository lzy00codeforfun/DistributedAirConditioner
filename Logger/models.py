from django.db import models


class RunLog(models.Model):
	currenttime = models.DateTimeField(auto_now_add=True)
	roomid = models.CharField(max_length = 10)
	temperature = models.FloatField()
	windspeed = models.IntegerField()
	status = models.CharField(max_length = 10)
	logtype = models.CharField(max_length = 10)
	flag = models.CharField(max_length = 10)

