import sqlite3
import json, pathlib, os

class DatabaseManagement:
    """Manages and Create databases"""

    def __init__(self,data_list, db_name):
        """Creates database by accepting values from data_list parameter
        
        db_name     --> is the name of the database that will be created
        dataType    --> data type supposed to be stored by the data_list parameter
        data_list --> List of data 
        """
        print("HELLOC")
        if pathlib.Path('databases/'+str(db_name)+'.db').exists():
            os.remove('databases/'+str(db_name)+'.db')
        self.myData = data_list # list of data

        self.conn = sqlite3.connect("databases/"+str(db_name)+".db") # Creating the database with name stored in db_name
        
        #Create a cursor object
        self.cursor = self.conn.cursor()

        self.conn.close()

        self.createTable()

    
    def createTable(self):
        """Creates a table using the data given from  self.myData"""
        #1st convert the 1D list to 2D
        x_vals = []
        y_vals = []

        i = 0
        for element in self.myData:
            if i > 0:
                x_vals.append(self.myData[i][0:element.find(",")])
                y_vals.append(self.myData[i][element.find(",")+1:])
            i += 1

        twoDlist = [x_vals,y_vals] #list of the values stored in self.myData but stored in 2D

        self.storeToDB(twoDlist)


    def storeToDB(self,twoDList):
        """Store the give 2d list to the created db file as a table"""

        #convert the 2D list to a JSON string
        data_json = json.dumps(twoDList)

        #create a table to store the data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data(
                            id INTEGER PRIMARY KEY,
                            json_data TEXT  
        )''')

        #insert the JSON Data into the table
        self.cursor.execute('INSERT INTO data (json_data) VALUES (?)',(data_json,))
        self.conn.commit()

        #close the connection
        self.conn.close()

    def printData(self):
        conn = sqlite3.connect('databases/dataPoints.db')
        cursor = conn.cursor()

        cursor.execute("SELECT json_data FROM data")
        rows = cursor.fetchall()
        
        print(rows[0][0])

        conn.close()
