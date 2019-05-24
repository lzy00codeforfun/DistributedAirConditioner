from django.db import models



class test(models.Model):
    name=models.CharField(max_length=100)
    phone= models.IntegerField(default=-1)

    class Meta:
        db_table = 'test'
# Create your models here.

