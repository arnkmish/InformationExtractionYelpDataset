'''

This file filters the businesses to store only the hospitals that are in Madison

'''
import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the collection that has all the hospitals
	hospitals = dBase.yelp_test_hospitals

	# Create a new collection to store the hospitals that are in Madison
	madisonHospitals = dBase.yelp_test_madison_hospitals

	# Clean old entries into the collection
	madisonHospitals.remove({})

	# Filter hospitals
	for item in hospitals.find({"city": "Madison"}):
		madisonHospitals.insert(item)

	# Print some statistics for the newly built collection
	print "The distinct number of Madison hospitals"
	print len(madisonHospitals.distinct("business_id"))
	print "The total number entries in madisonHospitals collection: "	
	print madisonHospitals.count()