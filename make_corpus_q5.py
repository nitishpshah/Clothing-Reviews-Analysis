done = ': Done'

lemmatize_words = 1
stem_words      = 1
spell_check     = 1     # slower than lemmatize
spell_check_depth = 1   # can be 1 (about 7 secs for preprocessing) or 2(more than 3 minutes), more accuracy at 2
sym_spell_check = 0     # also very slow
only_words_in_dictionary = 0

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
from itertools import combinations

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

# In[9]:
def get_wordnet_pos(treebank_tag):
	if treebank_tag.startswith('J'):
		return wordnet.ADJ
	elif treebank_tag.startswith('V'):
		return wordnet.VERB
	elif treebank_tag.startswith('N'):
		return wordnet.NOUN
	elif treebank_tag.startswith('R'):
		return wordnet.ADV
	elif treebank_tag.startswith('S'):
		return wordnet.ADJ_SAT
	else:
		return wordnet.VERB


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

delete_duplicate_letters = re.compile(r"([a-zA-Z0-9_])\1{2,}")

def clean_data(data, stop_words=stopwords, stemmer=stemmer, lematizer=lemmatiser):

	'''
	return ret_list, ret_pos_list, ret_index_list, ret_orig_pos_list
	RETURNS: 
		1. list of cleaned words
		2. list of POS tags of the words
		3. index of each word of (1) in the original list
		4. original pos list of the ret_list
	'''

	# # delete apostrophies, it's => its
	# data = data.replace('\'', '')	# done by tokenize
	# data = re.sub('[\']', '', data)

	data = data.lower()

	# seperate sentences with full stops, question and exclaimation marks
	data = re.sub('[?!.]', '\n', data)

	data.replace('n\'t', ' not')
	data.replace('\'s', ' is')
	data.replace('\'s', ' is')
	data.replace('\'d', ' had')
	data.replace('\'ll', ' will')
	data.replace('\'ve', ' have')
	data.replace('\'er', ' never')
	data.replace('\'re', ' are')
	data.replace('\'re', ' are')
	# potential clause breakers, conjunctions
	# data = re.sub('[(but|except|aside from|apart from|other than|besides)]', '\n', data)

	# delete punctuation marks including ' and "
	data = re.sub('[^a-z\s]', '', data)

	# split each sentence
	data = data.split('\n')

	ret_list = []
	ret_pos_list = []
	ret_orig_pos_list = []
	ret_index_list = []

	for i in range(len(data)):

		# words from the review sentence
		ret_list.append([])

		# POS tag of each word in the final word list of the review sentence
		ret_pos_list.append([])

		# index of the word in the original reviwe sentence
		ret_index_list.append([])

		sentence = data[i]

		# delete punctustion marks '?', '!' => ' '  -------- again?
		sentence = re.sub('[^a-z\s\']', ' ', sentence)
		sentence = delete_duplicate_letters.sub(r"\1\1", sentence)

		if sym_spell_check == 1:

			input_term = (sentence)	# whole review
			suggestions = sym_spell.lookup_compound(input_term, max_edit_distance_lookup)
			#  for suggestion in suggestions:
			if sentence != suggestions[0].term:
				# print(sentence, '\nCorrection:', suggestions[0].term,'\n')
				sentence = suggestions[0].term  # take the first suggestion, split at spaces
		
		words = word_tokenize(sentence)	

		if spell_check == 1:
			corrected_sentence = []
			for word in words:
				if word == '':
					continue
				# blindly correct each word at depth spell_check_depth if not in dictionary
				cor_word = spelling.correction(word, spell_check_depth)
				corrected_sentence.append(cor_word)
			words = corrected_sentence

		# part of speech tagging
		words_pos = pos_tag(words)
		ret_orig_pos_list.append(words_pos)

		for j in range(len(words)):

			word = words[j]
			word_postag = words_pos[j][1]

			# lemmatize
			if lemmatize_words == 1:
				# postag=get_wordnet_pos(postag)
				for tag in ['v','a','s','r','n']:
					word_ = lemmatiser.lemmatize(word, pos=tag)
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

			if word not in string.punctuation and not word.isnumeric() and len(word) > 2 and word not in stop_words:

				ret_list[i].append(word)
				ret_pos_list[i].append(word_postag)
				ret_index_list[i].append(j)

	return ret_list, ret_pos_list, ret_index_list, ret_orig_pos_list
	# return ret_list, ret_pos_list, data, ret_orig_pos_list

# print('Group by IDs', end=' ')
# reviews_ = dataframe.groupby('Clothing ID')
# cloth_id_reviews = reviews_.groups
# print(done)

def clean_make_and_store_corpus(
		dataframe,
		corpus_file_name='processed_corpus.pkl', 
		corpus_pos_file_name='processed_corpus_pos.pkl', 
		corpus_index_file_name='processed_corpus_index.pkl', 
		corpus_original_pos_file_name='processed_corpus_original_pos.pkl',
		review_list_df_map_file_name='review_list_df_map.pkl'
	):
	corpus = []
	corpus_pos = []
	corpus_index = []
	corpus_orig_pos = []
	to_drop = []
	# review index in corpus [] => review index in detaframe loc[]
	review_list_df_map = {}
	total = len(dataframe)
	# for each clothing id
	for ID, review in dataframe['text'].iteritems():

		if ID%50 == 0:
			print('cleaning data and making a corpus: ', round(ID*100/total, 2),'% Done',  end='\r')

		if review == ' : ' or review == '':
			# empty review
			to_drop.append(ID)
			continue

		word_list, pos_tags, index_list, orig_pos = clean_data(review, stopwords)

		for i in range(len(word_list)):	
			if len(word_list[i]) > 0:
				corpus.append(' '.join(word_list[i]))
				corpus_pos.append(pos_tags[i])
				corpus_index.append(index_list[i])
				corpus_orig_pos.append(orig_pos[i])
				review_list_df_map[len(corpus)-1] = ID

	# dataframe = dataframe.drop(to_drop)
	print('cleaning data and making a corpus: 100.00% Done',  end='\r')

	print('storing the corpus to HD', end='')

	with open(corpus_file_name, 'wb') as output:
		pickle.dump(corpus, output, pickle.HIGHEST_PROTOCOL)

	with open(corpus_pos_file_name, 'wb') as output:
		pickle.dump(corpus_pos, output, pickle.HIGHEST_PROTOCOL)

	with open(corpus_index_file_name, 'wb') as output:
		pickle.dump(corpus_index, output, pickle.HIGHEST_PROTOCOL)

	with open(corpus_original_pos_file_name, 'wb') as output:
		pickle.dump(corpus_orig_pos, output, pickle.HIGHEST_PROTOCOL)

	with open(review_list_df_map_file_name, 'wb') as output:
		pickle.dump(review_list_df_map, output, pickle.HIGHEST_PROTOCOL)

	print(done)

	return corpus, corpus_pos, corpus_index, corpus_orig_pos, review_list_df_map


# # ********************************************************************************
# dataframe = import_dataframe()
# clean_make_and_store_corpus()
# # ********************************************************************************