# ----------------------------------------------------------------------
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import os
import ntpath
from datetime import datetime

import simplejson as json
import pandas as pd

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.data.inference_shifter import InferenceShifter

from nupic_workshop.args import parseArgs


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
OUTPUT_DIR = "out"
MODEL_PARAMS_PATH = "model_params/model_params.json"


def getDataFrame(dataFilePath):
  return pd.read_csv(dataFilePath, skiprows=3, names=["timestamp", "value"])


def getMinMax(dataFrame):
  return dataFrame.min().values[1], dataFrame.max().values[1]


def createModel(dataFrame):
  with open(MODEL_PARAMS_PATH, "r") as dataIn:
    modelParams = json.loads(dataIn.read())
  minInput, maxInput = getMinMax(dataFrame)

  # RDSE - resolution calculation
  valueEncoderParams = \
    modelParams["modelParams"]["sensorParams"]["encoders"]["value"]
  numBuckets = float(valueEncoderParams.pop("numBuckets"))
  resolution = max(0.001, (maxInput - minInput) / numBuckets)
  valueEncoderParams["resolution"] = resolution

  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "value"})
  return model


def runDataThroughModel(model, dataFrame):
  shifter = InferenceShifter()
  out = []
  for index, row in dataFrame.iterrows():
    timestamp = datetime.strptime(row["timestamp"], DATE_FORMAT)
    value = int(row["value"])
    result = model.run({
      "timestamp": timestamp,
      "value": value
    })
    if index % 100 == 0:
      print "Read %i lines..." % index
    result = shifter.shift(result)
    out.append({
      "timestamp": timestamp,
      "value": value,
      "prediction": result.inferences["multiStepBestPredictions"][1]
    })
  return pd.DataFrame(out)


def main(inputPath):
  inputFileName = ntpath.basename(inputPath)
  dataFrame = getDataFrame(inputPath)
  model = createModel(dataFrame)
  outputFrame = runDataThroughModel(model, dataFrame)
  if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
  outputFrame.to_csv(os.path.join(OUTPUT_DIR, inputFileName), index=False)


if __name__ == "__main__":
  (options, args) = parseArgs()
  dataPath = args[0]
  main(dataPath)
