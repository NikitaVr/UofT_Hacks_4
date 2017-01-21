import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pprint import pprint
from pymongo import MongoClient
import ast
import datetime 
import time
from time import gmtime, strftime

UPLOAD_FOLDER = 'users/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

##@app.route("/")
##def index():
##    return "Hello World" #render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if(not(os.path.isdir("testFolder/"))):
        os.makedirs('testFolder/')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>

    <form action="login" method="POST">
        <input type="text" name="username">
        <input type="submit" name="my-form" value="Send">
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/login', methods=['POST'])
def my_form_post():

    username = request.form['username']

    if(not(os.path.isdir("users/" + username + "/"))):
        os.makedirs("users/" + username + "/")

    processed_text = username.upper()
    return processed_text

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

