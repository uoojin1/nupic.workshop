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
"""
Helper class for Plot.py plots of input data, NuPIC predictions, and NuPIC
anomaly likelihoods. Some of this is customized for NuPIC data.
"""
import os
import pandas as pd
import plotly.plotly as py

from plotly.graph_objs import (
    Data, Figure, Layout, Line, Bar, Marker, Scatter, XAxis, YAxis)

try:
  import simplejson as json
except ImportError:
  import json


def getCSVData(dataPath):
  try:
    data = pd.read_csv(dataPath)
  except IOError("Invalid path to data file."):
    return
  return data



class PlotlyPlotter(object):
  """Plot NAB data and results files with the plotly API."""

  def __init__(self,
               apiKey=None,
               username=None,
               dataFile=None,
               dataName=""):

    # Instantiate API credentials.
    try:
      self.apiKey = apiKey if apiKey else os.environ["PLOTLY_API_KEY"]
    except:
      print ("Missing PLOTLY_API_KEY environment variable. If you have a "
        "key, set it with $ export PLOTLY_API_KEY=api_key\n"
        "You can retrieve a key by registering for the Plotly API at "
        "http://www.plot.ly")
      raise OSError("Missing API key.")
    try:
      self.username = username if username else os.environ["PLOTLY_USERNAME"]
    except:
      print ("Missing PLOTLY_USERNAME environment variable. If you have a "
        "username, set it with $ export PLOTLY_USERNAME=username\n"
        "You can sign up for the Plotly API at http://www.plot.ly")
      raise OSError("Missing username.")

    py.sign_in(self.username, self.apiKey)

    # Setup data
    self.dataFile = dataFile
    self.dataName = dataName if dataName else dataFile
    self.dataPath = os.path.join(os.getcwd(), dataFile)
    self.rawData = getCSVData(self.dataPath) if self.dataPath else None

    # For open shape markers, append "-open" to strings below:
    self.markers = ["circle", "diamond", "square", "cross", "triangle-up",
                    "hexagon", "triangle-down"]


  def _addValues(self, name=None, title=None):
    """Return data values trace."""
    if name is None:
      name = "value"
    if title is None:
      title = "Value"
    return Scatter(x=self.rawData["timestamp"],
                   y=self.rawData[name],
                   name=title,
                   line=Line(
                     width=1.5
                   ),
                   yaxis="y1",
                   showlegend=False)


  def _addAnomalyScores(self, useLog):
    yName = "anomalyLikelihood"
    yTitle = "Anomaly Likelihood"
    if useLog:
      yName = "logAnomalyLikelihood"
      yTitle = "Log(Anomaly Likelihood)"
    return Bar(x=self.rawData["timestamp"],
               y=self.rawData[yName],
               name=yTitle,
               yaxis="y2",
               opacity=0.5)


  def _hasPredictions(self):
    return "prediction" in self.rawData


  def _hasAnomalyScores(self):
    return "anomalyLikelihood" in self.rawData


  @staticmethod
  def _createLayout(title):
    """Return plotly Layout object."""
    return Layout(title=title,
                  showlegend=False,
                  width=1000,
                  height=600,
                  xaxis=XAxis(
                    title="Date"
                  ),
                  yaxis=YAxis(
                    title="Metric",
                    domain=[0, 1],
                    autorange=True,
                    autotick=True
                  ),
                  yaxis2=YAxis(
                    overlaying="y",
                    side="right"
                  ),
                  barmode="stack",
                  bargap=0)


  def plotRawData(self, useLog=False):
    """Plot the data stream."""

    if self.rawData is None:
      self.rawData = getCSVData(self.dataPath)

    traces = []

    if self._hasAnomalyScores():
      traces.append(self._addAnomalyScores(useLog))

    traces.append(self._addValues())

    if self._hasPredictions() and not self._hasAnomalyScores():
      traces.append(self._addValues(name="prediction", title="Prediction"))

    # Create plotly Data and Layout objects:
    data = Data(traces)
    layout = self._createLayout(self.dataName)

    # Query plotly
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)
    print "Data plot URL: ", plot_url

    return plot_url
