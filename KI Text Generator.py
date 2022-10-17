# -*- coding: utf-8 -*-
#!/usr/bin/python3.7 -S
import time
start_time = time.time()

import re
#import site
import codecs
from nltk.corpus import stopwords
import locale
import gensim
import gensim; print("gensim", gensim.__version__)
import logging
import pprint
import sys
import os.path
import os, sys
import glob
from bs4 import BeautifulSoup
import os
import glob

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lSent = list()
filename = "/root/patenteMarcel/similiarity.bin";

"""
# training with fresh start
try:
	os.unlink(filename)
	map(os.remove, glob.glob("/root/patenteMarcel/*.npy"))
except Exception as e:
	1
"""

def makeASCII(text):
	text	= text.replace("'","")
	text	= text.replace("\\","")
	text	= text.replace("\"","")
	text	= text.replace(":","")
	text	= ''.join([i if ord(i) < 128 else ' ' for i in text])
	return re.sub(r'[^\x00-\x7F]+',' ', text)

def encodeToUTF8Adv(text):
	encResults 	= text.encode('utf-8', "ignore")
	#return str(encResults.decode('latin-1', "ignore"))
	s_string	= str(encResults.decode('utf-8', "remove"))
	#textv1 		= re_pattern.sub(u'\uFFFD', s_string)
	return s_string

def encodeToLatin1(text):
	#text 		= text.replace('ß','ss')
	encResults  = text.encode('utf-8', "ignore")
	#encResults = text.encode('utf-8', "ignore")
	s_string	= str(encResults.decode('latin-1', "ignore"))
	#textv1 		= re_pattern.sub(u'\uFFFD', s_string)
	return s_string

def process_query(query):
    words = []
    words = query.split()
    return words

def getSimilar(p_headline, model):
	#sim = model.score(p_shortcode, total_sentences=1000000, chunksize=100, queue_factor=2, report_delay=1)
	#print(model.docvecs.offset2doctag)
	rVal = str("")

	"""
	vector = model.infer_vector(p_headline.split())
	print("VECTOR:",vector)
	#print("MOST SIMILAR:",model.most_similar(positive=[vector], topn=10))
	docvecs = model.docvecs.most_similar(positive=[vector], topn=10)

	for vec in docvecs:
	    print(vec)
	"""

	try:
		l 		= process_query(p_headline)
		vector 	= model.infer_vector(l)
		sims 	= model.docvecs.most_similar(positive=[vector], negative=[], topn=10)
		#sims = model.docvecs.most_similar_cosmul(positive=[p_headline], negative=[], topn=20)
		for i, val in enumerate(sims):
			print("DEBUG p_headline Shortcode: ",sims[i][0]," / Score: ",sims[i][1])
			if len(sims[i][0]) >= 1:
				rVal += sims[i][0]+";"
		return rVal
	except Exception as e:
		1#return ""

	return rVal

def trainGensimWord2Vec(sentences):
	num_epochs 		= 10
	# Word vector dimensionality
	num_features	= 800
	# Minimum word count - min_count = ignore all words with total frequency lower than this.
	min_word_count	= 1
	# Number of threads to run in parallel
	num_workers		= 50
	# Context window size
	context			= 35
	# Downsample setting for frequent words
	downsampling	= 1e-3
	# Initialize and train the model (this will take some time)

	if os.path.isfile(filename):
		model 		= gensim.models.Doc2Vec.load(filename)
	else:
		#model 		= gensim.models.Doc2Vec(iter=5, size=400, workers=10, sorted_vocab=1, alpha=0.65, min_alpha=0.15, window=25, sample=1e-5, dbow_words=1, min_count=1) #
		model = gensim.models.Doc2Vec(workers=num_workers, dbow_words=1, vector_size=num_features, min_count=min_word_count, window=context, sample=downsampling, dm=1, hs=1, alpha=0.025, epochs=num_epochs)

		#model.sort_vocab()
		model.build_vocab(sentences)

		for epoch in range(1):
			model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
			# decrease the learning rate
			model.alpha -= 0.002
			# fix the learning rate, no decay
			model.min_alpha = model.alpha

		model.init_sims(replace=False) 	# can read,write from, and also training -> more memory
		#model.init_sims(replace=True)	# can only read from, but no more training -> less memory
		model.save(filename)
	return model

def create_wordlist( review, remove_stopwords=True ):
	# Function to convert a document to a sequence of words,
	# optionally removing stop words.  Returns a list of words.
	#
	# 1. Remove HTML
	review_text = BeautifulSoup(review, "lxml").get_text()
	#
	# 2. Remove non-letters
	review_text = re.sub("[^a-zA-Z0-9 ]"," ", review_text)
	#
	# 3. Convert words to lower case and split them
	words = review_text.lower().split()
	words = review_text.split()
	#
	# 4. Optionally remove stop words (false by default)
	if remove_stopwords:
		stops = set(stopwords.words("german"))
		stopsE = set(stopwords.words("english"))
		words = [w for w in words if not w in stops]
		words = [w for w in words if not w in stopsE]
	#
	# 5. Return a list of words
	return(words)


count = int(0)
os.chdir("/root/patenteMarcel/Patente/")
#os.chdir("/root/patenteMarcel/text_reden/")

for file in glob.glob("*.txt"):
	f 			= open(file,'r',encoding="utf-8")
	readFile 	= str(f.read())
	f.close()
	words 		= create_wordlist(readFile)
	labelSent 	= gensim.models.doc2vec.TaggedDocument(words, [file])
	lSent.append(labelSent)
	count += 1

model 		= trainGensimWord2Vec(lSent)

#textInput 	= input("prompt")  # Python 3 - read from command line
textInput	= "image processing artificial intelligence"
print("######################################################################################")
print("These where similar to your search request (filenames): ", textInput)
print("######################################################################################")
simArticle	= getSimilar(textInput, model)
