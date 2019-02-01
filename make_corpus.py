done = ': Done'

lemmatize_words = 1	# prefered
stem_words      = 1
spell_check     = 1     
spell_check_depth = 1  
sym_spell_check = 0   # no symspell library with this version, do NOT change to 1

# if stemming is done, no use of lemmatization and vice versa
if lemmatize_words == 1:
	stem_words = 0

if stem_words == 1:
	lemmatize_words = 0

if sym_spell_check == 1:
	spell_check = 0

if spell_check == 1:
	sym_spell_check = 0

import random
import re
import sys
import string
import os
import pandas as pd
import numpy as np
import pickle

import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from scipy.spatial.distance import cosine
from scipy.sparse.linalg import svds

from stopwords import stopwords

if sym_spell_check == 1:
	from symspellpy.symspellpy import SymSpell, Verbosity
if spell_check == 1:
	import spelling

lemmatiser = WordNetLemmatizer()
stemmed_words = {}
stemmer = PorterStemmer()

# In[3]:
# drop empty reviews, group by clothing id

def ext():
	sys.exit(1)

# # In[9]:
# def get_wordnet_pos(treebank_tag):
# 	if treebank_tag.startswith('J'):
# 		return wordnet.ADJ
# 	elif treebank_tag.startswith('V'):
# 		return wordnet.VERB
# 	elif treebank_tag.startswith('N'):
# 		return wordnet.NOUN
# 	elif treebank_tag.startswith('R'):
# 		return wordnet.ADV
# 	elif treebank_tag.startswith('S'):
# 		return wordnet.ADJ_SAT
# 	else:
# 		return wordnet.VERB

delete_duplicate_letters = re.compile(r"([a-zA-Z0-9_])\1{3,}")

# In[7]:
# Load symspell dictionary
if sym_spell_check == 1:
	initial_capacity = 83000
	max_edit_distance_dictionary = 2
	prefix_length = 7
	sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary, prefix_length)
	dictionary_path = "frequency_dictionary_en_82_765.txt"
	term_index = 0  
	count_index = 1 
	if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
		print("Dictionary file not found")
	max_edit_distance_lookup = 2

def clean_data(data, stop_words, stemmer=stemmer, lematizer=lemmatiser):

	data = data.lower()
	# delete punctustion marks '?', '!' => ''
	data = re.sub('[^a-z\s\']', ' ', data)
	data = delete_duplicate_letters.sub(r"\1\1", data)

	# if sym_spell_check == 1:

	# 	input_term = (data)	# whole review
	# 	suggestions = sym_spell.lookup_compound(input_term, max_edit_distance_lookup)
	# 	#  for suggestion in suggestions:
	# 	if data != suggestions[0].term:
	# 		# print(data, '\nCorrection:', suggestions[0].term,'\n')
	# 		data = suggestions[0].term  # take the first suggestion, split at spaces
	
	words = word_tokenize(data)	

	if spell_check == 1:
		corrected_sentence = []
		for word in words:
			if word == '':
				continue
			# blindly correct each word at spell_check_depth if not in dictionary
			cor_word = spelling.correction(word, spell_check_depth)
			corrected_sentence.append(cor_word)
		words = corrected_sentence

	# part of speech tagging
	# words_pos = pos_tag(words)

	ret_list = []

	# for j in range(len(words_pos)):
	for j in range(len(words)):
		# word, postag = words_pos[j]
		word = words[j]

		if word not in string.punctuation and not word.isnumeric() and len(word) > 2 and word not in stop_words:

			# lemmatize
			if lemmatize_words == 1:
				# postag=get_wordnet_pos(postag)
				for postag in ['v','a','s','r','n']:
					word_ = lemmatiser.lemmatize(word, pos=postag)
					if word_ != word:
						break
				word = word_

			# stem () if lemmatize, stem words with same 
			if stem_words == 1:
				stemmed_word = stemmer.stem(word)
				word = stemmed_word
				# keep a reverse dictionary of stemmed words, both may be the same
				if stemmed_word not in stemmed_words:
					stemmed_words[stemmed_word] = []
				if word not in stemmed_words[stemmed_word]:
					stemmed_words[stemmed_word].append(word)

			ret_list.append(word)

	return ret_list

def import_dataframe(file_name='reviews.csv'):

	dataframe = pd.read_csv(file_name)
	# drop NaNs
	print('Filling NaNs with empty strings', end=' ')
	dataframe = dataframe.fillna('')
	print(done)
	# combine review title and text
	print('Combining review title and text', end=' ')
	dataframe['text'] = dataframe['Title'] + ' : ' + dataframe['Review Text']
	print(done)

	return dataframe

# SA
# print('Group by IDs', end=' ')
# reviews_ = dataframe.groupby('Clothing ID')
# cloth_id_reviews = reviews_.groups
# print(done)

def clean_make_and_store_corpus(dataframe):

	corpus = []
	to_drop = []
	# review index in corpus [] => review index in detaframe loc[]
	review_list_df_map = {}
	total = len(dataframe)
	# for each clothing id
	for ID, review in dataframe['text'].iteritems():
		if ID%500 == 0:
			print('cleaning data and making a corpus: ', round(ID*100/total, 2),'% Done',  end='\r')
		if review == ' : ':
			to_drop.append(ID)
			continue
		corpus.append(' '.join(clean_data(review, stopwords)))
		review_list_df_map[len(corpus)-1] = ID
	# dataframe = dataframe.drop(to_drop)
	print('cleaning data and making a corpus: 100.00% Done',  end='\r')

	print('storing the corpus to HD', end='')

	with open('processed_corpus.pkl', 'wb') as output:
		pickle.dump(corpus, output, pickle.HIGHEST_PROTOCOL)

	with open('review_list_df_map.pkl', 'wb') as output:
		pickle.dump(review_list_df_map, output, pickle.HIGHEST_PROTOCOL)

	print(done)

	return corpus, review_list_df_map


# # ********************************************************************************
# dataframe = import_dataframe()
# clean_make_and_store_corpus()
# # ********************************************************************************
