from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
import sys
import sqlite3
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)
import os.path as path
from retrieve import Retrieve
from itertools import islice
import numpy as np
from collections import Counter
from random import randint
import datetime
'''
@author: Luca Gandolfi
@title: GUI for Recommender System

Instruction:
python -m virtualenv ~/pyqt_venv
source pyqt_venv/bin/activate
-- to close the venv type: deactivate
cd pyqt_venv
pip install PyQt5

Here we are.
'''

PATH =  path.abspath(path.join(__file__ ,"../.."))+'/tweets_data/'
GLOBAL_BLACK_LIST = set()

'''
###############################
	Recommendation Window
###############################
'''
class RecommendList(QWidget):
	def __init__(self, user, model):
		super().__init__()
		self.user = user
		self.MODEL = model
		self.update_list = []
		self.R = Retrieve(self.user, self.MODEL)
		self.conn = sqlite3.connect(PATH+'full_database.db')
		self.c = self.conn.cursor()
		self.initUI()

	'''
	We have to define a database connection here.
	Also we have to import our preprocess class and our class for obtaining the items' list
	'''
	def initUI(self):
		self.resize(1450, 800)
		self.setLayout(QVBoxLayout())
		h_layout = QHBoxLayout()
		self.layout().addLayout(h_layout)
		
		# Call the function to load the table with tweets
		self.load_table()
		
		label = QLabel('Hey! Check out these Tweets!', self)
		h_layout.addWidget(label)

		button = QPushButton('RELOAD', self)
		button.setToolTip('This button will <b>Reload</b> the current window using the selected '+
						'items to improve the system.')
		
		button.clicked.connect(self.reload)
		self.layout().addWidget(button)
		
		back = QPushButton('Back', self)
		back.setToolTip('This button will bring you back to the user selection window.')
		back.clicked.connect(self.goBack)
		self.layout().addWidget(back)
		
		self.center()
		
		self.setWindowTitle('Tweets Recommendation List')
		self.show()
	
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
	def onStateChange_check(self, item):
		# the listener is on every cell of the table
		# we are interested in just when the checkbox is checked
		if item.checkState() == Qt.Checked:
			# first i need to know the row - position
			row_id = item.row()
			# then i have self.keys and i can get its key
			tweet_id = self.keys[row_id]
			# store this id in a global variable and update when the reload button is pressed
			self.update_list.append(tweet_id)
			GLOBAL_BLACK_LIST.add(tweet_id)
			
		elif item.checkState() == Qt.Unchecked:
			row_id = item.row()
			tweet_id = self.keys[row_id]
			if(tweet_id in self.update_list):
				self.update_list.remove(tweet_id)
				GLOBAL_BLACK_LIST.remove(tweet_id)
		
	def reload(self):
		alert = QMessageBox()
		alert.setText('This window will be reloaded!')
		alert.exec_()
		# Call the update user profile function
		self.R.pushUP(self.update_list)
		# After pressing the ok button in the alert, the window will be updated
		self.w = RecommendList(self.user, self.MODEL)
		self.w.show()
		self.hide()
	
	def goBack(self):
		self.w = LoginScreen()
		self.w.show()
		self.hide()
	
	'''
	This function return a list of tweets to show up in the table
	'''
	def getVectors(self):
		n_topic = self.R.get_countTopic()
		topics = self.R.get_topics()
		
		all_similarity_results = [] # list of dicts of N = n_topics elements
		for topic in topics:
			# get vectors by topic in the user profile
			vectors = self.R.get_vectorsUP(topic)
			#print(vectors)
			# get the mean
			mean_vector = self.R.calculateMean(vectors)
			# compute similarity
			similarity_results = self.R.computeSimilarity(mean_vector,20)
			# remove the black listed ids
			similarity_results = {k: v for k, v in similarity_results.items() if k not in GLOBAL_BLACK_LIST}
			# append to the general list
			all_similarity_results.append(similarity_results)
		# Merge results into a single dict
		results_dict = {k: v for d in all_similarity_results for k, v in d.items()}
		# Order by value
		results_dict_ordered = {k: v for k, v in sorted(results_dict.items(), key=lambda item: item[1], reverse=True)}
		# Obtain only top N ids
		top_n = 19
		top_n_dict = dict(Counter(results_dict_ordered).most_common(top_n))
		# Now order by considering the date
		top_n_dict, top_n_list = self.R.ranking(top_n_dict)
		self.keys = [k for k, v in top_n_dict.items()]
		# Obtain the 20th number from the Long-tail
		ran_value = randint(20, len(results_dict_ordered)-1)
		count = 0
		for k, v in results_dict_ordered.items():
			if(count==ran_value):
				ran_key = k
				ran_similarity = v
			count=count+1
		#tail = {ran_key: ran_similarity}
		# Retrieve Tweets
		tweets = []
		dates = []
		for i in range(0, top_n):
			self.c.execute("SELECT tweet FROM Tweets WHERE tweet_id=? ",(self.keys[i],))
			tweets.append(self.c.fetchone())
			self.c.execute("SELECT date FROM Tweets WHERE tweet_id=? ",(self.keys[i],))
			dates.append(self.c.fetchone()[0])
		
		# Get the last one from the tail
		self.c.execute("SELECT tweet FROM Tweets WHERE tweet_id=? ",(ran_key,))
		tweets.append(self.c.fetchone())
		self.c.execute("SELECT date FROM Tweets WHERE tweet_id=? ",(ran_key,))
		dates.append(self.c.fetchone()[0])
		self.keys.append(ran_key)
		return tweets, dates, top_n_list, ran_similarity
		
		
	def load_table(self):
		columns = 4
		
		rows, dates, top_n_list, tail_similarity = self.getVectors()
		rows = self.R.cleanRows(rows)
		n_rows = len(rows)
		
		self.table = QTableWidget(n_rows, columns, self)
		self.table.setHorizontalHeaderLabels(["Tweet", "Do you like it?", "Tweet date", "Similarity"])
		header = self.table.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		#self.table.setResizeMode(QHeaderView.ResizeToContents)
		
		for row in rows:
			inx = rows.index(row)

			self.table.insertRow(inx)
			self.chkBoxItem = QTableWidgetItem('I Like it!')
			self.chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
			self.chkBoxItem.setCheckState(Qt.Unchecked)
			self.chkBoxItem.setToolTip('Help to <b>Improve</b> our system selecting the items you like.')
			# Listener on the checkbox
			self.table.itemClicked.connect(self.onStateChange_check)
			
			#self.table.setItem(inx, 0, QTableWidgetItem(str(row[0].decode("utf-8"))))
			self.table.setItem(inx, 0, QTableWidgetItem(row))
			self.table.setItem(inx, 1, self.chkBoxItem)
			self.table.setItem(inx, 2, QTableWidgetItem(dates[inx]))
			if(inx == (n_rows-1)):
				self.table.setItem(inx, 3, QTableWidgetItem("{:1.5f}".format(tail_similarity)))
			else :
				#self.table.setItem(inx, 3, QTableWidgetItem(str(top_n_list[inx])))
				self.table.setItem(inx, 3, QTableWidgetItem("{:1.5f}".format(top_n_list[inx])))
		self.layout().addWidget(self.table)
			
	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Message',
		"Are you sure to quit?", QMessageBox.Yes |
		QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

