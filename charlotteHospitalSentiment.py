'''

This file creates the positive and negative phrases corresponding to the reviews of hospitals that are in Charlotte. The ouput files are in CSV format, so that it can be used for vsualization with the help of Tableu software.

'''
import nltk
import nltk.corpus
from pymongo import MongoClient
from pattern.en import sentiment,positive
import itertools
from collections import defaultdict

if __name__ == '__main__':
	# The output files that are to be written on.
	f_pos = open('charlotteHospPos.csv','w')
	f_neg = open('charlotteHospNeg.csv','w')
	
	client = MongoClient()
	# Access the yelp_test database
	dBase = client.yelp_test

	# Access the filtered reviews for further processing.
	charlotteHospitalReviews = dBase.yelp_test_charlotte_hospitals_reviews

	# Group phrases as either positive or negative
	word_cnt_pos = defaultdict(int)
	word_list = []
	noun_dict_pos = defaultdict(int)
	word_cnt_neg = defaultdict(int)
	noun_dict_neg = defaultdict(int)
	reviewHash = {}
	keyCount = 0
	for item in charlotteHospitalReviews.find():
		keyCount = keyCount + 1
		reviewHash[keyCount] = item["text"]
	for key, value in reviewHash.iteritems():
		string = value
		if(positive(string,0.1)):
			try:
				words = nltk.word_tokenize(string)
				tagged = nltk.pos_tag(words)
				chunkGram = "NP: {<JJ> <NN>|<JJ> <NNS>|<NN> <NNS>}"
				chunkParser = nltk.RegexpParser(chunkGram)
				chunked = chunkParser.parse(tagged)
				for subtree in chunked.subtrees():
					if subtree.label() == 'NP':
						string = subtree.leaves()
						(terms, tags) = zip(*subtree)
						for i in range(0,len(terms)):
							word_list.append(terms[i].lower())
							word_cnt_pos[terms[i].lower()] += 1
						noun_dict_pos[(terms[0].lower(),terms[1].lower())] = 1
						word_list = []	
			except Exception as e:
				pass
		else:
			try:
				words = nltk.word_tokenize(string)
				tagged = nltk.pos_tag(words)
				chunkGram = "NP: {<NNP> <NN|NNP>|<RB> <JJ>|<JJ> <NNS>|<NN> <NN>}"
				chunkParser = nltk.RegexpParser(chunkGram)
				chunked = chunkParser.parse(tagged)
				for subtree in chunked.subtrees():
					if subtree.label() == 'NP':
						string = subtree.leaves()
						(terms, tags) = zip(*subtree)
						for i in range(0,len(terms)):
							word_list.append(terms[i].lower())
							word_cnt_neg[terms[i].lower()] += 1
						noun_dict_neg[(terms[0].lower(),terms[1].lower())] = 1
						word_list = []
			except Exception as e:
				pass
	for key, value in noun_dict_pos.iteritems():
		for word in key:
			if key not in noun_dict_neg:
				noun_dict_pos[key] += word_cnt_pos[word]
			else:
				noun_dict_pos.pop(key)
				noun_dict_neg.pop(key)
	for key, value in noun_dict_neg.iteritems():
		for word in key:
			if key not in noun_dict_pos:
				noun_dict_neg[key] += word_cnt_neg[word]
			else:
				noun_dict_pos.pop(key)
				noun_dict_neg.pop(key)
	for key, value in noun_dict_neg.iteritems():
		new_string = ""
		for word in key:
			new_string = new_string + word +" "
		new_string.strip()
		if(positive(new_string,0.1) == False):
			for word in key:
				phrase_true = False
				if word.isalpha() == True or word == "dr." or word == "mr." or word == "ms." or word == "mrs.":
					print word,
					phrase_true = True
				else:phrase_true = False;break
			try:
				if phrase_true == True:f_neg.write(new_string+" "+","+str(value)+"\n");print value
			except:pass
	for key, value in noun_dict_pos.iteritems():
		new_string = ""
		for word in key:
			new_string = new_string + word +" "
		new_string.strip()
		if(positive(new_string,0.1)):
			for word in key:
				phrase_true = False
				if word.isalpha() == True or word == "dr." or word == "mr." or word == "ms." or word == "mrs.":
					print word,
					phrase_true = True
				else:phrase_true = False;break
			try:
				if phrase_true == True:f_pos.write(new_string+" "+","+str(value)+"\n");print value
			except:pass