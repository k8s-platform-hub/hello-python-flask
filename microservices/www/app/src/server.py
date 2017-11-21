from src import app
from flask import jsonify, request, render_template
import requests
import json



@app.route("/")
def hello():
  return render_template('index.html')
