'''

This file loads the review json file and filters out the reviews corresponding only to those businesses that have 'Hosptal' in their category list. Here the collections built by running reviewCollectionBuilder.py and hospitalFilter.py are used.

'''
import json
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the yelp_test_review collection that was built using the reviewCollectionBuilder.py file
	reviews = dBase.yelp_test_review

	# Access the yelp_test_hospitals collection that was built using the hospitalFilter.py file
	hospitals = dBase.yelp_test_hospitals

	# Create a new collection to store the filtered hospital reviews
	hospitalReviews = dBase.yelp_test_hospital_reviews

	hospitalReviews.remove({})

	for item in reviews.find():
		if hospitals.find_one({"business_id": item["business_id"]}) != None:
			hospitalReviews.insert(item)

	# Print some stats about the newly built collection
	print "The distinct number of businesses for which the reviews have been filtered is: "
	print len(hospitalReviews.distinct("business_id"))
	print "The total number of reviews filtered for hospitals: "	
	print hospitalReviews.count()