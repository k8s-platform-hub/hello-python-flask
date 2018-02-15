import requests, json
from flask import jsonify, request, render_template
from src import app

@app.route("/examples/auth")
def user_info():
    """
        An example of using Hasura's auth UI kit & API gateway
        to avoid writing auth and session handling code.

        Hasura's auth microservice provides login/signup functionality
        and can redirect back to your own app.

        Hasura's API gateway will automatically resolve session tokens into
        HTTP headers containing user-id and roles.
    """
    # print (str(request.headers))

    # Important for local development, ignore otherwise.
    # Local development will need you to add custom headers to simulate the API gateway.
    if 'x-hasura-allowed-roles' not in [x.lower() for x in request.headers.keys()]:
        return """This route can only be accessed
            via the Hasura API gateway.
            Add headers via your browser if you're testing locally.<br/>
            <a href="https://docs.hasura.io/0.15/manual/gateway/session-middleware.html"
              target="_blank">Read the docs.</a>"""

    # If user is not logged in
    # render the HTML page with a login link.
    if ('anonymous' in request.headers['x-hasura-allowed-roles']):
        return render_template(
            'auth_anonymous.html',
            **{'base_domain': request.headers['X-Hasura-Base-Domain']}
        )

    # If the user is logged in
    # render the HTML template showing the user's auth info
    else:
        return render_template(
            'auth_user.html',
            **{
                'base_domain': request.headers['X-Hasura-Base-Domain'],
                'user_id': request.headers['X-Hasura-User-Id'],
                'roles': request.headers['X-Hasura-Allowed-Roles']
            }
        )
