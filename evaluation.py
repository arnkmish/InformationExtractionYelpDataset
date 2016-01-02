'''

This file does the evaluation of the accuracy of the charlotte hospitals extracted phrases.

'''

from pymongo import MongoClient
import operator
import time
import matplotlib.pyplot as py
import pylab
import nltk
from pattern.en import sentiment,positive
import math
import copy

if __name__ == '__main__':
	client = MongoClient()

	# Access the yelp_test database
	dBase = client.yelp_test

	charlotteHospitals = dBase.yelp_test_charlotte_hospitals

	charlotteHospitalReviews = dBase.yelp_test_charlotte_hospitals_reviews

	sortedCollection = dBase.sortedCollection

	tempDict = {};score = []

	sortedCollection.remove({})

	for item in charlotteHospitalReviews.find():
		string = str(item["date"])
		date = time.strptime(string, "%Y-%m-%d")
		tempDict[item["text"]] = date

	sortedIDs =  [k for k, v in sorted(tempDict.items(), key=lambda p: p[1], reverse=False)]
	
	chunkGram_pos = "POS: {<JJ> <NN>|<JJ> <NNS>|<NN> <NNS>}"
	chunkParser_pos = nltk.RegexpParser(chunkGram_pos)
	chunkGram_neg = "NEG: {<NNP> <NN|NNP>|<RB> <JJ>|<JJ> <NNS>|<NN> <NN>}"
	chunkParser_neg = nltk.RegexpParser(chunkGram_neg)
	
	for item in sortedIDs:
		for i in charlotteHospitalReviews.find():
			if item == i["text"]:
				sortedCollection.insert(i)
	keyCount = 0;reviewHash = {}
	for item in sortedCollection.find():
		keyCount = keyCount + 1
		reviewHash[keyCount] = item["text"]
	
	count_pos_sent =0
	for key,value in reviewHash.iteritems():
		final_score = 3.0
		count_pos = 0;count_neg = 0;total_count = 0
		review = value;phrase = ""
		if positive(value,0.1) == True:count_pos_sent += 1
		words = nltk.word_tokenize(review)
		tagged = nltk.pos_tag(words)
		try:					
			chunked = chunkParser_pos.parse(tagged)
			for subtree in chunked.subtrees():
				if subtree.label() == 'POS':
					phrase = ""
					(terms, tags) = zip(*subtree)
					for i in range(0,len(terms)):
						phrase = phrase + " " + terms[i]
					if positive(phrase.strip(),0.1) == True:count_pos += 1;total_count += 1
			chunked = chunkParser_neg.parse(tagged)
			for subtree in chunked.subtrees():
				if subtree.label() == 'NEG':
					phrase = ""
					(terms, tags) = zip(*subtree)
					for i in range(0,len(terms)):
						phrase = phrase + " " + terms[i]
					if positive(phrase.strip(),0.1) == False:count_neg += 1;total_count += 1
		except Exception as e:pass
		if count_pos == 0 and count_neg == 0:
			final_score = 3.0
		elif count_pos == 0:
			final_score = 2.0
		elif count_neg == 0:
			final_score = 4.0
		else:final_score = math.ceil(float(float(count_pos)/float(total_count))*5.0)
		score.append(final_score)	
	
	ratings = copy.copy(score)
	count = 0
	correct_count = 0
	count = sortedCollection.count()
	#Error calculation
	sentiment_rating = float(float(count_pos_sent)/float(count)*5)
	error = float(math.fabs(3.84 - sentiment_rating)/3.84)
	for item in sortedCollection.find():
		score_cur = score.pop()
		if math.fabs(float(item["stars"] - score_cur)) <= math.ceil(error+1):correct_count += 1
	
	print "Average Sentiment Rating = ",sentiment_rating
	print "Error percentage = ",float(error*100)
	print "Accuracy = ",float(float(float(correct_count)/float(count))*100)