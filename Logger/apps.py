from django.apps import AppConfig
from django.db.models import Q
from django.http import Http404
from django.utils.dateparse import parse_date
from Logger import models
from django.shortcuts import render
import datetime
import calendar
import json
from Logger import Printer
import django.utils.timezone as timezone

class Statistic():
	__statProcessType = None
	__inputInfo = None
	__handleInfo = None
	__lastStatResult = None

	def __init__(self, processType, processInfo):
		self.__initStatProcess(processType, processInfo)

	def __getTime(self):
		btime = None; etime = None
		processType = self.__statProcessType
		if processType == 'day':
			btime = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
			etime = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
		elif processType == 'week':
			dt = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00","%Y-%m-%d %H:%M:%S")
			weekday = dt.weekday()
			if weekday == 0:
				weekday = 7
			btime = dt - datetime.timedelta(days=weekday)
			etime = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59","%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=(6-weekday))
		elif processType == 'month':
			dt = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00","%Y-%m-%d %H:%M:%S")
			monthday = calendar.monthrange(dt.year,dt.month)[1]
			btime = dt - datetime.timedelta(days=dt.day-1)
			etime = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59","%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=(monthday-dt.day))	
		elif processType == 'year':
			dt = datetime.datetime.strptime(self.__inputInfo['btime'] + " 00:00:00","%Y-%m-%d %H:%M:%S")
			yearday = 365
			if dt.year % 400 == 0 or (dt.year % 4 == 0 and dt.year % 100 != 0):
				yearday += 1
			noday = (dt - datetime.datetime.strptime(self.__inputInfo['btime'][:4] + "-01-01 00:00:00","%Y-%m-%d %H:%M:%S")).days
			btime = dt - datetime.timedelta(days=noday)
			etime = datetime.datetime.strptime(self.__inputInfo['btime'] + " 23:59:59","%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=(yearday-noday-1))	
		return btime, etime

	def __initStatProcess(self, processType, processInfo):
		self.__statProcessType = processType
		self.__inputInfo = processInfo

		if processType in ['day','week','month','year']:
			data = models.RunLog.objects.filter(roomid = processInfo['roomid'])
			self.__handleInfo = [x.__dict__ for x in data]

			btime, etime = self.__getTime()		
			temp = []
			for row in self.__handleInfo:
				dt = datetime.datetime.strptime(str(row['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")
				if dt >= btime and dt <= etime:
					temp.append(row)
			self.__handleInfo = temp

		elif processType == 'invoice' or processType == 'record':
			data = models.RunLog.objects.filter(roomid = processInfo['roomid'])
			data = [x.__dict__ for x in data]
			if len(data) > 1:
				self.__handleInfo = [data[-1]]
				for i in range(len(data)-2, -1, -1):
					temp = data[i]
					self.__handleInfo.append(temp)
					if temp['logtype'] == 'LOG_OTHER' and temp['flag'] == 'check_in':
						break
				self.__handleInfo = self.__handleInfo[::-1]
			else:
				self.__handleInfo = []
		else:
			pass 

	def __calRdrTimes(self):
		data = models.RunLog.objects.filter(roomid = self.__inputInfo['roomid'])
		data = [x.__dict__ for x in data]
		if len(data) < 2:
			return 0
		handleInfo = [data[-1]]
		for i in range(len(data)-2, -1, -1):
			temp = data[i]
			handleInfo.append(temp)
			if temp['logtype'] == 'LOG_OTHER' and temp['flag'] == 'check_in':
				break
		handleInfo = handleInfo[::-1]

		templete = {"room_id":self.__inputInfo['roomid'], 'start_time':0, "end_time":0, "speed":0,  "fee":0, "fee_rate":0}
			
		last = None
		result = []
		rock = False
		for i, row in enumerate(handleInfo):
			if rock:
				break
			dt = datetime.datetime.strptime(str(row['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")
			if row['logtype'] == "LOG_OTHER" and row['flag'] == 'check_out':
				rock = True
			if last == None:
				if row['flag'] != 'check_in':
					break
				last = row
			else:
				last_dt = datetime.datetime.strptime(str(last['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")

				if last['flag'] in ['change_status', 'dispatch_on']:
					temp = templete.copy()
					temp['start_time'] = str(last_dt)
					temp['end_time'] = str(dt)
					temp['fee'] = self.__calFee(last, (dt - last_dt).seconds)
					temp['speed'] = last['windspeed']
					temp['fee_rate'] = self.__calFeeRate(last)
					result.append(temp)
				last = row
		new_result = []
		if len(result) <= 1:
			new_result = result
		else:
			last = result[0]
			for i in range(1, len(result)):
				if last['speed'] == result[i]['speed'] and last['end_time'] == result[i]['start_time']:
					result[i]['start_time'] = last['start_time']
					result[i]['fee'] += last['fee']
				else:
					new_result.append(last)
				last = result[i]
			if len(new_result) > 0:
				if last['speed'] != new_result[-1]['speed'] or last['end_time'] != new_result[-1]['end_time']:
					new_result.append(last) 
			elif len(new_result) == 0:
				new_result.append(last)

		return len(new_result)





	def __calFeeRate(self, item):
		file = open("init_fee.txt",'r')
		f1, f2, f3 = [float(x.strip()) for x in file.readlines()]
		file.close()
		if item['windspeed'] == 2:
			return f1
		elif item['windspeed'] == 1:
			return f2
		elif item['windspeed'] == 0:
			return f3
		else:
			return 0

	def __calFee(self, item, duration):
		return self.__calFeeRate(item) * duration / 60

	def __genReport(self):
		report = {'room_id': self.__inputInfo['roomid'], 'on_off_times': 0,
			      'service_time': 0, 'fee': 0, 'dispatch_times':0, 'rdr_number': 0,
			      'change_temp_times': 0, 'change_speed_times': 0}
		
		if len(self.__handleInfo) == 0:
			return report
		else:
			last = None
			rock = True
			for i, row in enumerate(self.__handleInfo):
				if rock and row['flag'] != 'check_in':
					continue
				rock = False
				dt = datetime.datetime.strptime(str(row['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")				
				if row['logtype'] == 'LOG_DISPATCH' and row['flag'] == "air_out/dispatch":
					report['dispatch_times'] += 1
				if row['flag'] == 'request_on' or row['flag'] == 'request_off':
					report['on_off_times'] += 1
				if last == None:
					if row['flag'] != 'check_in':
						return report
					last = row
				else:
					last_dt = datetime.datetime.strptime(str(last['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")
					if row['flag'] == "change_status":
						if row['windspeed'] != last['windspeed']:
							report['change_speed_times'] += 1
						if row['temperature'] != last['temperature']:
							report['change_temp_times'] += 1
					if last['flag'] in ['change_status', 'dispatch_on']:
						report['service_time'] += (dt - last_dt).seconds
					if last['flag'] in ['change_status', 'dispatch_on']:
						report['fee'] += self.__calFee(last, (dt - last_dt).seconds)
					last = row

		report['rdr_number'] = self.__calRdrTimes()
		report['fee'] = round(report['fee'],3)
		return report


	def handleStatProcess(self, op="query"):
		
		if self.__statProcessType in ['day', 'week', 'month', 'year']:
			self.__lastStatResult = self.__genReport()		
		
		elif self.__statProcessType == 'invoice':
			result = {"room_id": self.__inputInfo['roomid'], "check_in_time":0,"check_out_time":0,"fee":0}
			last = None
			rock = False
			for row in self.__handleInfo:
				if rock:
					break
				dt = datetime.datetime.strptime(str(row['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")
				if row['logtype'] == "LOG_OTHER" and row['flag'] == "check_in":
					result['check_in_time'] = str(dt)
				elif row['logtype'] == "LOG_OTHER" and row['flag'] == "check_out":
					result['check_out_time'] = str(dt)
					rock = True
				if last == None:
					if row['flag'] != 'check_in':
						break
					last = row
				else:
					last_dt = datetime.datetime.strptime(str(last['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")
					if last['flag'] in ['change_status', 'dispatch_on']:
						result['fee'] += self.__calFee(last, (dt - last_dt).seconds)
					last = row
			result['fee'] = round(result['fee'], 3)
			if result['check_out_time'] == 0:
				result['check_out_time'] = str(datetime.datetime.now()).split(".")[0]
			self.__lastStatResult = result

		elif self.__statProcessType == 'record':
			#logger = Logger()
			#logger.addLog({'roomid': self.__inputInfo['roomid'], 'temperature':0, 'windspeed':0, 'status':"HOT", "logtype":"LOG_OTHER", "flag":"record"})

			templete = {"room_id":self.__inputInfo['roomid'], 'start_time':0, "end_time":0, "speed":0,  "fee":0, "fee_rate":0}
			
			last = None
			result = []
			rock = False
			for i, row in enumerate(self.__handleInfo):
				if rock:
					break
				if row['flag'] == 'check_out' and row['logtype'] == 'LOG_OTHER':
					rock = True
				dt = datetime.datetime.strptime(str(row['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")
				if last == None:
					if row['flag'] != 'check_in':
						break
					last = row
				else:
					last_dt = datetime.datetime.strptime(str(last['currenttime']).split(".")[0],"%Y-%m-%d %H:%M:%S")

					if last['flag'] in ['change_status', 'dispatch_on']:
							temp = templete.copy()
							temp['start_time'] = str(last_dt)
							temp['end_time'] = str(dt)
							temp['fee'] = self.__calFee(last, (dt - last_dt).seconds)
							temp['speed'] = last['windspeed']
							temp['fee_rate'] = self.__calFeeRate(last)
							result.append(temp)
					last = row
			new_result = []
			if len(result) <= 1:
				new_result = result
			else:
				last = result[0]
				for i in range(1, len(result)):
					if last['speed'] == result[i]['speed'] and last['end_time'] == result[i]['start_time']:
						result[i]['start_time'] = last['start_time']
						result[i]['fee'] += last['fee']
					else:
						new_result.append(last)
					last = result[i]
				if len(new_result) > 0:
					if last['speed'] != new_result[-1]['speed'] or last['end_time'] != new_result[-1]['end_time']:
						new_result.append(last) 
				elif len(new_result) == 0:
					new_result.append(last)
				
			for result in new_result:
				result['fee'] = round(result['fee'], 3)

			self.__lastStatResult = new_result

		return self.__lastStatResult

	def printStatResult(self):

		formatData = ""
		if self.__statProcessType == 'record':
			return Printer.printRdr(self.__inputInfo['roomid'] + "-详单.xls", self.__inputInfo['roomid'], self.__lastStatResult)
		elif self.__statProcessType == 'invoice':
			return Printer.printInvoice(self.__inputInfo['roomid'] + "-账单.xls", self.__inputInfo['roomid'], self.__lastStatResult)
		else:
			btime, etime = self.__getTime() 
			btime = str(btime)
			etime = str(etime)
			if self.__statProcessType == 'day':
				return Printer.printReport(self.__inputInfo['roomid'] + "-日报表.xls", self.__inputInfo['roomid'], self.__statProcessType,
					                       self.__lastStatResult, btime, etime)
			elif self.__statProcessType == 'week':
				return Printer.printReport(self.__inputInfo['roomid'] + "-周报表.xls", self.__inputInfo['roomid'], self.__statProcessType,
					                       self.__lastStatResult, btime, etime)
			elif self.__statProcessType == 'month':
				return Printer.printReport(self.__inputInfo['roomid'] + "-月报表.xls", self.__inputInfo['roomid'], self.__statProcessType,
					                       self.__lastStatResult, btime, etime)
			else:
				return Printer.printReport(self.__inputInfo['roomid'] + "-年报表.xls", self.__inputInfo['roomid'], self.__statProcessType,
					                       self.__lastStatResult, btime, etime)

		return formatData

class Logger():
	def addLog(self, logInfo1):
		logInfo = {}
		for k in logInfo1.keys():
			if logInfo1[k] != None:
				logInfo[k] = logInfo1[k]
		models.RunLog.objects.create(**logInfo)

