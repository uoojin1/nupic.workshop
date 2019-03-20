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
from datetime import datetime

import pandas as pd
from nupic.algorithms import anomaly_likelihood
from nupic.data.inference_shifter import InferenceShifter


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def getDataFrame(dataFilePath):
  return pd.read_csv(dataFilePath, skiprows=3, names=["timestamp", "value"])


def getMinMax(dataFrame):
  return dataFrame.min().values[1], dataFrame.max().values[1]


def convertToWritableOutput(result, anomalyLikelihood):
  timestamp = result.rawInput["timestamp"]
  value = result.rawInput["value"]
  inferences = result.inferences
  output = {
    "timestamp": timestamp,
    "value": value,
    "prediction": inferences["multiStepBestPredictions"][1]
  }
  # If there are anomaly scores in the result, extract them, too.
  if "anomalyScore" in inferences and inferences["anomalyScore"] is not None:
    anomalyScore = inferences["anomalyScore"]
    output["anomalyScore"] = anomalyScore
    likelihood = anomalyLikelihood.anomalyProbability(
      value, anomalyScore, timestamp)
    logAnomalyLikelihood = anomalyLikelihood.computeLogLikelihood(anomalyScore)
    output["logAnomalyLikelihood"] = logAnomalyLikelihood
    output["anomalyLikelihood"] = likelihood
  return output


def runDataThroughModel(model, dataFrame):
  shifter = InferenceShifter()
  anomalyLikelihood = anomaly_likelihood.AnomalyLikelihood()
  print("anomalyLikelihood")
  print(anomalyLikelihood)
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
    resultOut = convertToWritableOutput(result, anomalyLikelihood)
    out.append(resultOut)

  return pd.DataFrame(out)
