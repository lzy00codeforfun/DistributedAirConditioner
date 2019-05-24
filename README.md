**to rock** :star:



写日志方式

```python
logger = Logger()
logger.addLog(dict)

'''
dict example:
{'roomid':XXX,
 'temperature':XXX,
 'windspeed':XXX,
 'status':XXX,
 'logtype':XXX,
 'flag':XXX}
'''
```



关于写日志的一些说明：

- logtype分为“LOG_DISPATCH”和“LOG_OTHER”，前者只包括调度开关机、调风调温、出调度队列5种情况，后者包括用户到店、用户离店



- status（仅针对LOG_DISPATCH）： ON表示开机/OFF表示关机/HOT制热/COLD制冷/OUT调度出列



- flag（仅针对LOG_OTHER）:check_in表示进店/check_out表示离店