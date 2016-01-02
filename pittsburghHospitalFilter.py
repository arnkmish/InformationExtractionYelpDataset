'''

This file filters the hospitals based on city Pittsburgh, and builds a new collection for storing only these hospitals.

'''

import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access yelp_test database
	dBase = client.yelp_test

	# Access the collection that has all the hospitals from the business json file
	hospitals = dBase.yelp_test_hospitals

	# Create a new collection for storing all the hospitals
	pittsburghHospitals = dBase.yelp_test_pittsburgh_hospitals

	# Clean old entries
	pittsburghHospitals.remove({})

	# Filter the hospitals
	for item in hospitals.find({"city": "Pittsburgh"}):
		pittsburghHospitals.insert(item)

	# Print some stats for the newly built collection
	print "The distinct number of Pittsburgh hospitals"
	print len(pittsburghHospitals.distinct("business_id"))
	print "The total number entries in pittsburghHospitals collection: "	
	print pittsburghHospitals.count()