lsa_search = 1
tfidf_search = 1

done = ': Done\n'

# import random
import re
import sys
# import string
# import os
import pandas as pd
import numpy as np
import pickle
# import bisect
import time

from pathlib import Path

import nltk
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from scipy.sparse.linalg import svds
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine

from stopwords import stopwords
from make_corpus import *

def ext():
	sys.exit(1)

remake_corpus = 0

start = time.clock()
reviews_df = import_dataframe('reviews.csv')

my_file = Path("./processed_corpus.pkl")
my_file2 = Path("./review_list_df_map.pkl")

if not my_file.is_file() or not my_file2.is_file() or remake_corpus == 1:
	print('Making Corpus:')
	corpus, review_list_df_map = clean_make_and_store_corpus(reviews_df)
else:
	print("Importing pre-processed corpus")
	with open('processed_corpus.pkl', 'rb') as corpus_file:
		corpus = pickle.load(corpus_file)
	with open('review_list_df_map.pkl', 'rb') as review_map_file:
		review_list_df_map = pickle.load(review_map_file)

end = time.clock()
print(done, 'took ',round(end-start, 2), 'seconds  <------------------------------------ TIME TAKEN ')

print()
print('example review: ', reviews_df.loc[review_list_df_map[999]]['text'])
print('corpus tokenized and cleaned review: ', corpus[999])
print()

# ---------------------------------------------------------------
# ### Vectorize
# ---------------------------------------------------------------

print('Making document frequency matrix from corpus: ', end='')
vectorizer = CountVectorizer(stop_words=stopwords, strip_accents='ascii')
docs_tf = vectorizer.fit_transform(corpus)	# learns vocabulary
vocabulary_terms = vectorizer.get_feature_names()
print(done)

# ---------------------------------------------------------------
# ### TFIDF
# ---------------------------------------------------------------

transformer = TfidfTransformer(smooth_idf = False)

print('Making document tfidf matrix: ', end='')
docs_tfidf = transformer.fit_transform(docs_tf)	# fit => learn idf, transform => return 
print(done)

# ---------------------------------------------------------------
# ### Latent Semantic Analysis (LSA)
# ---------------------------------------------------------------

print('performing LSA on the reviews: ', end='')
A = docs_tfidf.T # D x V matrix 
U, s, V = svds(A, k=16)

s = s[::-1]
singular_values = len(s)
dimensions = 8

A_reduced = np.dot(U[:,:dimensions], np.dot(np.diag(s[:dimensions]), V[:dimensions, :])) # D x V matrix 
docs_rep = np.dot(np.diag(s[:dimensions]), V[:dimensions, :]).T # D x K matrix 
terms_rep = np.dot(U[:,:dimensions], np.diag(s[:dimensions])) # V x K matrix
print(done)

# ---------------------------------------------------------------
# ### Query TFIDF
# ---------------------------------------------------------------

def transform_query_tfidf(key_words_string):
	query_tf = vectorizer.transform([' '.join(key_words_string)])
	query_tfidf = transformer.transform(query_tf)
	return query_tfidf

# key_words2 = 'love gorgeous comfortable perfect fabulous neat cheap love like excited cute amazing flair best good cool great pleasant comfortable'
# key_words = 'dissapointed ugly hate revealing bad fit horrible faded return hate not upset old costly pricey hate horrible expensive worst flaw cheap ludricous used fit'

key_words2 = 'gorgeous dress, perfectly stretchable, good size'
key_words = 'dissapointed and ugly dress, i am returning it'

key_words = clean_data(key_words, stopwords)
key_words2 = clean_data(key_words2,stopwords)

# print('Making query tfidf vector using keywords\n\t "',key_words,'" \n: ', end='')
query_tfidf = transform_query_tfidf(key_words)
query_tfidf2 = transform_query_tfidf(key_words2)

# ---------------------------------------------------------------
# ### Rank TFIDF
# ---------------------------------------------------------------

tfidf_cos_dist = []
total = docs_tfidf.shape[0]

