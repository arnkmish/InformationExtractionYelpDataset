'''

This file filters hospitals that are from the city Charlotte, so that further steps of text analysis can be done on the reiews on those hospitals.

'''
import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the yelp_test_hospitals collection, that was built running the hospitalFilter.py file
	hospitals = dBase.yelp_test_hospitals

	# Create a new collection to store only the Charlotte hospitals
	charlotteHospitals = dBase.yelp_test_charlotte_hospitals

	# Clear the old records in the collection
	charlotteHospitals.remove({})

	# Filter city-wise
	for item in hospitals.find({"city": "Charlotte"}):
		charlotteHospitals.insert(item)

	# Print some stats about the newly built collection
	print "The distinct number of Charlotte hospitals"
	print len(charlotteHospitals.distinct("business_id"))
	print "The total number entries in charlotteHospitals collection: "	
	print charlotteHospitals.count()