from flask import Flask, render_template, request, jsonify
from pprint import pprint
from pymongo import MongoClient
import ast
import datetime 
import time
from time import gmtime, strftime

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.FinhacksDB
app_users = db.appUsers
transactions = db.transactions

def debug_table(collection):
    ret = ""
    cursor = collection.find({})
    for document in cursor: 
        ret += str(document) +"\n"
    return ret 

def get_karma(query,collection):
    ret_usr = collection.find_one({"username":query["username"]})
    return str(ret_usr["upVote"])+"|"+str(ret_usr["downVote"])

def insert_friend(query,collection):
    try:
       ret_usr1 = collection.find_one({"username":query["usr1"]})
       ret_usr2 =  collection.find_one({"username":query["usr2"]})
       if not(ret_usr1["_id"] in ret_usr2["friends"]):
           collection.update({"_id":ret_usr1["_id"]},{"$push":{"friends":ret_usr2["_id"]}})
           collection.update({"_id":ret_usr2["_id"]},{"$push":{"friends":ret_usr1["_id"]}})
           return "success"
       else:
           return "Failed"
    except:
        return "None"
def update_pass(query,collection):
    try:
        collection.update({"username":query["username"]},{"$set":{"password":query["new_password"]}})
        return "Success"
    except:
        return "Failed"


def increment_karma(query,collection):
    collection.update({"username":query["username"]},{"$inc":{"upVote":1}})

def decrement_karma(query,collection):
    collection.update({"username":query["username"]},{"$inc":{"downVote":1}})

@app.route("/")
def index():
    return "Hello World" #render_template("index.html")
@app.route("/decreasekarma",methods=["POST"])
def decrease_karma():
     json = request.json
     try:
         decrement_karma(json,app_users)
         return "Success"
     except:
         return "Failed"

if __name__ == '__main__':
    app.run(
        host = "localhost",
        port = 5000
    )

