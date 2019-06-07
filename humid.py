#!/usr/bin/python
import airdata,os,time,sys
import numpy
airdata_inst = airdata.Energy()
extract = float(sys.argv[1])
def get_humidity():
		global airdata_inst,extract
                day = 60*24
                templist = []
                data = os.popen("tail -n "+str(int(day))+" ./RAM/data.log")
		try:
			sunrise = int(os.popen ("./forcast.py sun").readlines()[0].split(":")[0])
		except: sunrise = 6
                for each in data.readlines():
                         tmp = each.split(":")
			 try:
				 if time.localtime(float(tmp[0]))[3] >=sunrise-1 and time.localtime(float(tmp[0]))[3] <= sunrise+1 and float(tmp[0])>time.time()-(day*60):
	                         	#if float(tmp[0])<time.time()-(24*3600):
					templist.append (float(tmp[5]))
				 else:
					#print time.localtime(float(tmp[0]))[3]
				 	pass
			 except: print "error"
		#print templist
                inlet_min = numpy.average(templist)
		airdata_inst.vapor_max(extract)
		bottom = airdata_inst.pw
		airdata_inst.vapor_max(inlet_min)
		top = airdata_inst.pw
		# adjustmet to closer match RHwmo below zero saturations
		if inlet_min < 0:
			top  = airdata_inst.pw + bottom*(float(inlet_min*-0.9)/100)

		print top/bottom*100, inlet_min

#input : indoor temp
#output: relative humidity as expressed by indoortemp last 24hrs min temp

try:
	get_humidity()
except: print -1, -1
##############
