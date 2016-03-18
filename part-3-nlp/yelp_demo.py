#!/usr/bin/env python
"""
Script to run a Cortical.io NLP demo w/ the Yelp Challenge text data
(yelp.com/dataset_challenge). This is a classification example, where categories
are defined by the star ratings (1-5) of Yelp reviews.

Requires retinasdk w/ API key (github.com/cortical-io/retina-sdk.py).
"""
from collections import defaultdict
import numpy
import os
import random
import retinasdk
import simplejson as json
from textwrap import TextWrapper


wrapper = TextWrapper(width=80)
_DATA_PATH = "data/reviews.json"


def classifyText(text, categoryFingerprints, client):
  # The lite client uses the cosine similarity distance metric
  cosSims = numpy.ones(len(categoryFingerprints))
  for cat, fingerprint in categoryFingerprints.iteritems():
    cosSims[int(cat)-1] = client.compare(client.getFingerprint(text),
                                       fingerprint.positions)
  catRanks = numpy.argsort(cosSims)[::-1]
  print wrapper.fill("{} --> {} stars".format(text, catRanks[0]+1))
  return catRanks


def setupCio():
  """ Setup Cortical.io clients."""
  apiKey = os.environ.get("CORTICAL_API_KEY")
  cioFullClient = retinasdk.FullClient(apiKey)
  cioLiteClient = retinasdk.LiteClient(apiKey)
  return cioFullClient, cioLiteClient


def createCategories(client, categorySize=1000):
  print "Reading in Yelp data."
  starCategories = defaultdict(list)
  with open(_DATA_PATH, "rb") as fin:
    for i, line in enumerate(fin):
      entry = json.loads(line)
      starCategories[entry["stars"]].append(entry["text"])

  print "Creating categories, each with random selection of {} entries.".format(
    categorySize)
  starFingerprints = {}
  for stars, entries in starCategories.iteritems():
    starFingerprints[stars] = client.createCategoryFilter(
      "{}".format(stars),
      positiveExamples=random.sample(entries, categorySize),
      negativeExamples=[])

  return starFingerprints



if __name__ == "__main__":

  cioFullClient, cioLiteClient = setupCio()
  categoryFingerprints = createCategories(cioFullClient)

  print
  print "Now let's try to classify some reviews (quit with 'q')..."
  while True:
    userInput = raw_input("Enter a review: ")
    if userInput == "q":
      break
    classifyText(userInput, categoryFingerprints, cioLiteClient)

  print
  print "Categorize some fake reviews..."
  tests = [
    "Ugh, no all you can eat salad and breadsticks... No gluten sensitive menu... Take me back to Olive Garden now!",
    "The pizza is terribly delicious , these people cook the pasta so bad I come back twice a week. The specials are under priced and i hate saving money and getting my money's worth. I hate getting such great food.",
    "I have no words for how horrible this place is. Apart from the food and service, I don't recommend it.",
    "Who the hell does not allow people to do half and half toppings. What a joke. I guess i will just get delicious meat all over my pizza and my silly vegeterian girlfriend cannot have any of my pizza. Perfect!",
    "Do not order from here, they don't deliver to where I live. Sure, I live in Omaha, but still..."
  ]
  for test in tests:
    classifyText(test, categoryFingerprints, cioLiteClient)
    print
