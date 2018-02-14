from src import app
from flask import render_template
# from flask import jsonify

@app.route("/")
def home():
    return render_template('index.html')

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
