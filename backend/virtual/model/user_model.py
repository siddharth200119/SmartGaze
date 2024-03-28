import mysql.connector
import json
from flask import make_response
class user_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="mohit",database="smart")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Established")
        except:
            print("Connection Establishment error")
    
    def user_getall_model(self):
        #code that has to be written
        self.cur.execute("SELECT * FROM to_do_list")
        result=self.cur.fetchall()
        if(len(result)>0):
            # return json.dumps(result)
            return {'payload':result}
        else:
            return {"message":"No Data Found"} 
        
    def user_addone_model(self, data):
        self.cur.execute(f"INSERT INTO to_do_list(title, item_description, UID, due_date) VALUES('{data['title']}','{data['item_description']}','{data['UID']}','{data['due_date']}')")
        return {"message": "task created successfully" }
    
    def user_update_model(self, data):
        self.cur.execute(f"UPDATE to_do_list SET title = '{data['title']}', item_description = '{data['item_description']}', UID = '{data['UID']}' , due_date = '{data['due_date']}' WHERE TID = {data['TID']}")
        if self.cur.rowcount>0:
            return {"message": "task updated successfully" }
        else:
            return {"message": "nothing to update" }
        
    def user_delete_model(self, TID):
        self.cur.execute(f"DELETE FROM to_do_list WHERE TID = {TID}" )
        if self.cur.rowcount>0:
            return {"message": "User deleted successfully" } 
        else:
            return {"message": "not deleted" }

    def user_delete2_model(self, data):
        self.cur.execute(f"DELETE FROM users WHERE TID = {data['TID']}")
        if self.cur.rowcount>0:
            return {"message": "User deleted successfully" } 
        else:
            return {"message": "not deleted" } 

    