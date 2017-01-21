import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory,make_response
from werkzeug.utils import secure_filename
from pprint import pprint
from pymongo import MongoClient
import ast
from datetime import datetime
from time import gmtime, strftime
import json
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# run these lines to access the Mirror Mirror application
os.environ["CLARIFAI_APP_ID"] = "fXM043GazV7t45lQSFQpw3Jj8NIuRWO4PEVNtzBS"
os.environ["CLARIFAI_APP_SECRET"] = "mKsHrQ7CKaHXROyeNfZlaDNZ61W2BH3jjIJ9NJ_7"

# initializing clarify app
cApp = ClarifaiApp()
model = cApp.models.get('Style-Categorizer')

client = MongoClient('localhost',27017)
db = client.MirrorMirror
user_images = db.user_Images

UPLOAD_FOLDER = 'users/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#Initiallizing Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')





@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            username = request.cookies.get('userID')
            print(username)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], username)
            filename = os.path.join(app.config['UPLOAD_FOLDER']+username, "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            print(app.config['UPLOAD_FOLDER']+username)
            file.save(filename)


            #image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')
            image = ClImage(file_obj=open(filename, 'rb'))
            pred = model.predict([image])


            user_images.insert_one(
                {
                    "username": username,
                    "filepath": filename,
                    "clarifai_data": pred       
                }
            )
            print(pred)

            return jsonify({"success":True})
    elif(request.method == 'GET'):
        return render_template("upload.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/login', methods=['POST','GET'])
def my_form_post():
    if(request.method == 'POST'):
        username = str(request.form['username']).strip()
        print(username)
        if((username!= "") and (not(os.path.isdir("users/" + username + "/")))):
            os.makedirs("users/" + username + "/")
            resp = make_response(render_template('upload.html'))
            resp.set_cookie('userID',username)
            return resp
        elif((username!= "") and (os.path.isdir("users/" + username + "/"))):
            resp = make_response(render_template('upload.html'))
            resp.set_cookie('userID',username)
            return resp
        else:
            return "<h1>Please enter a Username!!</h1>"
            
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(
        host = "localhost",
        port = 5000
    )

