import sqlite3
import json
import os.path as path

'''
@author: Stefano Sacco
@title: CRUD functions for DB

Instruction:
sudo apt-get install sqlite3
sudo apt-get install sqlitebrowser
'''

DB_PATH =  path.abspath(path.join(__file__ ,"../.."))+'/tweets_data/'

class Functions():
    
    def __init__(self, DB_PATH):
        super().__init__()
        self.cur, self.con = self.getConnection()  
        self.createDatabase()

    def getConnection(self):
        #Connection to database
        connection = sqlite3.connect(DB_PATH+'full_database.db')
        cursor = connection.cursor()
        return cursor, connection

    def createDatabase(self):
        #Create table
        self.cur.execute('CREATE TABLE IF NOT EXISTS Tweets(tweet_id INTEGER PRIMARY KEY AUTOINCREMENT, tweet TEXT, topic BLOB, vector_bert BLOB, vector_model BLOB, date VARCHAR(32))') 
        self.cur.execute('CREATE TABLE IF NOT EXISTS Users(user_id INTEGER, tweet_id INTEGER, topic BLOB, vector_bert BLOB, vector_model BLOB)') 

    def dropTables(self, tname):
        #Drop table
        self.cur.execute('DROP TABLE '+tname) 

    def insertData(self,data):
        id = data[0]
        tweet = json.dumps(data[1]).encode('utf8')
        topic = json.dumps(data[2]).encode('utf8')
        vector_bert = json.dumps(data[3]).encode('utf8')
        vector_model = json.dumps(data[4]).encode('utf8')
        date = data[5]

        try:
            # Insert a row of data
            self.cur.execute("INSERT INTO Tweets (tweet_id,tweet,topic,vector_bert,vector_model,date) VALUES(?,?,?,?,?,?)",(id, tweet, topic, vector_bert, vector_model, date))
            # Save (commit) the changes
            self.con.commit()
        except:
            print("Data insertion failed")

    def insertUser(self,data):
        user_id = data[0]
        tweet_id = data[1]
        topic = data[2]
        vector_bert = data[3]
        vector_model = data[4]
	    # Insert a row of data
        self.cur.execute("INSERT INTO Users (user_id,tweet_id,topic,vector_bert,vector_model) VALUES(?,?,?,?,?)",(user_id, tweet_id, topic, vector_bert, vector_model))
        # Save (commit) the changes
        self.con.commit()

    def readAllData(self):
        rows = []      
        try:
            # Read all data in db
            self.cur.execute("SELECT * FROM Tweets") 
            rows = self.cur.fetchall()     
        except:
            print("Data read failed")

        return rows

    def readData(self,id):
        row = []
        try:
            #Read data by id
            self.cur.execute("SELECT * FROM Tweets WHERE id=?", (id,))
            row = self.cur.fetchall()
        except:
            print("Data read failed")
        
        return row

    def parseData(self, data):
        d = data.decode("utf-8")
        d = d.replace('[','')
        d = d.replace(']','')
        d = d.replace(' "','')
        d = d.replace('"','')
        d = d.replace(', ',',')
        d = list(d.split(","))
        return d

if __name__ == '__main__':

    #Testing functions

    '''
    #Testing some data insertion into DB
    id = 4545
    topic = ['pol','miao','bau']
    vector = [223,234,555,333]
    data = [id,topic,vector]

    id2 = 3433
    data2 = [id2,topic,vector]

    #Creating Function object
    f = Functions(DB_PATH)

    #Data insertion
    f.insertData(data)
    f.insertData(data2)
    
    #Reading one row from DB
    data = f.readData(3433)
    topic = data[0][1]
    vector = data[0][2]

    topics = f.parseData(topic)
    vectors = f.parseData(vector)
    
    for topic in topics:
        print(topic)
    
    for vector in vectors:
        print(vector)

    #Reading all datas from DB
    datas = f.readAllData()

    for row in datas:
        print(row)
        for topic in f.parseData(row[1]):
            print(topic)
        for vector in f.parseData(row[2]):
            print(vector)
    '''
