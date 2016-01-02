'''
This file is used for loading the businesses in MongoDB collection, which is used for further filtering based on types of businesses.
'''
import json
from pymongo import MongoClient

# Load the json file
def decode_json(line):
	try:
		return json.loads(line)
	except:
		return None

with open("yelp_academic_dataset_business.json") as f:
	yelp_data_business = [decode_json(line) for line in f]


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

	# For Indian restaurants create collection
	indianRestaurant = dBase.yelp_test_indRes

	# Get rid of the old documents inside the collection
	indianRestaurant.remove({})
	
	# populate the newly created empty collection
	for item in business.find({"categories": "Indian"}):
		indianRestaurant.insert(item)

	# print indian counts
	print "Total number of documents inside indianRestaurant collection: "
	print indianRestaurant.count()
	print "Total number of distinct documents inside indianRestaurant collection: "
	print len(indianRestaurant.distinct("business_id"))
	for item in indianRestaurant.find():
		print item
	
	# For cafes create collection

	cafe = dBase.yelp_test_cafes

	# Get rid of the old documents inside the collection
	cafe.remove({})

	# populate the newly created empty collection
	for item in business.find({"categories": "Cafes"}):
		cafe.insert(item)

	# print cafe counts
	print "Total number of documents inside cafe collection: "
	print cafe.count()
	print "Total number of distinct documents inside cafe collection: "
	print len(cafe.distinct("business_id"))

	# For bars create new collection
	bar = dBase.yelp_test_bars

	# Get rid of the old documents from the collection
	bar.remove({})

	# populate the newly created empty collection
	for item in business.find({"categories": "Bars"}):
		bar.insert(item)

	# print bar counts
	print "Total number of documents inside bar collection: "
	print bar.count()
	print "Total number of distinct documents inside bar collection: "
	print len(bar.distinct("business_id"))

	# For gyms create new collection
	gym = dBase.yelp_test_gyms

	# get rid of the old documents from the collection
	gym.remove({})

	# populate the newly created empty collection
	for item in business.find({"categories": "Gyms"}):
		gym.insert(item)

	# print gym counts
	print "Total number of documents inside gym collection: "
	print gym.count()
	print "Total number of distinct documents inside gym collection: "
	print len(gym.distinct("business_id"))	

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