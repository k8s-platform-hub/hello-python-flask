import requests, json
from flask import request, render_template
from src import app

# // For local development,
# // First: connect to Hasura Data APIs directly on port 9000
# // $ hasura ms port-forward data -n hasura --local-port=9000
# // Second: Uncomment the line below
# dataUrl = 'http://localhost:9000/v1/query'

# When deployed to your cluster, use this:
dataUrl = 'http://data.hasura/v1/query'

@app.route("/examples/data")
def get_articles():
    if ('hasura-app.io' in request.url_root) or \
       ('data.hasura' not in dataUrl):

        query = {
            "type": "select",
            "args": {
                "table": "article",
                "columns": [ "title", "id", "author_id", "rating", "title" ],
                "limit": 10
            }
        }

        response = requests.post(dataUrl, data=json.dumps(query))
        if response.status_code == 200:
            return render_template('data.html', data=json.dumps(response.json(), indent=2, sort_keys=True))
        else:
            return 'Something went wrong: <br/>' + str(response.status_code) + '<br/>' + response.text

    # Change the data URL during local development
    return ("""Edit the dataUrl variable in
        <code>microservices/app/src/hasura.py</code>
        to test locally.""")
