from django.db import models

class RunLog(models.Model):
	currenttime = models.DateTimeField(auto_now_add=True)
	userid = models.CharField(max_length = 10)
	roomid = models.CharField(max_length = 2)
	temperature = models.FloatField()
	windspeed = models.IntegerField()
	status = models.IntegerField()
