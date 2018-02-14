import requests
from flask import jsonify, request
from src import app

# // For local development,
# // First: connect to Hasura Data APIs directly on port 9000
# // $ hasura ms port-forward data -n hasura --local-port=9000
# // Second: Uncomment the line below
# dataUrl = 'http://localhost:9000'

dataUrl = 'http://data.hasura/v1/query'

@app.route("/get_articles")
def get_articles():
    if 'hasura-app.io' in request.url_root:
        query = {
            "type": "select",
            "args": {
                "table": "article",
                "columns": [
                    "*"
                ]
            }
        }
        response = requests.post(dataUrl, data=json.dumps(query))
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return 'Something went wrong: <br/>' + response.status_code + '<br/>' + response.text

    # Change the data URL during local development
    return ("Edit the dataUrl variable in <code>microservices/app/src/hasura.py</code> to test locally.")
