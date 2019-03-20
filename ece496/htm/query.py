import requests
from htm.config import PROM_USER,PROM_PASS


def getPromData(conatiner,part):
	#prime query
	
	#query prometheus server
	r = requests.get(url=queryUrl,params=queryParams,auth=(PROM_USER,PROM_PASS))
	data = r.json();

	#process data
	if part == "cpu":
		return processCpuData(container)
	elif part == "mem":
		return processMemData(data)
	else:
		return None,None

def getQuery(conatiner,part):
	qry = ""
	if part == "cpu":
		qry = "rate(container_cpu_usage_seconds{job='cadvisor',name='srsLTE_{0}'}[10m])/(container_spec_cpu_quota{job='cadvisor',name='srsLTE_base'} / container_spec_cpu_period{job='cadvisor',name='srsLTE_{0}'}) * 100".format(conatiner,)
	elif part = "mem":
		qry = "container_memory_usage_bytes{job='cadvisor',name='srsLTE_{0}'}".format(container,)
	return qry

# function to process CPU data from prometheus server
def processCpuData(data):
	timeValue = None
	dataValue = None
	#Do something with data
	return timeValue,dataValue
	
# function to process Mem data from prometheus server
def processMemData(data):
	timeValue = None
	dataValue = None
	#Do something with data
	return timeValue,dataValue
