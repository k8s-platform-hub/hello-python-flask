import json
import requests
from flask import Blueprint
from .config import dataUrl, dataHeaders

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
    print(json.dumps(query))
    print(dataUrl)

    response = requests.post(
        dataUrl, data=json.dumps(query),
        headers=dataHeaders
    )

    return response.content
