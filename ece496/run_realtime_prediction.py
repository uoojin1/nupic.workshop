import ntpath
import os, math
import simplejson as json
from nupic.frameworks.opf.model_factory import ModelFactory
from htm.utils import getDataFrame, getMinMax, convertToWritableOutput
import datetime
from datetime import datetime as dt
import random
import pandas as pd
from nupic.algorithms import anomaly_likelihood
from nupic.data.inference_shifter import InferenceShifter
import time
import csv
import sys
# for plotting
import numpy as np
import matplotlib.pyplot as plt
# for prometheus
import requests

first_container = 'http://142.150.208.216:9090/api/v1/query?query='

query_parameter = '(sum by (name) (rate(container_cpu_usage_seconds_total{job="cadvisor",name="test-container-cpu-ram-stress-scale"}[30s])*100))/7'

cpu_query = 'http://142.150.208.216:9090/api/v1/query?query=(sum%20(rate%20(container_cpu_usage_seconds_total{job=%22cadvisor%22,name=%22test-container-cpu-ram-stress-scale%22}[1m]))%20/%20(sum%20(machine_cpu_cores)))*100'

CPU_QUERY = cpu_query #first_container + query_parameter


overall = '(sum(rate(container_cpu_usage_seconds_total{job="cadvisor",name="test-container-cpu-ram-stress-scale"}[1m]))/(sum(machine_cpu_cores)))'
final_cpu_query =  first_container + overall

limit = 'sum(container_spec_cpu_quota{name="test-container-cpu-ram-stress-scale"}/container_spec_cpu_period{name="test-container-cpu-ram-stress-scale"})'
final_limit_query = first_container + limit


OUTPUT_DIR = "out"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MODEL_PARAMS_PATH = "model_params/model_params.json"
SCALE_PERIOD = 3
TARGETED_USAGE = 75 #in percentage
MIN_USAGE = 25 # in percentage


def createPredictionModel():
	with open(MODEL_PARAMS_PATH, "r") as dataIn:
		modelParams = json.loads(dataIn.read())
	minInput = 0
	maxInput = 100
	valueEncoderParams = \
		modelParams["modelParams"]["sensorParams"]["encoders"]["value"]
	numBuckets = float(valueEncoderParams.pop("numBuckets"))
	resolution = max(0.001, (maxInput - minInput) / numBuckets) # 301.45
	valueEncoderParams["resolution"] = resolution
	model = ModelFactory.create(modelParams)
	model.enableInference({"predictedField": "value"})
	return model

def callPrometheus(ts, i):
	timestamp = datetime.datetime.fromtimestamp(ts + i*3600).strftime('%Y-%m-%d %H:%M:%S')

	query = cpu_query #final_cpu_query
	r = requests.get(query, auth=('admin', 'admin'))
	requestJson = r.json()
	if requestJson['data']['result']:
		u_value = requestJson['data']['result'][0]['value']
		print "CPU: ", u_value[1]
		return timestamp, float(u_value[1])
	else:
		print "CPU: NO RESULT"
		return timestamp, 0


def runDatapointThroughModel(model, data, shifter, anomalyLikelihood):
	timestamp = dt.strptime(data[0], DATE_FORMAT)
	#print "data[0]", data[0]
	value = int(data[1])
	prediction = model.run({
		"timestamp": timestamp,
		"value": value
	})
	result = shifter.shift(prediction)

	with open('./out/encoding0.csv', mode='a') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=' ')
		csv_writer.writerow(result.sensorInput.dataEncodings[0])
	with open('./out/encoding1.csv', mode='a') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=' ')
		csv_writer.writerow(result.sensorInput.dataEncodings[1])
	with open('./out/encoding2.csv', mode='a') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=' ')
		csv_writer.writerow(result.sensorInput.dataEncodings[2])
	with open('./out/encoding3.csv', mode='a') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=' ')
		csv_writer.writerow(result.sensorInput.dataEncodings[3])

	resultOut = convertToWritableOutput(result, anomalyLikelihood)
	# print "result out?", resultOut
	return resultOut


