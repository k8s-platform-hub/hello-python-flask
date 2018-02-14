import requests, json
from flask import jsonify, request, render_template
from src import app

# // For local development,
# // First: connect to Hasura Data APIs directly on port 9000
# // $ hasura ms port-forward data -n hasura --local-port=9000
# // Second: Uncomment the line below
# dataUrl = 'http://localhost:9000/v1/query'

# When deployed to your cluster, use this:
dataUrl = 'http://data.hasura/v1/query'

@app.route("/examples/get-data")
def get_articles():
    if ('hasura-app.io' in request.url_root) or \
       ('data.hasura' not in dataUrl):

        query = {
            "type": "select",
            "args": {
                "table": "article",
                "columns": [
                    "*"
                ],
                "limit": 10
            }
        }

        response = requests.post(dataUrl, data=json.dumps(query))
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return 'Something went wrong: <br/>' + str(response.status_code) + '<br/>' + response.text

    # Change the data URL during local development
    return ("""Edit the dataUrl variable in
        <code>microservices/app/src/hasura.py</code>
        to test locally.""")


@app.route("/examples/auth")
def user_info():
    """
        An example of using Hasura's API gateway to avoid writing
        auth code and session handling code.
    """
    print (str(request.headers))

    # Local development will need you to add custom headers
    if 'x-hasura-allowed-roles' not in [x.lower() for x in request.headers.keys()]:
        return """This route can only be accessed
            via the Hasura API gateway.
            Add headers via your browser if you're testing locally.<br/>
            <a href="https://docs.hasura.io/0.15/manual/gateway/session-middleware.html"
              target="_blank">Read the docs.</a>"""

    # If user is not logged in (via Hasura's auth)
    if ('anonymous' in request.headers['x-hasura-allowed-roles']):
        return render_template('anonymous.html',
            **{'base_domain': request.headers['X-Hasura-Base-Domain']})

    # If user is logged in
    else:
        return render_template('user.html',
            **{
                'base_domain': request.headers['X-Hasura-Base-Domain'],
                'user_id': request.headers['X-Hasura-User-Id'],
                'roles': request.headers['X-Hasura-Allowed-Roles']
            })

@app.route("/examples/user-files")
def files():
    """
        Sample endpoint that allows logged in users to upload files
        and shows users the files they've uploaded.
    """
    print (str(request.headers))

    # Local development will need you to add custom headers
    if 'x-hasura-allowed-roles' not in [x.lower() for x in request.headers.keys()]:
        return """This route can only be accessed
            via the Hasura API gateway.
            Deploy with <code>git push</code> and then test this route."""

    # If user is not logged in (via Hasura's auth)
    if ('anonymous' in request.headers['x-hasura-allowed-roles']):
        return render_template('anonymous_file.html',
            **{'base_domain': request.headers['X-Hasura-Base-Domain']})

    # If user is logged in, show the user files they have uploaded
    else:
        # Query from the fileupload table
        requestPayload = {
            "type": "select",
            "args": {
                "table": {
                    "name": "hf_file",
                    "schema": "hf_catalog"
                },
                "columns": [ "*" ],
                "where": {"user_id": request.headers['x-hasura-user-id']}
            }
        }

        # Make the query and store response in resp
        resp = requests.post(dataUrl, data=json.dumps(requestPayload))

        # resp.content contains the json response.
        if not(resp.status_code == 200):
            print (resp.text)
            return "Something went wrong while trying to fetch files: " + resp.text

        files = resp.json()
        return render_template('user.html',
            **{
                'base_domain': request.headers['X-Hasura-Base-Domain'],
                'files': request.headers['X-Hasura-User-Id']
            })
