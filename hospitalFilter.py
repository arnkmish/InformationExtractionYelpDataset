import re
import json
from pymongo import MongoClient
from pattern.en import positive

def decode_json(line):
	try:
		return json.loads(line)
	except:
		return None

with open("yelp_academic_dataset_business.json") as f:
	yelp_data_business = [decode_json(line) for line in f]
# The following two lines are giving me memory error while decoding the review json file
#with open("yelp_academic_dataset_review.json") as g:
#	yelp_data_review = [decode_json(line) for line in g]


if __name__ == '__main__':
	client = MongoClient()

	dBase = client.yelp_test

	business = dBase.yelp_test_business

	# To clear the business collection for not printing old values
	business.remove({})

	# Populate the business collection
	for item in yelp_data_business:
		business.insert(item)

	
	# CREATE SEPARATE COLLECTIONS FOR EACH BUSINESS CATEGORY TO BE EXAMINED

	# For hospitals create new collection
	hospital = dBase.yelp_test_hospitals

	# get rid of the old documents from the collection
	hospital.remove({})

	# populate the newly created empty collection
	for item in business.find({"categories": "Hospitals"}):
		hospital.insert(item)

	# print hospital counts
	print "The total number of documents inside hospital collection: "
	print hospital.count()
	print "Total number of distinct documents inside hospital collection: "
	print len(hospital.distinct("business_id"))

	for item in hospital.find():
		print item
