import xlwt

speed = ['低','中','高']
rtypes = {'day':'日','week':'周','month':'月','year':'年','other':""}

def getTopicStyle():
	font = xlwt.Font()
	font.bold = True
	font.height = 350
	font.name = 'Times New Roman'

	al = xlwt.Alignment()
	al.horz = 0x02      
	al.vert = 0x01      

	color = xlwt.Borders.THIN
	borders = xlwt.Borders()
	borders.left = color
	borders.right = color
	borders.top = color
	borders.bottom = color


	style = xlwt.XFStyle()
	style.font = font
	style.alignment = al
	style.borders = borders

	return style

def getHeaderStyle(p):
	font = xlwt.Font()
	font.bold = True
	font.height = 220
	font.name="等线"

	al = xlwt.Alignment()
	al.horz = 0x02      
	al.vert = 0x01      

	borders = xlwt.Borders()
	if p == 'left':
		borders.left = xlwt.Borders.THIN
	elif p == 'right':
		borders.right = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN


	style = xlwt.XFStyle()
	style.font = font
	style.alignment = al
	style.borders = borders

	return style

def getLastStyle():
	borders = xlwt.Borders()
	borders.top = xlwt.Borders.THIN

	style = xlwt.XFStyle()
	style.borders = borders

	return style

def getCellStyle(p):
	font = xlwt.Font()
	font.name = "等线"
	font.height = 200

	al = xlwt.Alignment()
	al.horz = 0x02      
	al.vert = 0x01      

	borders = xlwt.Borders()
	if p == 'left':
		borders.left = xlwt.Borders.THIN
	elif p == 'right':
		borders.right = xlwt.Borders.THIN

	style = xlwt.XFStyle()
	style.font = font
	style.alignment = al
	style.borders = borders

	return style

topicStyle = getTopicStyle()
leftheaderStyle = getHeaderStyle('left')
rightheaderStyle = getHeaderStyle('right')
midheaderStyle = getHeaderStyle('mid')
leftcellStyle = getCellStyle("left")
rightcellStyle = getCellStyle("right")
midcellStyle = getCellStyle("mid")
lastStyle = getLastStyle()

def printRdr(filename, room_id, results):
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet('详单')

	worksheet.col(2).width = 256 * 25 
	worksheet.col(3).width = 256 * 25 
	worksheet.col(5).width = 256 * 19 
	worksheet.col(6).width = 256 * 19 

	if len(results) > 0:
		worksheet.write_merge(1, 2, 1, 6, "{}详单({}~{})".format(results[0]['room_id'], results[0]['start_time'], results[-1]['end_time']), topicStyle)
	else:
		worksheet.write_merge(1, 2, 1, 6, "{}详单".format(room_id), topicStyle)

	worksheet.write(3,1,"房间号",leftheaderStyle)
	worksheet.write(3,2,"开始时间",midheaderStyle)
	worksheet.write(3,3,"结束时间",midheaderStyle)
	worksheet.write(3,4,"风速",midheaderStyle)
	worksheet.write(3,5,"费率(元/分钟)",midheaderStyle)
	worksheet.write(3,6,"费用(元)",rightheaderStyle)

	idx = 4
	for r in results:
		if r['speed'] > 2 or r['speed'] < 0:
			sp = '中'
		else:
			sp = speed[r['speed']]
		worksheet.write(idx,1,r['room_id'],leftcellStyle)
		worksheet.write(idx,2,r['start_time'],midcellStyle)
		worksheet.write(idx,3,r['end_time'],midcellStyle)
		worksheet.write(idx,4,sp,midcellStyle)
		worksheet.write(idx,5,r['fee_rate'],midcellStyle)
		worksheet.write(idx,6,r['fee'],rightcellStyle)
		idx += 1

	for i in range(1,7):
		worksheet.write(idx,i,"",lastStyle)

	workbook.save("downloads/"+filename)
	return filename

def printInvoice(filename, room_id, result):
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet('账单')

	worksheet.col(2).width = 256 * 25 
	worksheet.col(3).width = 256 * 25 


	worksheet.write_merge(1, 2, 1, 4, "{}-账单".format(room_id), topicStyle)

	worksheet.write(3,1,"房间号",leftheaderStyle)
	worksheet.write(3,2,"入住时间",midheaderStyle)
	worksheet.write(3,3,"离店时间",midheaderStyle)
	worksheet.write(3,4,"费用(元)",rightheaderStyle)

	if len(result) > 0:
		worksheet.write(4,1,result['room_id'],   leftcellStyle)
		worksheet.write(4,2,result['check_in_time'], midcellStyle)
		worksheet.write(4,3,result['check_out_time'],midcellStyle)
		worksheet.write(4,4,result['fee'],      rightcellStyle)

	for i in range(1,5):
		worksheet.write(5,i,"",lastStyle)

	workbook.save("downloads/"+filename)
	return filename

def printReport(filename,room_id, rtype, result, begin_time=0, end_time=0):
	workbook = xlwt.Workbook()
	if rtype not in ['day', 'week', 'month', 'year']:
		rtype = 'other'
	worksheet = workbook.add_sheet(rtypes[rtype]+'报表')

	for i in range(2,9):
		worksheet.col(i).width = 256 * 20 
	#worksheet.col(3).width = 256 * 25 

	worksheet.write_merge(1,2,1,8,"{}-{}报表({}~{})".format(room_id,rtypes[rtype],begin_time,end_time), topicStyle)

	worksheet.write(3,1,"房间号",leftheaderStyle)
	worksheet.write(3,2,"服务时长(秒)",midheaderStyle)
	worksheet.write(3,3,"开关机次数",midheaderStyle)
	worksheet.write(3,4,"调度次数",midheaderStyle)
	worksheet.write(3,5,"详单数目",midheaderStyle)
	worksheet.write(3,6,"温度调节次数",midheaderStyle)
	worksheet.write(3,7,"风速调节次数",midheaderStyle)
	worksheet.write(3,8,"费用(元)",rightheaderStyle)

	if len(result) > 0:
		worksheet.write(4,1,result['room_id'],   leftcellStyle)
		worksheet.write(4,2,result['service_time'], midcellStyle)
		worksheet.write(4,3,result['on_off_times'],midcellStyle)
		worksheet.write(4,4,result['dispatch_times'],midcellStyle)
		worksheet.write(4,5,result['rdr_number'],midcellStyle)
		worksheet.write(4,6,result['change_temp_times'],midcellStyle)
		worksheet.write(4,7,result['change_speed_times'],midcellStyle)
		worksheet.write(4,8,result['fee'], rightcellStyle)

	for i in range(1,9):
		worksheet.write(5,i,"",lastStyle)

	workbook.save("downloads/"+filename)
	return filename

