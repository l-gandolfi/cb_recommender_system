import numpy as np
from retrieve import Retrieve
import os.path as path
from sklearn.metrics import classification_report
import sqlite3
from collections import Counter

'''
@author: Luca Gandolfi
@title: Evaluations of the system

Questo script va semplicemente a misurare la Precision e Recall dei risultati
del Recommender System per due utenti. I risultati finali verranno uniti con una media.
Non verrà utilizzata la GUI per eseguire queste misure.
'''
PATH =  path.abspath(path.join(__file__ ,"../.."))+'/tweets_data/'
conn = sqlite3.connect(PATH+'full_database.db')
c = conn.cursor()

list_classes = ['sport', 'music', 'science', 'economics', 'environment', 'politics', 'news', 'cinema', 'religion', 'tech', 'food']

user_id = 'Jack'
model = 'BERT'

def class_report(user_id, model):
	R = Retrieve(user_id, model)
	topics = R.get_topics()

	all_similarity_results = []

	for topic in topics:
		vectors = R.get_vectorsUP(topic)
		mean_vector = R.calculateMean(vectors)
		similarity_results = R.computeSimilarity(mean_vector,15)
		all_similarity_results.append(similarity_results)

	results_dict = {k: v for d in all_similarity_results for k, v in d.items()}

	results_dict_ordered = {k: v for k, v in sorted(results_dict.items(), key=lambda item: item[1])}
	top_n = 20
	top_n_dict = dict(Counter(results_dict_ordered).most_common(top_n))
	keys = [k for k, v in top_n_dict.items()]

	topics_retr = []
	for i in range(0, top_n):
		c.execute("SELECT topic FROM Tweets WHERE tweet_id=? ",(keys[i],))
		topics_retr.append(c.fetchone()[0].decode('utf-8'))

	print(topics_retr)
	print('\n')
	print(topics)
	print('\n')
	print(top_n_dict)
	binary_pred = [1 for i in range(0,20)]
	binary_real = []
	for topic in topics_retr:
		if topic in topics:
			binary_real.append(1)
		else:
			binary_real.append(0)

	print(classification_report(binary_real, binary_pred))

print(user_id+" and "+model+" model:")
class_report(user_id, model)
model = 'Word2Vec'
print(user_id+" and "+model+" model:")
class_report(user_id, model)

user_id = 'Genny'
print(user_id+" and "+model+" model:")
class_report(user_id, model)
model = 'BERT'
print(user_id+" and "+model+" model:")
class_report(user_id, model)



