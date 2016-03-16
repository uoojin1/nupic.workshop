## Natural Language Processing with Cortical.io API

This is an example of using Cortical.io to encode text data from Yelp reviews into SDRs for classification. The API has many capabilities, [check them out here](http://www.cortical.io/demos.html).

### Setup

#### Cortical.io API
You must have a [free API key](http://www.cortical.io/resources_apikey.html) and set it as the environment variable `CORTICAL_API_KEY`.

#### Python Requirements

To install required python modules:

    pip install -r requirements.txt [--user]

#### Yelp Data
The reviews portion of the [Yelp Challenge Dataset](https://www.yelp.com/dataset_challenge) is used for this classification example. Get the data from the link and 

	cp <path to yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json> \
	data/reviews.json


## Running

	python yelp_demo.py

