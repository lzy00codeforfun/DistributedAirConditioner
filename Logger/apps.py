from django.apps import AppConfig
from django.utils.dateparse import parse_date
from Logger import models
from django.shortcuts import render

#class LoggerConfig(AppConfig):
#    name = 'Logger'


class Statistic():
	__statProcessType = None
	__handleInfo = None
	__lastStatResult = None

	def __init__(self, processType, processInfo):
		self.__initStatProcess(processType, processInfo)

	def __initStatProcess(self, processType, processInfo):
		self.__statProcessType = processType

		'''
		根据processInfo从数据库拿需要的数据给self.__handleInfo
		'''

	def handleStatProcess(self):
		'''
		根据__handleInfo计算结果放在self.__lastStatResult
		'''

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

