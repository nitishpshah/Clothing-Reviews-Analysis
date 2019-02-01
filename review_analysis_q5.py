import sys
if len(sys.argv) > 1:
	remake_corpus_q5 = int(sys.argv[1])
if len(sys.argv) > 2:
	tf_search = int(sys.argv[2])
if len(sys.argv) > 3:
	lsa_search = int(sys.argv[3])
if len(sys.argv) > 4:
	show_graph = int(sys.argv[4])
if len(sys.argv) > 5:
	print('extra arguments')
	sys.exit(1)
else:
	remake_corpus_q5 = 0
	lsa_search = 1
	tf_search = 1
	show_graph = 1

# NOTE: delete this block at the end 
lsa_search = 0
tf_search = 0
show_graph = 0

remake_corpus_q5 = 0
ask_for_product_id = 1
# analyse_full_corpus = 1

verbosity = 0

done = ': Done'

# import random
import re
import string
import pickle
import time

from pathlib import Path

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer

from stopwords import stopwords
import make_corpus_q5

def ext():
	# local short for
	sys.exit(0)

# if analyse_full_corpus:
reviews_df = make_corpus_q5.import_dataframe('reviews.csv')
# else:
# 	reviews_df = make_corpus_q5.import_dataframe('reviews.csv')[:100]

# if analyse_full_corpus:
my_file  = Path("./full_processed_corpus.pkl")
my_file2 = Path("./full_review_list_df_map.pkl")
my_file3 = Path("./full_processed_corpus_pos.pkl")
my_file4 = Path("./full_processed_corpus_index.pkl")
my_file5 = Path("./full_processed_corpus_orig_pos.pkl")
# else:	
	# my_file = Path("./processed_corpus.pkl")
	# my_file2 = Path("./review_list_df_map.pkl")
	# my_file3 = Path("./processed_corpus_pos.pkl")
	# my_file4 = Path("./processed_corpus_index.pkl")
	# my_file5 = Path("./processed_corpus_orig_pos.pkl")

if 		not my_file.is_file() 	\
	or 	not my_file2.is_file() 	\
	or 	not my_file3.is_file() 	\
	or 	not my_file5.is_file() 	\
	or 	not my_file4.is_file() 	\
	or 	remake_corpus_q5 == 1:

	print('Making Corpus:')
	# corpus, corpus_pos, corpus_orig, corpus_orig_pos, review_list_df_map = make_corpus_q5.clean_make_and_store_corpus(reviews_df)
	corpus_full, corpus_pos_full, corpus_index_full, corpus_orig_pos_full, review_list_df_map = make_corpus_q5.clean_make_and_store_corpus(
		reviews_df,
		corpus_file_name=my_file.name, 
		corpus_pos_file_name=my_file3.name, 
		corpus_index_file_name=my_file4.name, 
		corpus_original_pos_file_name=my_file5.name,
		review_list_df_map_file_name=my_file2.name
	)

else:

	print("Importing pre-processed corpus")

	with open(my_file.name, 'rb') as corpus_file:
		corpus_full = pickle.load(corpus_file)
	with open(my_file2.name, 'rb') as review_map_file:
		review_list_df_map = pickle.load(review_map_file)
	with open(my_file3.name, 'rb') as corpus_pos_file:
		corpus_pos_full = pickle.load(corpus_pos_file)
	with open(my_file4.name, 'rb') as corpus_index_file:
		corpus_index_full = pickle.load(corpus_index_file)
	with open(my_file5.name, 'rb') as corpus_orig_file:
		corpus_orig_pos_full = pickle.load(corpus_orig_file)

print(done)

# invert this map
reviews_df_list_map = dict()
for key, value in review_list_df_map.items():
	reviews_df_list_map.setdefault(value, list()).append(key)

