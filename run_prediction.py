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

import simplejson as json
import pandas as pd

from nupic.frameworks.opf.modelfactory import ModelFactory

from nupic_workshop.args import parseArgs

MODEL_PARAMS_PATH = "model_params/model_params.json"


def getMinMax(dataFilePath):
  df = pd.read_csv(dataFilePath, skiprows=3, names=["timestamp", "value"])
  return df.min().values[1], df.max().values[1]




def createModel(dataFile):
  with open(MODEL_PARAMS_PATH, "r") as dataIn:
    modelParams = json.loads(dataIn.read())
  minInput, maxInput = getMinMax(os.path.join("data", dataFile))

  # RDSE - resolution calculation
  valueEncoderParams = \
    modelParams["modelParams"]["sensorParams"]["encoders"]["value"]
  numBuckets = float(valueEncoderParams.pop("numBuckets"))
  resolution = max(0.001, (maxInput - minInput) / numBuckets)
  valueEncoderParams["resolution"] = resolution

  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "value"})
  return model


if __name__ == "__main__":
  (options, args) = parseArgs()
  model = createModel(options.dataFile)
