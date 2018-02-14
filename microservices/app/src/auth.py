import requests, json
from flask import jsonify, request, render_template
from src import app

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
