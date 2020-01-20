'''
@Title: Retrieving utilities functions

This class is the core of the retrieval process.
It is used in the GUI which performs the right call sequences needed.
'''

import os.path as path
import pandas as pd
import numpy as np
import re
import itertools
import string
import gensim
import statistics
import datetime
from scipy import spatial
from db_functions import Functions
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from collections import Counter, OrderedDict
import unicodedata
import copy

class Retrieve():
	def __init__(self, user, model):
		'''
		Define a dict to map user names into their ids -- we know the db structure!
		'''
		users_dict = {'Luca':0, 'Stefy':1, 'Bru':2, 'Jack':3, 'Lollo':4, 'Ale':5, 'Dylan':6, 'Mark':7, 'Genny':8, 'Pippo':9}
		model_dict = {'BERT': 'vector_bert', 'Word2Vec': 'vector_model'}
		
		self.user = users_dict.get(user)
		self.model = model_dict.get(model)
		self.PATH =  path.abspath(path.join(__file__ ,"../.."))+'/tweets_data/'
		self.conn = sqlite3.connect(self.PATH+'full_database.db')
		self.c = self.conn.cursor()
		
	def take(n, iterable):
		"Return first n items of the iterable as a list"
		return list(islice(iterable, n))
	
	def get_countTopic(self):
		self.c.execute("SELECT COUNT(DISTINCT topic) FROM Users WHERE user_id=? ",(self.user,))
		count, = self.c.fetchone()
		return count
		
	def get_topics(self):
		self.c.execute("SELECT DISTINCT topic FROM Users WHERE user_id=? ",(self.user,))
		topics = self.c.fetchall()
		temp = []
		'''
		per semplicità non ri-formatto il risultato: userò il topic as-is nelle query
		'''
		for topic in topics:
			#temp.append(topic[0].decode('utf-8').replace('"',''))
			temp.append(topic[0])
		return temp
	
	'''
	Vectors need to be cleaned
	'''
	def process_users(self, vectors):
		new_vector = []
		out = []
		for vector in vectors:
			#v = vector[0].decode('utf-8')
			temp = []
			#split_v = vector[0].replace('\\n', '')
			split_v = vector[0].replace('[', '')
			split_v = split_v.replace(']', '')
			split_v = split_v.split(' ')

			for token in split_v:
				token = token.replace('\\n', '')

				if token != '':
					temp.append(float(token))
			out.append(temp)

		return out
	
	'''
	Tweets are stored differently than users
	'''
	def process_tweets(self, vectors):
		new_vector = []
		out = []
		for vector in vectors:
			v = vector[0].decode('utf-8')
			temp = []
			v = v.replace(']', '')
			v = v.replace('[', '')
			v = v.replace('\\n', '')
			v = v.replace('"', '')
			split_v = v.split(' ')
			#print(split_v)
			for token in split_v:
				if token != '':
					temp.append(float(token))
			out.append(temp)
		return out

	# Vectors in user profile by topic
	def get_vectorsUP(self, topic):
		self.c.execute("SELECT "+self.model+" FROM Users WHERE user_id=? AND topic=?", (self.user,topic))
		vectors = self.c.fetchall()
		return self.process_users(vectors)
	
	'''
	riceve in input i vettori embedded di un solo topic e restituisce il loro vettore media
	'''
	def calculateMean(self, vectors):
		return [statistics.mean(k) for k in zip(*vectors)]
	
	'''
	riceve in input il vettore centroide dal quale computare la similarità
	'''	
	def computeSimilarity(self, centroid, top_n):
		# retrieve embedding from db
		self.c.execute("SELECT "+self.model+" FROM Tweets")
		vectors = self.c.fetchall()
		# clean blob vectors
		clean_vectors = self.process_tweets(vectors)
		print('computing similarity')
		# compute similarity
		similarity_dict = {}
		id = 0
		for vector in clean_vectors:
			sim = np.dot(centroid, vector)/(np.linalg.norm(centroid)*np.linalg.norm(vector))
			similarity_dict[id] = sim
			id = id+1
		
		# order the dict
		ordered = OrderedDict(sorted(similarity_dict.items(), key=lambda element: element[1],reverse=True))
		most_similar = dict(Counter(ordered).most_common(top_n))
		# Here you could filter the top scored if it has similarity=1
		return most_similar
	
	'''
	pusha un nuovo tweet nello user profile
	'''
	def pushUP(self, tweet_id_list):
		for tweet_id in tweet_id_list:
			# first we check if the tweet has already been inserted
			exist = self.c.execute("SELECT EXISTS (SELECT 1 FROM Users WHERE user_id=? AND tweet_id=? LIMIT 1)", (self.user, tweet_id,)).fetchone()[0]
			if(exist == 0):
				# query the db to obtain the correct tweet
				self.c.execute("SELECT * FROM Tweets WHERE tweet_id=?", (tweet_id,))
				tweet = self.c.fetchall()[0]
				# now that we have the tweet row we must insert it into the user profile
				up = []
				up.append(self.user)
				up.append(tweet[0])
				up.append(tweet[2])
				# 3 and 4 are the embeddings: they must be processed to be in the correct format
				vector_bert = tweet[3].decode('utf-8').replace('"', '')
				vector_model = tweet[4].decode('utf-8').replace('"', '')
				up.append(vector_bert)
				up.append(vector_model)
				db_fun = Functions(self.PATH)
				db_fun.insertUser(up)
	'''
	funzione accessorio per il print nella gui dei tweet.
	converte i caratteri unicode in normali caratteri ascii
	'''
	def cleanRows(self, rows):
		new_rows = []
		for row in rows:
			row = bytes(row[0].decode("utf-8"), 'ascii').decode("unicode-escape").replace('"', '')
			new_rows.append(row)
		return new_rows
	
	def ranking(self, similarity_dict):
		# We are going to modify the dict so save a copy before do it
		old_similarity_dict = copy.deepcopy(similarity_dict)

		# First obtain dates of tweets -> 2018-02 becomes 1802
		date_list = []
		for k,v in similarity_dict.items():
			self.c.execute("SELECT date FROM Tweets WHERE tweet_id=? ",(k,))
			date = self.c.fetchone()[0]
			parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
			final_date = ''
			final_date += str(parsed_date.year)[2:]
			if(len(str(parsed_date.month)) == 1):
				final_date += str(0)
				final_date += str(parsed_date.month)
			else:
				final_date += str(parsed_date.month)
			
			date_list.append(float(final_date))
		# Now compute a weighted mean 
		count = 0

		for k, v in similarity_dict.items():
			res = ((v) * (date_list[count]/2000))
			count=count+1
			similarity_dict[k]=res
		
		# Order the dict
		dict_ordered = {k: v for k, v in sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)}

		# Retrieve the list of similarity after the new sorting
		top_list = []
		for k,v in dict_ordered.items():
			top_list.append(old_similarity_dict.get(k))
		return dict_ordered, top_list
		
if __name__ == '__main__':
	c = Retrieve('Stefy', 'bert')
	topic = c.get_topics()
	topics = c.get_topics()
	vectors = c.get_vectorsUP(topics[0])
	mean_vector = c.calculateMean(vectors)
	similarity_results = c.computeSimilarity(mean_vector,10)
	print(similarity_results)
