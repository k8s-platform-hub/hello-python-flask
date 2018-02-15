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

@app.route("/examples/filestore")
def user_files():
    """
        This route renders a file-upload page for users.

        Not logged-in users (anonymous):
            > request that they login

        logged-in users (anonymous):
            > list files they own
            > show file-upload box

        The file-upload and download API uses hasura's filestore APIs
        so you will notice that this code has no file-handling code!

    """
    print (str(request.headers))

    # Important only for local development. Ignore otherwise.
    # Local development will need you to add custom headers
    if 'x-hasura-allowed-roles' not in [x.lower() for x in request.headers.keys()]:
        return """This route can only be accessed
            via the Hasura API gateway.
            Deploy with <code>git push</code> and then test this route."""

    # If user is not logged in
    if ('anonymous' in request.headers['x-hasura-allowed-roles']):
        return render_template(
            'filestore_anonymous.html',
            **{'base_domain': request.headers['X-Hasura-Base-Domain']}
        )

    # If user is logged in, show the user files they have uploaded
    else:
        # Query from the file-upload table to fetch files this user owns.
        # We're using the Hasura data APIs to query
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

        resp = requests.post(dataUrl, data=json.dumps(requestPayload))

        # resp.content contains the json response.
        if not(resp.status_code == 200):
            print (resp.text)
            return "Something went wrong while trying to fetch files: " + resp.text

        files = resp.json()
        return render_template('filestore_user.html',
            **{
                'base_domain': request.headers['X-Hasura-Base-Domain'],
                'files': files
            })
