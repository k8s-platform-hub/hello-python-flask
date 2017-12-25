import json
import os
import sys
import requests
from flask import Blueprint, jsonify, request, redirect

PRODUCTION_ENV = os.environ.get("PRODUCTION")
CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
if cluster_name is None:
    print("""
    Set the name of your cluster as an environment variable and start again:

    $ export CLUSTER_NAME=<cluster-name>

    """)

if PRODUCTION_ENV == "true":
    # set dataUrl as internal url if PRODUCTION_ENV is true
    # note that internal url has admin permissions
    dataUrl = "http://data.hasura/v1/query"
else:
    # for local development, contact the cluster via external url
    dataUrl = "https://data." + cluster_name + ".hasura-app.io/v1/query"

hasura_examples = Blueprint('hasura_examples', __name__)

@hasura_examples.route("/get_articles")
def get_articles():
    query = {
        "type": "select",
        "args": {
            "table": "article",
            "columns": [
                "*"
            ]
        }
    }
    print(dataUrl)
    print(json.dumps(query))
    response = requests.post(
        dataUrl, data=json.dumps(query)
    )
    data = response.json()
    print(json.dumps(data))
    return jsonify(data=data)

@hasura_examples.route("/logged_in_user")
def logged_in_user():
    user_id = requests.headers.get('X-Hasura-User-Id')
    if user_id is None:
        return redirect(
            "https://auth."+cluster_name+".hasura-app.io/ui?redirect_to=https://app."+cluster_name+".hasura-app.io/logged_in_user"
        )
    else:
        return jsonify(user_id=user_id, message="Welcome logged in user!")