def generateSemiRandomCPUUsage(ts, i):
	timestamp = datetime.datetime.fromtimestamp(ts + i*3600).strftime('%Y-%m-%d %H:%M:%S')
	hr = datetime.datetime.fromtimestamp(ts + i*3600).hour
	weekday = datetime.datetime.fromtimestamp(ts + i*3600).weekday()
	cpu_usage = random.gauss(50,2)
	if hr >= 16 and hr <= 20:
			cpu_usage *= random.randrange(3,4)/3
	cpu_usage /= (7-weekday)
	return timestamp, cpu_usage

def calculate_buffer(current_usage, predicted_usage,mse):
	mse = mse if mse != 0 else 1
	# from [current_usage - (predicted_usage + added_amt)] ** 2 = mse
	added_amt = abs((current_usage - math.sqrt(mse)) - predicted_usage)
	buffered_value  = (100.0/75.0) * (predicted_usage + added_amt)
	# print "buffer_value", buffered_value
	buffered_value = (MIN_USAGE + buffered_value) if buffered_value < current_usage else buffered_value
	buffered_value = MIN_USAGE if buffered_value < MIN_USAGE else buffered_value
	return buffered_value

def scale(cpu_share, container_name):
	#print 'docker update --cpu-shares ' + str(cpu_share) + ' ' + container_name
	#os.system('docker update --cpu-shares ' + str(cpu_share) + ' ' + container_name)
	print "######CPUS: ", cpu_share
	if (cpu_share < 0.1 or cpu_share > 5):
		print "cpu out of bound"
		return
	os.system('docker update --cpus="' + str(cpu_share) + '" ' + container_name)
	print 'docker update --cpus="' + str(cpu_share) + '" ' + container_name 

def main(inputPath):
	model = createPredictionModel()
	ts = time.time()
	shifter = InferenceShifter()
	anomalyLikelihood = anomaly_likelihood.AnomalyLikelihood()

	cpus = 1

	#scaling parameters
	squared_error_sum = 0
	prev_prediction = 0
	cur_period = 1
	buffered_prediction = 0
	for i in range (0, 10000):
		with open('./out/realtime_prediction.csv', mode='a') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',')
			# cpu_usage_data = generateSemiRandomCPUUsage(ts, i)
			cpu_usage_data = callPrometheus(ts, i)
			print "\n\n--------- cpu_usage_data", cpu_usage_data
			output = runDatapointThroughModel(model, cpu_usage_data, shifter, anomalyLikelihood)
			squared_error = 0
			mse_value = 0
			if output['prediction']:
				squared_error = (prev_prediction - float(cpu_usage_data[1])) ** 2
				prev_prediction = float(output['prediction'])
				squared_error_sum += abs(squared_error)
				mse_value = squared_error_sum/float(i+1)
			if cur_period % SCALE_PERIOD == 0:
                		# reset period counter
                		cur_period = 1
                		# calculate buffered value
                		buffered_prediction = calculate_buffer(cpu_usage_data[1],output['prediction'], mse_value)
			else:
                		cur_period += 1
			#print "current_cpu_share", current_cpu_share
			print "buffered_prediction: ", buffered_prediction
			container_name = 'test-container-cpu-ram-stress-scale'
			if  round(buffered_prediction) > 30:
				#print "current_cpu_share", current_cpu_share
				if cpus >= 0.1:
					print  "cpus reducable"
					cpus -= 0.02
					scale(cpus, container_name)
					print "scale down"
			if round(buffered_prediction) < 3:
				if cpus <= 2:
					print "cpus increasable"
					cpus += 0.02
					scale(cpus, container_name)
					print "scale up"
			csv_writer.writerow([cpu_usage_data[0], output['prediction'], round(cpu_usage_data[1]), mse_value, buffered_prediction])
			# print "\ncpu_usage_data[0]: ", cpu_usage_data[0]
			# print "prediction: ", output['prediction']
			# print "round(cpu...): ", round(cpu_usage_data[1])
			# print "mse_value", mse_value
			# print "buffered_prediction", buffered_prediction
			time.sleep(8)


if __name__ == "__main__":
	main(sys.argv[1:])
