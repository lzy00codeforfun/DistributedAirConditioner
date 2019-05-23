from django.apps import AppConfig
from django.db.models import Q
from django.utils.dateparse import parse_date
from Logger import models
from django.shortcuts import render
import datetime
import calendar
import json

#class LoggerConfig(AppConfig):
#    name = 'Logger'


class Statistic():
	__statProcessType = None
	__inputInfo = None
	__handleInfo = None
	__lastStatResult = None

	def __init__(self, processType, processInfo):
		self.__initStatProcess(processType, processInfo)

	def __initStatProcess(self, processType, processInfo):
		self.__statProcessType = processType
		self.__inputInfo = processInfo

		if processType in ['dayreport','weekreport','monthreport','yearreport']:
			data = models.RunLog.objects.filter(roomid = processInfo['roomid'])
			self.__handleInfo = [x.__dict__ for x in data]

		elif processType == 'invoice' || processType == 'record':
			data = models.RunLog.objects.filter(roomid = processInfo['roomid'])
			self.__handleInfo = [data[-1].__dict__]
			for i in range(len(data)-2, -1, 0):
				temp = data[i].__dict__
				self.__handleInfo.append(temp)
				if temp['logtype'] == 'LOG_OTHER' and temp['flag'] == 'check_in':
					break
			self.__handleInfo = self.__handleInfo[::-1]
		else:
			pass

	def __calFeeRate(item):
		return 1

	def __calFee(item, duration):
		return self.__calFeeRate(item) * duration

	def __genReport(base, end):
		report = 
		report = {'room_id': self.__inputInfo['roomid'], 'on_off_times': 0,
			      'service_time': 0, 'fee': 0, 'dispatch_times':0, 'rdr_number': 0,
			      'change_temp_times': 0, 'change_speed_times': 0}
		
		left = False; right = False;
		for i, row in enumerate(self.__handleInfo):
			dt = datetime.datetime.strptime(row['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
			if dt >= base and dt <= end
				if not left:
					left = i
					right = True
			else:
				if right:
					right = i

		last = self.__handleInfo[left - 1]
		for i in range(left, right):
			row = self.__handleInfo[i]
			dt = datetime.datetime.strptime(row['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
				
			if row['logtype'] == "LOG_DISPATCH":
				if i == left:
					if row['status'] == 'OFF' or row['status'] == "OUT":
						report['service_time'] += (dt - base).seconds
						report['fee'] += self.__calFee(last, (dt - base).seconds)
				elif i == right - 1:
					if row['status'] != "OFF":
						report['service_time'] += (end - dt).seconds
						report['fee'] += self.__calFee(row, (end - dt).seconds)
				else:
					last_dt = datetime.datetime.strptime(last['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
					if last['status'] != 'OFF':
						report['service_time'] += (dt - last_dt).seconds
					if last['status'] != 'OFF' and last['status'] != 'OUT':
						report['fee'] += self.__calFee(last, (dt - last_dt).seconds)
				last = row
				report['dispatch_times'] += 1
				if row['flag'] == "changewind":
					report['change_speed_times'] += 1
				if row['flag'] == 'changetemp':
					report['change_temp_times'] += 1
				if row['status'] in ['ON',"OFF"]:
					report['on_off_times'] += 1
			elif row['logtype'] == "LOG_OTHER":
				if row['flag'] == 'record':
					report['rdr_number'] += 1



	def handleStatProcess(self):
		
		if self.__statProcessType == 'dayreport':
			base = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
			end = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
			self.__lastStatResult = self.__genReport(base, endh5   )		
		
		elif self.__statProcessType == 'weekreport':
			dt = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00","%Y-%m-%d %H:%M:%S")
			weekday = dt.weekday()
			if weekday == 0:
				weekday = 7
			base = dt - datetime.timedelta(days=weekday)
			end = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59","%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=(7-weekday))
			self.__lastStatResult = self.__genReport(base, end ,left, right)	

		elif self.__statProcessType == 'monthreport':
			dt = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00","%Y-%m-%d %H:%M:%S")
			monthday = calendar.monthrange(dt.year,dt.month)[1]
			base = dt - datetime.timedelta(days=dt.day-1)
			end = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59","%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=(monthday-dt.day))	
			self.__lastStatResult = self.__genReport(base, end ,left, right)
		
		elif self.__statProcessType == 'yearreport':
			dt = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00","%Y-%m-%d %H:%M:%S")
			yearday = 365
			if dt.year % 400 == 0 or (dt.year % 4 == 0 and dt.year % 100 != 0):
				yearday += 1
			noday = (dt - datetime.datetime.strptime(self.__inputInfo['btime'][:4] + "-01-01 00:00:00","%Y-%m-%d %H:%M:%S")).days
			base = dt - datetime.timedelta(days=dt.day)
			end = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59","%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=(monthday-dt.day+1))	
			self.__lastStatResult = self.__genReport(base, end ,left, right)

		elif self.__statProcessType == 'invoice':
			result = {"room_id": self.__inputInfo['roomid'], "check_in_time":0,"check_out_time":0,"fee":0}
			last = None
			for row in self.__handleInfo:
				dt = datetime.datetime.strptime(row['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
				if row['logtype'] == "LOG_OTHER" and row['flag'] == "check_in":
					result['check_in_time'] = str(dt)
				elif row['logtype'] == "LOG_OTHER" and row['flag'] == "check_out":
					result['check_out_time'] = str(dt)
				if row['logtype'] == 'LOG_DISPATCH':
					if row['status'] == 'ON':
						last = row
					elif row['status'] != "OFF" and row['status'] != "OUT"
						last_dt = datetime.datetime.strptime(last['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
						result['fee'] += self.__calFee(last, (dt - last_dt).seconds)
			self.__lastStatResult = result


		elif self.__statProcessType == 'record':
			logger = Logger()
			logger.addLog({'roomid': self.__inputInfo['roomid'], 'temperature':0, 'windspeed':0, 'status':"OFF", "logtype":"LOG_TYPE", "flag":"record"})

			templete = {"roomid":self.__inputInfo['roomid'], 'start_time':0, "end_time":0, "speed":0, "target_temper":0, "fee":0, "fee_rate":0}
			last = None
			temp = templete.copy()
			for row in self.__handleInfo:
				dt = datetime.datetime.strptime(row['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
				if row['logtype'] != 'LOG_DISPATCH':
					continue
				if row['status'] = 'ON':
					temp['start_time'] = str(dt)
					temp['speed'] = row['windspeed']
					temp['target_temper'] = row['temperature']
					last = row
				elif row['status'] in ['OFF', 'OUT']:
					last_dt = datetime.datetime.strptime(last['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
					temp['end_time'] = str(dt)
					temp['fee'] = self.__calFee(last, (dt - last_dt).seconds)
					temp['fee_rate'] = self.__calFeeRate(last)
					result.append(temp)
					temp = templete.copy()
				else if last['status'] in ['OUT', "OFF"]:
					temp['start_time'] = str(dt)
					temp['speed'] = row['windspeed']
					temp['target_temper'] = row['temperature']
					last = row
				else:
					last_dt = datetime.datetime.strptime(last['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
					temp['end_time'] = str(dt)
					temp['fee'] = self.__calFee(last, (dt - last_dt).seconds)
					temp['fee_rate'] = self.__calFeeRate(last)
					last = row
			self.__lastStatResult = result

	def printStatResult(self):

		formatData = ""
		if self.__statProcessType != 'report':
			for k in self.__lastStatResult.keys():
				formatData += "{},{}\n".format(k, self.__lastStatResult[k])
		else:
			formatData += "btime, etime, speed, target, fee_rate, fee\n"
			for row in self.__lastStatResult:
				formatData += ",".join([str(row[k]) for k in row.keys()]) + '\n'

		return formatData

class Logger():
	def addLog(self, logInfo):
		models.RunLog.objects.create(**logInfo)
