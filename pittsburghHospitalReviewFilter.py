'''

This file filters reviews that correspond to Pittsburgh hospitals, and stores them in a new collection.

'''
import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the hospital reviews collection
	hospitalReviews = dBase.yelp_test_hospital_reviews

	# Access the hospitals that are there in Pittsburgh
	pittsburghHospitals = dBase.yelp_test_pittsburgh_hospitals

	# Create a new collection for storing the Pittsburgh hospital reviews
	pittsburghHospitalReviews = dBase.yelp_test_pittsburgh_hospitals_reviews

	# Clean old entries
	pittsburghHospitalReviews.remove({})

	# Filter the reviews
	for item in hospitalReviews.find():
		if pittsburghHospitals.find_one({"business_id": item["business_id"]}) != None:
			pittsburghHospitalReviews.insert(item)

	# Print some stats for the newly built collection
	print "The distinct number of businesses for which the reviews have been filtered is: "
	print len(pittsburghHospitalReviews.distinct("business_id"))
	print "The total number of reviews filtered for Pittsburgh hospitals: "	
	print pittsburghHospitalReviews.count()