'''
############################
		Login Screen
############################
'''
class LoginScreen(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
	
	def initUI(self):
		QToolTip.setFont(QFont('SansSerif', 15))
		self.setLayout(QVBoxLayout())
		
		h_layout = QHBoxLayout()
		self.layout().addLayout(h_layout)
        
		self.userComboBox = QComboBox(self)
		self.userComboBox.addItems(['Luca', 'Stefy', 'Bru', 'Jack', 'Lollo', 'Ale', 'Dylan', 'Mark', 'Genny', 'Pippo'])
		self.USER = 'Luca'
		
		# When another user is selected, we store the user name
		self.userComboBox.activated.connect(self.comboSelected)
		
		label_user = QLabel('Select username:', self)
		label_user.setBuddy(self.userComboBox)
		
		b_layout = QHBoxLayout()
		self.layout().addLayout(b_layout)
		
		self.modelComboBox = QComboBox(self)
		self.modelComboBox.addItems(['Word2Vec', 'BERT'])
		self.MODEL = 'Word2Vec'
		
		# When another model is selected, we store the selected model name
		self.modelComboBox.activated.connect(self.comboSelectedModel)
		
		label_model = QLabel('Select the model:', self)
		label_model.setBuddy(self.modelComboBox)
		
		button = QPushButton('START', self)
		button.setToolTip('Select a <b>User Profile</b>, then press START to initialize the System')

		button.clicked.connect(self.recommendation_list)
		
		h_layout.addWidget(label_user)
		h_layout.addWidget(self.userComboBox)
		b_layout.addWidget(label_model)
		b_layout.addWidget(self.modelComboBox)
		self.layout().addWidget(button)
		
		self.resize(400, 100)
		self.center()
		
		#self.setGeometry(300, 300, 300, 300)
		self.setWindowTitle('User Profile Selection')
		self.show()
		
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		

	def recommendation_list(self):
		self.w = RecommendList(self.USER, self.MODEL)
		self.w.show()
		self.hide()
	
	def comboSelected(self, user):
		self.USER = str(self.userComboBox.currentText())
	
	def comboSelectedModel(self, model):
		self.MODEL = str(self.modelComboBox.currentText())
			        
	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Message',
		"Are you sure to quit?", QMessageBox.Yes |
		QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

			
if __name__ == '__main__':
	app = QApplication([])
	login = LoginScreen()

	sys.exit(app.exec_())
