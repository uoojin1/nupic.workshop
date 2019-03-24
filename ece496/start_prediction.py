import ntpath
import os
import time
import csv
import simplejson as json
import pandas as pd
from datetime import datetime as dt
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.algorithms import anomaly_likelihood
from nupic.data.inference_shifter import InferenceShifter
from htm.utils import getDataFrame, getMinMax, runDataThroughModel, convertToWritableOutput
from htm.args import parseArgs
from htm.query import getPromData
from htm.test import generateRandomUsageData
from htm.config import getCsvFile, DATE_FORMAT,MODEL_PARAMS_PATH



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
  resultOut = convertToWritableOutput(result, anomalyLikelihood)
  return resultOut
      
def getData(mode, container, part):
  """
  This function returns a tuple (timestamp, usage_value)
  If mode = prom, it queries the prometheus server for values based on container and part
  If mode = test (default), it simply generates random values for the ue 'container' and cpu 'part'
  """
  if mode == 'test':
    return generateRandomUsageData()
  else:
    return getPromData(container,part)
  


def main(options):
  # Create Prediction Model
  model = createPredictionModel()
  shifter = InferenceShifter()
  anomalyLikelihood = anomaly_likelihood.AnomalyLikelihood()
  
  # Append data to csv file
  csvFile = getCsvFile(options.mode, options.container,options.part)
  for i in range (0, 10000):
    with open(csvFile, mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        usage_data = generateRandomUsageData() # get prometheus data or generated data
        output = runDatapointThroughModel(model, usage_data, shifter, anomalyLikelihood)
        print(output)
        csv_writer.writerow([usage_data[0], output['prediction'], round(usage_data[1])])
        time.sleep(0.10)


if __name__ == "__main__":
  (options, args) = parseArgs()
  main(options)
