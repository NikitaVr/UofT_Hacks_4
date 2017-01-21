from flask import Flask, render_template, request, jsonify
from pprint import pprint
from pymongo import MongoClient
import ast
import datetime 
import time
from time import gmtime

app = Flask(__name__)
@app.route("/")
def index():
    return "Hello World" 



if __name__ == '__main__':
    app.run(
        host = "localhost",
        port = 5000
    )