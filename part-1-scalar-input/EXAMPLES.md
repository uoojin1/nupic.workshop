## Examples

#### Plot the input data file

    python plot.py data/nyc_taxi.csv --title="NYC Taxi Rides"

<div>
    <a href="https://plot.ly/~rhyolight/209/" target="_blank" title="NYC Taxi Rides" style="display: block; text-align: center;"><img src="https://plot.ly/~rhyolight/209.png" alt="NYC Taxi Rides" style="max-width: 100%;width: 1000px;"  width="1000" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="rhyolight:209"  src="https://plot.ly/embed.js" async></script>
</div>

#### Run a NuPIC model for predictions

    python run_prediction.py data/nyc_taxi.csv

#### Plot the Predictions

    python plot.py out/prediction_nyc_taxi.csv --title="NYC Taxi Ride Predictions"

<div>
    <a href="https://plot.ly/~rhyolight/211/" target="_blank" title="NYC Taxi Ride Predictions" style="display: block; text-align: center;"><img src="https://plot.ly/~rhyolight/211.png" alt="NYC Taxi Ride Predictions" style="max-width: 100%;width: 1000px;"  width="1000" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="rhyolight:211"  src="https://plot.ly/embed.js" async></script>
</div>

#### Run a NuPIC model for anomalies

    python run_anomaly.py data/nyc_taxi.csv

#### Plot the Anomalies

    python plot.py out/anomaly_nyc_taxi.csv --title="NYC Taxi Ride Anomalies"

<div>
    <a href="https://plot.ly/~rhyolight/261/" target="_blank" title="NYC Taxi Ride Anomalies" style="display: block; text-align: center;"><img src="https://plot.ly/~rhyolight/261.png" alt="NYC Taxi Ride Anomalies" style="max-width: 100%;width: 1000px;"  width="1000" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="rhyolight:261"  src="https://plot.ly/embed.js" async></script>
</div>
