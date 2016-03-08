## Setup

### Plot.py Setup

You need to sign up for a free [Plot.ly](http://plot.ly) account. Set the following environment variables:

    PLOTLY_USERNAME=<username>
    PLOTLY_API_KEY=<key>

## Running

### Plot the Input Data

    python plot.py <filepath> --name=<title>

### Run Input Data Through a NuPIC Model

    python run_prediction.py <filepath>

This will write an output file into the `out/` folder with the same name as the input file.

### Plot the Predictions and Input Data

    python plot.py <filepath> --name=<title>


## Example

#### Plot the input data file

    python plot.py data/nyc_taxi.csv --title="NYC Taxi Rides"

<div>
    <a href="https://plot.ly/~rhyolight/209/" target="_blank" title="NYC Taxi Rides" style="display: block; text-align: center;"><img src="https://plot.ly/~rhyolight/209.png" alt="NYC Taxi Rides" style="max-width: 100%;width: 1000px;"  width="1000" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="rhyolight:209"  src="https://plot.ly/embed.js" async></script>
</div>

#### Run the NuPIC model

    python run_prediction.py data/nyc_taxi.csv

#### Plot the Predictions

    python plot.py out/nyc_taxi.csv --title="NYC Taxi Ride Predictions"

<div>
    <a href="https://plot.ly/~rhyolight/211/" target="_blank" title="NYC Taxi Ride Predictions" style="display: block; text-align: center;"><img src="https://plot.ly/~rhyolight/211.png" alt="NYC Taxi Ride Predictions" style="max-width: 100%;width: 1000px;"  width="1000" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="rhyolight:211"  src="https://plot.ly/embed.js" async></script>
</div>