# ---------------------------------------------------------------
# ### Ask for product ID
# ---------------------------------------------------------------
if ask_for_product_id:
	# test on 1078 ~1000 reviews or 1033 ~200 reviews
	product_id = input('Enter a porduct ID: ')
	# product_id = 1060
	product_id = int(product_id)

	# get reviews of that ID in the processed corpus
	review_ids = list(reviews_df.loc[reviews_df['Clothing ID'] == product_id]['Id'])
	corpus_reviews_to_analyse = []
	for i in review_ids:
		if i in reviews_df_list_map:
			for j in reviews_df_list_map[i]:
				corpus_reviews_to_analyse.append(j)

	corpus 			= [corpus_full[i] for i in corpus_reviews_to_analyse]
	corpus_pos 		= [corpus_pos_full[i] for i in corpus_reviews_to_analyse]
	corpus_index 	= [corpus_index_full[i] for i in corpus_reviews_to_analyse]
	corpus_orig_pos = [corpus_orig_pos_full[i] for i in corpus_reviews_to_analyse]
else:

	corpus_reviews_to_analyse = range(len(corpus_full))
	corpus 			= corpus_full
	corpus_pos 		= corpus_pos_full
	corpus_index 	= corpus_index_full
	corpus_orig_pos = corpus_orig_pos_full

# ---------------------------------------------------------------
# ### Vectorize
# ---------------------------------------------------------------

print('Making document frequency matrix from corpus: ', end='')
# all words have an id
vectorizer = CountVectorizer(stop_words=stopwords, strip_accents='ascii', ngram_range=(1,1) ) # , min_df=0.005)
vectorizer.fit(corpus)	# just learn the vocab, dont transform instead of # docs_tf = vectorizer.fit_transform(corpus)
vocabulary_terms = vectorizer.get_feature_names()
vocabulary_id = vectorizer.vocabulary_
print(done)

# ---------------------------------------------------------------
# ### Get frequent set of (consecutive) features
# ---------------------------------------------------------------

def get_freqency(words, corpus_coded, corpus_index, max_seperation = 0.5):
	'''
	INPUT:
		words: (unordered) list of distinct word IDs
		corpus_coded: list of list of words ids for each sentence 
		max_seperation*(len(words)-1) is the total number of words allowed in between the `words` in `sentence`
			default = 0.5: if 3 words given, then maximum of (3-1)*0.5 = 1 word(s) allowed in between these words
	RETURNS:
		frequency and which review line had those terms with distance
	'''

	if len(set(words)) < len(words):
		# list has duplicates
		return 0, []

	freq = 0
	review_lines = []
	distances = []

	# for each sentence in the corpus
	for k in range(len(corpus_coded)):

		sentence = corpus_coded[k]
		indices = corpus_index[k]

		word_indices = []
		for word in words:
			# seperate index list for each word
			word_indices.append([])
			word_found = 0
			for i in range(len(sentence)):
				if sentence[i] == word:
					word_indices[-1].append(indices[i])
					word_found = 1
			if word_found == 0:
				# if all words are not found on the sentence,
				continue

		# get all together
		all_word_indices = []
		for i in range(len(word_indices)):
			all_word_indices.extend([(j, i) for j in word_indices[i]])

		# sort by value
		# sentence * log(sentence)
		all_word_indices.sort(key=lambda x:x[0])

		# sentence * sentence * |words|
		# get all subsequences of langth |words| with each word distinct
		# i.e. get possible word combiinations from the sentence
		all_combinations = []
		# start indices and cursor indices in [1...|words|]
		for i in range(len(all_word_indices)):
			word_index, start_query_word = all_word_indices[i]
			new_query_words = [start_query_word]
			word_indices_combination = [word_index]
			for j in range(i, len(all_word_indices)):
				word2_index, new_query_word = all_word_indices[j]
				if new_query_word not in new_query_words:
					new_query_words.append(new_query_word)
					word_indices_combination.append(word2_index)
			if len(word_indices_combination) == len(words):
				all_combinations.append(word_indices_combination)
		
		possible_distances = []
		for word_comb in all_combinations:
			distance = 0
			# calculate distance between the found word combinations
			for i in range(len(word_comb)-1):
				distance += word_comb[i+1] -  word_comb[i]
			possible_distances.append(distance)
		
		for i in range(len(possible_distances)):
			if possible_distances[i] - len(words) <= int(max_seperation*(len(words)-1)):
				# add one frequency for each occurence of feature fround in the sentence
				freq += 1
				review_lines.append(k)
				distances.append(distance-len(words)+1)

		if verbosity > 2:
			print('words', words)
			print('\tsentence',k,':',sentence)
			print('\t\tindices', indices)
			print('\t\tword_indices', word_indices)
			print('\t\tall_word_indices', all_word_indices)
			print('\t\tall_combinations', all_combinations)
			print('\t\tpossible_distances', possible_distances)

	review_lines_dist = list(zip(review_lines, distances))
	review_lines_dist.sort(key=lambda x:x[1])
	return freq, review_lines_dist

