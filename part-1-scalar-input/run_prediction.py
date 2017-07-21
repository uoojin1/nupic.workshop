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
import ntpath
import os
import simplejson as json
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic_workshop.utils import getDataFrame, getMinMax, runDataThroughModel
from nupic_workshop.args import parseArgs

OUTPUT_DIR = "out"
MODEL_PARAMS_PATH = "model_params/model_params.json"


def createPredictionModel(dataFrame):
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


def main(inputPath):
  inputFileName = ntpath.basename(inputPath)
  dataFrame = getDataFrame(inputPath)
  model = createPredictionModel(dataFrame)
  outputFrame = runDataThroughModel(model, dataFrame)
  if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
  outputFrame.to_csv(
    os.path.join(OUTPUT_DIR, "prediction_" + inputFileName),
    index=False
  )


if __name__ == "__main__":
  (options, args) = parseArgs()
  dataPath = args[0]
  main(dataPath)
