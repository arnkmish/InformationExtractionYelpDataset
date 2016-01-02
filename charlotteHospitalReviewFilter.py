'''

This file filters the reviews only for the hospitals that are in the city Charlotte.

'''
import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the yelp_test_hospital_reviews that was built by running the hospitalReviewFilter.py file
	hospitalReviews = dBase.yelp_test_hospital_reviews

	# Access the yelp_test_charlotte_hospitals that was built by running the charlotteHospitalFilter.py file
	charlotteHospitals = dBase.yelp_test_charlotte_hospitals

	# Create a new collection to store on the reviews that are for hospitals in the city Charlotte
	charlotteHospitalReviews = dBase.yelp_test_charlotte_hospitals_reviews

	charlotteHospitalReviews.remove({})

	# Filter the reviews
	for item in hospitalReviews.find():
		if charlotteHospitals.find_one({"business_id": item["business_id"]}) != None:
			charlotteHospitalReviews.insert(item)

	# Print some stats regarding the newly built collection
	print "The distinct number of businesses for which the reviews have been filtered is: "
	print len(charlotteHospitalReviews.distinct("business_id"))
	print "The total number of reviews filtered for Charlotte hospitals: "	
	print charlotteHospitalReviews.count()