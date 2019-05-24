from django.db import models

# Create your models here.

class Request(models.Model):
    time = models.DateTimeField()
    speed = models.IntegerField()
    target_temper = models.IntegerField()
    room_id = models.CharField(max_length=20)
    class Meta:
        db_table = "RequestMM"

RoomStatus = {"unregister":1,"registed":2,"waiting":"3","serving":4,"done":5}

# 房间状态对象
class RoomStatusDao(models.Model):
    """
        status :
                1   未注册
                2   已注册 未开机
                3   已注册 开机 未在服务（即为在等待队列中）
                4   已注册 开机 正在服务中
                5   已注册 开机 已达到温度
        time :
                若 status = 4 ，则该时间表示已经服务的时长
                若 status = 3 ，则该时间表示等待了多久
    """
    room_id = models.CharField(max_length=20)
    current_temper = models.FloatField(null=True)
    speed = models.IntegerField(null=True)
    fee = models.FloatField(null=True,default=0.0)
    fee_rate = models.FloatField(null=True)
    # 1 "未入住" , 2 "关机" ， 3 "等待中" , 4 "服务中" , 5 "待机"
    status = models.IntegerField(null=True)
    #在调出服务的时候，加上当前时间+服务开始的时间
    service_time = models.FloatField(null=True,default=0.0)
    target_temper = models.FloatField(null=True)
    mode = models.IntegerField(null=True)


    time = models.FloatField(null=True)
    def to_json(self):
        return {"room_id":self.room_id}
    @classmethod
    def create(cls,**kwargs):
        global RoomStatus
        room = cls(room_id=kwargs["room_id"], status=RoomStatus['registed'], target_temper=None, current_temper=None,
                   speed=None, fee=None, fee_rate = None,service_time=None, time=None)
        return room
    class Meta:
        db_table = "Room"