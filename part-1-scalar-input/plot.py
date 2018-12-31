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
from nupic_workshop.plotter import PlotlyPlotter
from nupic_workshop.args import parseArgs


# if __name__ == "__main__":
#   (options, args) = parseArgs()
#   PlotlyPlotter(
#     dataFile=args[0],
#     dataName=options.title
#   ).plotRawData(useLog=options.log)

import plotly.plotly as py
py.sign_in('uoojin95', 'c7d7iZxsvnTPUs5GYxva')
import plotly.graph_objs as go
import plotly.figure_factory as ff

import numpy as np
import pandas as pd

if __name__ == "__main__":
  (options, args) = parseArgs()
  df = pd.read_csv(args[0])
  # data_table = ff.create_table(df.head())
  # py.plot(data_table, filename='hiroo')

  prediction = go.Scatter(
    x=df['timestamp'], y=df['prediction'],
    mode='lines', name='prediction'
  )
  real = go.Scatter(
    x=df['timestamp'], y=df['value'],
    mode='lines', name='realvalue'
  )

  layout = go.Layout(title='prediction plot from csv data',
    plot_bgcolor='rgb(230,230,230)')
  
  fig = go.Figure(data=[prediction, real], layout=layout)

  py.plot(fig, filename='prediction_graph')