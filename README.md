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

    python plot.py <filepath> --name=<title>

### Run Input Data Through a NuPIC *Prediction* Model

This script will create a new NuPIC model that predicts the next value in the data. This is a one-step-ahead prediction.

    python run_prediction.py <filepath>

This will write an output file into the `out/` folder with the same name as the input file.

### Plot the Predictions and Input Data

    python plot.py <filepath> --name=<title>

### Run Input Data Through a NuPIC *Anomaly* Model

This script will create a new NuPIC model that returns information about how anomalous the data is at each point in time. 

    python run_anomaly.py <filepath>

Beware that this will overwrite any output file you might have with the same name in the `out/` directory.

### Plot the Anomaly Likelihoods

    python plot.py <filepath> --name=<title> [--log]

By default, this will plot the anomaly likelihood, not the anomaly score. To find out the difference, [check this out](https://www.youtube.com/watch?v=nVCKjZWYavM). 

The optional `--log` will plot the the anomaly likelihood logarithmically.
 
# [Examples](EXAMPLES.md)