# ---------------------------------------------------------------
# ### Get frequent Features
# ---------------------------------------------------------------
# generate all possible features
def get_features(
		corpus, 
		corpus_pos, 
		corpus_index, 
		vocabulary_id=vocabulary_id, 
		vocabulary_terms=vocabulary_terms,
		n_grams = [1,2,3], 
		max_distance_bw_nouns = 2,
		min_freq = 2,
		pre_feature_list=[],
		pre_feature_freqs={}, 
		show_progress=False):

	# do not modfy pre feature lists or freq dictionaries, only used for frequency checking
	feature_list = []
	feature_freqs = {}

	print('Using POS tags to extract nouns', end='')
	corpus_nouns = []
	corpus_coded = []
	for i in range(len(corpus)):

		corpus_nouns.append([])
		corpus_coded.append([])

		if corpus[i] == '':
			# if empty, split generates list with one empty string instead of empty list, so skip
			continue

		words = corpus[i].split(' ')
		for j in range(len(words)):
			# if word in vocabulary_id:		# word has to be in the vocabulary ?
			word = words[j]
			if word not in vocabulary_id:
				# add word to vocabulary
				vocabulary_terms.append(word)
				vocabulary_id[word] = len(vocabulary_terms)-1
			corpus_coded[i].append(vocabulary_id[word])

			if corpus_pos[i][j][0] == 'N':
				# noun
				corpus_nouns[i].append(vocabulary_id[word])
	print(done)

	for n in n_grams:
		feature_list.append([])
		# sorted_features.append([])
		print('Generating',n,'- word features', end='')
		for i in range(len(corpus_nouns)):
			noun_indices = [t for t in range(len(corpus_index[i])) if corpus_pos[i][t][0] == 'N']
			for j in range(len(noun_indices)-(n-1)):
				# for each starting position for the noun group in the sentence
				distance = 0
				vocab_term = [corpus_coded[i][noun_indices[j]]]
				for k in range(n-1):
					# calculate distance between the noun group that start at i and make a list of the coabulary terms
					distance += noun_indices[j+k+1]-noun_indices[j+k]
					vocab_term.append(corpus_nouns[i][j+k+1])
				# allow only `max_distance_bw_nouns` words in between features
				if distance-n < max_distance_bw_nouns:
					# only id dist less than max_words_bw nouns
					vocab_splits = [vocab_term[:r]+vocab_term[r+1:] for r in range(len(vocab_term))]
					if vocab_splits != [[]]:
						for n_min_1 in vocab_splits:
							# each should be a frequent feature, if even one isn't then the whole isn't
							if pre_feature_freqs != {}:
								if frozenset(n_min_1) not in pre_feature_freqs:
									break
							else:
								if frozenset(n_min_1) not in feature_freqs:
									break
						else:
							# not broken, each set was found with sufficient frequency to continue
							feature_list[n-1].append(vocab_term)
					else:
						# one word features will have no splits
						feature_list[n-1].append(vocab_term)

		print(done)
		print('Counting Frequencies')
		count = 0
		total = len(feature_list[n-1])
		discarded_count = 0
		progress = 0
		start = time.clock()

		for word_list in feature_list[n-1]:
			count += 1
			freq, review_lines_dist = get_freqency(word_list, corpus_coded, corpus_index)
			if freq >= min_freq:
				# only add to final frequencies if satisfy min freq requirement
				feature_freqs[frozenset(word_list)] = freq, review_lines_dist	
			else:
				discarded_count += 1

			# display percent progress and ETA

			if show_progress:
				progress = round(count*100/total, 2)
				total_updates = 1000
				if int((progress*total_updates)%100) == 0 and progress != 0.0:		# div by zero
					# update after every 0.01%
					now=time.clock()
					time_left = (now-start)*(total_updates)*((100-progress)/100)
					start = time.clock()
					secs = time_left%60
					totalmins = time_left//60
					hrs = totalmins//60
					mins = totalmins%60
					print('\tProgress: ', progress,'% Done\t ETA: ',hrs,'hrs',mins,'mins', int(secs), 'secs',end='\r')
	
		if show_progress:
			print('Progress: 100% Done\t\t\t\t\n')

		print( count,'possible new',n,'-word features')
		print('discard',discarded_count,'features not with mminimum required frequency')
	
	return feature_freqs, feature_list


