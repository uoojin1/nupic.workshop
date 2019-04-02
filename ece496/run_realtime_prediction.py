import ntpath
import os
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

OUTPUT_DIR = "out"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MODEL_PARAMS_PATH = "model_params/model_params.json"


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


def runDatapointThroughModel(model, data, shifter, anomalyLikelihood):
	timestamp = dt.strptime(data[0], DATE_FORMAT)
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


def main(inputPath):
	model = createPredictionModel()
	ts = time.time()
	shifter = InferenceShifter()
	anomalyLikelihood = anomaly_likelihood.AnomalyLikelihood()
	for i in range (0, 10000):
		with open('./out/realtime_prediction.csv', mode='a') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',')
			cpu_usage_data = generateSemiRandomCPUUsage(ts, i)
			output = runDatapointThroughModel(model, cpu_usage_data, shifter, anomalyLikelihood)
			print(output)
			squared_error = 0
			if output['prediction']:
				squared_error = (float(output['prediction']/100) - round(cpu_usage_data[1])/100) ** 2
			# print("MSE!!! : ", squared_error)
			csv_writer.writerow([cpu_usage_data[0], output['prediction'], round(cpu_usage_data[1]), squared_error])
			time.sleep(0.1)


if __name__ == "__main__":
	main(sys.argv[1:])