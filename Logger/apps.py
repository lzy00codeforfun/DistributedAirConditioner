from django.apps import AppConfig
from django.db.models import Q
from django.utils.dateparse import parse_date
from Logger import models
from django.shortcuts import render
import datetime

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
		'''
		根据processInfo从数据库拿需要的数据给self.__handleInfo
		'''
		data = None
		if processType == 'dayreport':
			data = models.RunLog.objects.filter(currenttime__startswith = processInfo['btime'], 
												roomid = processInfo['roomid'])
			__handleInfo = [x.__dict__ for x in data]
		elif processType == 'weekreport':
			etime = str(datetime.date(int(processInfo['btime'][:4]), int(processInfo['btime'][5:7]),
									  int(processInfo['btime'][8:])) + datetime.timedelta(days=7))
			data = model.RunLog.objects.filter(roomid = processInfo['roomid'],
											   currenttime__range = [processInfo['btime'], etime])
			__handleInfo = [x.__dict__ for x in data]
		elif processType == 'monthreport':
			data = models.RunLog.objects.filter(currenttime__year = int(processInfo['btime'][:4]),
												currenttime__month = int(processInfo['btime'][5:7]),
											    roomid = processInfo['roomid'])
			__handleInfo = [x.__dict__ for x in data]
		elif processType == 'yearreport':
			data = models.RunLog.objects.filter(currenttime__year = int(processInfo['btime'][:4]),
												roomid = processInfo['roomid'])
			__handleInfo = [x.__dict__ for x in data]
		elif processType == 'invoice' || processType == 'record':
			# 需要检验一下是否默认按照时间排序？
			data = models.RunLog.objects.filter(roomid = processInfo['roomid'])
			__handleInfo = []
			for i in range(len(data)-1, -1, 0):
				temp = __handleInfo.__dict__
				if temp['userstate'] = 'In':
					break
				__handleInfo.append(temp)
		else:
			pass

		
	def handleStatProcess(self):
		'''
		根据__handleInfo计算结果放在self.__lastStatResult
		'''
		report_templete = {'roomid': self.__inputInfo['roomid'], 'onoff_times': 0,
			               'duration': 0, 'fee': 0, 'dispatch_times':0, 'records_times': 0,
			               'changetemp_times': 0, 'changewind_times': 0}

		if self.__statProcessType == 'dayreport':
			result = [report_templete.copy] * 24
			for row in self.__handleInfo:
				dt = datetime.datetime.strptime(row['currenttime'].split(".")[0],"%Y-%m-%d %H:%M:%S")
				

		elif self.__statProcessType == 'weekreport':
			pass
		elif self.__statProcessType == 'monthreport':
			pass
		elif self.__statProcessType == 'yearreport':
			pass
		elif self.__statProcessType == 'invoice':
			pass
		elif self.__statProcessType == 'record':
			pass

		return self.__lastStatResult

	def printStatResult(self):
		formatData = None

		'''
		格式化self.__lastStatResult后返回
		'''

		return formatData



class Logger():
	def __gen(roomid):
		'''
		查询该room的最后一条数据，从而推断出当前用户id以及用户状态
		'''
	def addLog(self, logInfo):
		logInfo['userid'], logInfo['userstate'] = self.__gen(logInfo['roomid'])
		models.RunLog.objects.create(**logInfo)

	def queryLog(self, qType, qInfo):
		'''
		根据type/info，进行查询，逐渐扩展
		'''

class Report():
	__reportType = None
	def __init__(self, reportType):
		self.__reportType = reportType

	def genReport(self, logInfo):
		'''
		根据logInfo，出报表
		'''

class DetailedRecord():
	def genRecord(self, logInfo):
		'''
		根据logInfo，出详单
		'''

class Invoice():
	def genInvoice(self, logInfo):
		'''
		根据logInfo，出账单
		'''

