'''

This file filters the hospital reviews that only correspond to Madison

'''
import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the collection that contains only the hospital reviews
	hospitalReviews = dBase.yelp_test_hospital_reviews

	# Access the collection that has only the hospitals from Madison
	madisonHospitals = dBase.yelp_test_madison_hospitals

	# Create a new collection that stores the Madison hospital reviews
	madisonHospitalReviews = dBase.yelp_test_madison_hospitals_reviews

	# Clean old entries 
	madisonHospitalReviews.remove({})

	# Filter reviews
	for item in hospitalReviews.find():
		if madisonHospitals.find_one({"business_id": item["business_id"]}) != None:
			madisonHospitalReviews.insert(item)

	# Print some stats for the newly built collection
	print "The distinct number of businesses for which the reviews have been filtered is: "
	print len(madisonHospitalReviews.distinct("business_id"))
	print "The total number of reviews filtered for Madison hospitals: "	
	print madisonHospitalReviews.count()