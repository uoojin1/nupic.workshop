## Setup

### NuPIC

You must have NuPIC installed. See <https://github.com/numenta/nupic> for instructions.

### Plot.ly Setup

You need to sign up for a free [Plot.ly](http://plot.ly) account. Set the following environment variables:

    PLOTLY_USERNAME=<username>
    PLOTLY_API_KEY=<key>

## Running

You can run the scripts below on any of the data files found in the [`data`](data) directory. You can plot either the input data or the data output from NuPIC, which also contains a copy of the input data.

### Plot the Input Data

    python plot.py <path-to-input-file> --name=<title>

### Run Input Data Through a NuPIC *Prediction* Model

This script will create a new NuPIC model that predicts the next value in the data. This is a one-step-ahead prediction.

    python run_prediction.py <path-to-input-file>

This will write an output file to `out/prediction_<input-file-name>.csv`.

### Plot the Predictions and Input Data

    python plot.py <path-to-prediction> --name=<title>

### Run Input Data Through a NuPIC *Anomaly* Model

This script will create a new NuPIC model that returns information about how anomalous the data is at each point in time. 

    python run_anomaly.py <path-to-input-file>

This will write an output file to `out/anomaly_<input-file-name>.csv`.

### Plot the Anomaly Likelihoods

    python plot.py <path-to-anomaly-output> --name=<title> [--log]

By default, this will plot the anomaly likelihood, not the anomaly score. To find out the difference, [check this out](https://www.youtube.com/watch?v=nVCKjZWYavM). 

The optional `--log` will plot the the anomaly likelihood logarithmically.
 
# [Examples](EXAMPLES.md)