feature_freqs, feature_list = get_features(
		corpus, 
		corpus_pos, 
		corpus_index, 
		vocabulary_id=vocabulary_id, 
		n_grams = [1,2,3], 
		max_distance_bw_nouns = 2,
		min_freq = 2,
		show_progress=True)

# ---------------------------------------------------------------
# ### Output frequencies to a file
# ---------------------------------------------------------------

# TODO: frequency dependent on total number of documents

print('sorting n-word features based on frequency for each n-gram', end='')
# first sort on length, then on frequency
sorted_features = sorted(feature_freqs.keys(), key=lambda x: str('{0:03d}'.format(len(x)))+"_"+str(feature_freqs[x]), reverse=True)
print(done)

sid = SentimentIntensityAnalyzer()
sent_list = []

output_q5_file = open("output_q5.txt","w+")
print('storing results in a test file named output_q5.txt', end='')
for feature in sorted_features:
	if len(feature) <= 1:
		# do not print 1 length features, not features
		continue
	feature_name = ''
	for word_id in feature:
		feature_name += vocabulary_terms[word_id]+' '
	output_q5_file.write(str(feature_freqs[feature][0]) +' '+feature_name+'\n')
	sent_list = []
	for review_line, distance in feature_freqs[feature][1]:
		sent_list.append(sid.polarity_scores(corpus[review_line])['compound'])
	sorted_sent_list = np.argsort(sent_list)
	for i in range(len(sorted_sent_list)):
		review_line, distance = feature_freqs[feature][1][i]
		output_q5_file.write('\t '+'sentiment: '+str(int(sent_list[i]*100))+'/100\t'+ ' '.join([word for word, pos in corpus_orig_pos[review_line]]) +" \n")
		output_q5_file.write('\t\t*** ('+str(review_line)+') '+corpus[review_line] + '***\n')
		# +'('+pos[0]+')'
	# break
output_q5_file.close()
print(done)

# print contents of the file
with open('output_q5.txt', 'r') as output_file:
	print(output_file.read())

# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ END PROGRAM -----------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------

ext()

# ---------------------------------------------------------------
# manually make document vectors and try information retrieval
# ---------------------------------------------------------------

# vocabulary
feature_names = [ noun_set for noun_set, frequency in feature_freqs.items()]

# vocabulary index of each feature
feature_index = {}
for i in range(len(feature_names)):
	feature_index[feature_names[i]] = i

docs_tf = np.zeros((len(corpus), len(feature_names)), dtype=np.int)
for feature, review_list in feature_freqs.items():
	for review_index, distance in review_list[1]:
		docs_tf[review_index, feature_index[feature]] += review_list[0]

# not useful anymore
# def flatten_list(list_of_lists):
# 	return [a for b in list_of_lists for a in b]

# ---------------------------------------------------------------
# take an input query
# ---------------------------------------------------------------
# query = input('Enter a query: ')
query = 'the fabric color is beautiful an is of hte perfect stretch. the fabric is very smooth and silky. i wear it all the time. i love it.'
query_list, query_pos, query_index, query_orig_pos	= make_corpus_q5.clean_data(query)
query_coded = [[vocabulary_id[word] for word in word_set if word in vocabulary_id] for word_set in query_list]
query_corpus = [' '.join(query_list_item) for query_list_item in query_list]
query_feature_freqs, query_feature_list = get_features(
	query_corpus,
	query_pos,
	query_index,
	min_freq = 1,		# get all features
	show_progress=False)

# vocabulary
query_feature_names = [ noun_set for noun_set, frequency in query_feature_freqs.items()]

query_tf = np.zeros((len(query_corpus), len(feature_names)), dtype=np.int)		# original feature names
for feature, review_list in query_feature_freqs.items():
	for review_index, distance in review_list[1]:
		if feature in feature_index:
			query_tf[review_index, feature_index[feature]] += review_list[0]

# debugging
# for word_id, freq in corpus_nouns[0].items():
#     print(vocabulary_terms[word_id])