if tfidf_search:
	print('for Query: ', key_words)
	start = time.clock()
	for i in range(total):
		if i%500 == 0:
			print('Checking Documents for similarity using TF-IDF: ', round(i*100/total, 2),'% Done',  end='\r')	
		cos = cosine_similarity(query_tfidf, docs_tfidf[i])[0][0]
		tfidf_cos_dist.append(cos)
		# bisect.insort(query_doc_tfidf_tfidf_cos_dist, cos)
	tfidf_query_doc_sort_index = np.argsort(np.array(tfidf_cos_dist))
	end = time.clock()
	print('Checking Documents for similarity using TF-IDF: 100.00% Done, took', round(end-start, 2),'seconds  <------------------------------------ TIME TAKEN')	

	# print('Printing the 10 most similar documents')
	printed = 0
	total 	= len(tfidf_query_doc_sort_index)
	ratings = []
	while True:
		user_input = input('******************* ENTER m TO SHOW THE NEXT 10 SIMILAR DOCUMENTS, x to exit: *******************\n')
		if type(user_input) == str and user_input[0].lower() == 'm':
			print_count = 0
			for rank, sort_index in enumerate(tfidf_query_doc_sort_index[total-printed::-1]):
				print_count += 1
				printed 	+= 1
				review = reviews_df.loc[review_list_df_map[sort_index]]
				ratings.append(review['Rating'])
				print (' Sr: ***', printed, '***\tIndex: ', sort_index,'\tSimilarity: ', tfidf_cos_dist[sort_index],'\nStars',review['Rating'],'\nReview: ', review['text'], '\n')
				if print_count > 10:
					break
		else:
			break

# ---------------------------------------------------------------
# ### Query Encode LSA
# ---------------------------------------------------------------

def query_encode_lsa(key_words, vocabulary_terms):
	key_word_indices = [] # vocabulary indices 
	for key_word in key_words:
		if key_word in vocabulary_terms:
			key_word_indices.append(vocabulary_terms.index(key_word))
		else:
			key_word_indices.append(0)
	key_words_rep = terms_rep[key_word_indices,:]
	query_rep = np.sum(key_words_rep, axis = 0)
	return query_rep

query_rep = query_encode_lsa(key_words, vocabulary_terms)
query_rep2 = query_encode_lsa(key_words2, vocabulary_terms)

# ---------------------------------------------------------------
# ### Rank LSA
# ---------------------------------------------------------------

# lsa_cos_dist = [cosine_similarity(query_rep, doc_rep) for doc_rep in docs_rep]
lsa_cos_dist = []
total = docs_tfidf.shape[0]
if lsa_search:
	start = time.clock()
	for i in range(total):
		if i%750 == 0:
			print('Checking Documents for similarity using LSA: ', round(i*100/total, 2),'% Done',  end='\r')
		cos = cosine_similarity(query_rep.reshape(1,-1), docs_rep[i].reshape(1,-1))[0][0]
		lsa_cos_dist.append(cos)
		# bisect.insort(query_doc_tfidf_tfidf_cos_dist, cos)
	lsa_query_doc_sort_index = np.argsort(np.array(lsa_cos_dist))
	end = time.clock()
	print('Checking Documents for similarity using LSA: 100.00% Done, took', round(end-start, 2),'seconds')	

	printed = 0
	total 	= len(lsa_query_doc_sort_index)
	ratings = []
	while True:
		user_input = input('*********** ENTER m TO SHOW THE NEXT 10 SIMILAR DOCUMENTS, x to exit: *******************\n')
		if type(user_input) == str and user_input[0].lower() == 'm':
			print_count = 0
			for rank, sort_index in enumerate(lsa_query_doc_sort_index[total-printed::-1]):
				print_count += 1
				printed += 1
				review = reviews_df.loc[review_list_df_map[sort_index]]
				ratings.append(review['Rating'])
				print ('Sr:', printed, '\tIndex: ', sort_index,'\tSimilarity: ', lsa_cos_dist[sort_index],'\nStars',review['Rating'],'\nReview: ', review['text'], '\n')
				if print_count > 10:
					break
		else:
			break

# ratings_df = reviews_df.loc[review_list_df_map.values()]['Recommended IND']
# ratings_df = reviews_df.loc[review_list_df_map.values()]['Age']

def func(x):
	if x >= 3:
		return 1
	else:
		return 0

ratings = list(reviews_df.loc[review_list_df_map.values()]['Rating'].apply(func)/5)
plt.scatter(docs_rep[:,0], docs_rep[:,1], c=ratings, alpha=0.35) # all documents 
plt.scatter(query_rep[0], query_rep[1], marker='+', c='red') # the query 
plt.scatter(query_rep2[0], query_rep2[1], marker='o', c='blue') # the query
plt.title('Documents in semantic space, colored by rating')
plt.legend(['Reviews',key_words,key_words2])
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.show()
# plt.hist( lsa_cos_dist , bins=11, range=(0,1))
# plt.hist(tfidf_cos_dist, bins=11, range=(0,1))
# plt.hist(docs_rep[:,2]) # all documents 

# plot documents in the new space  
# get_ipython().run_line_magic('matplotlib', 'inline')
# import matplotlib.pyplot as plt
# plt.scatter(docs_rep[:,0], docs_rep[:,1], c=lsa_cos_dist) # all documents 

