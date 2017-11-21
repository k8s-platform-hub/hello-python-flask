from flask import Flask
from .hasuraExamples import hasura_examples

app = Flask(__name__)

# This line adds the hasura example routes form the hasuraExamples.py file.
# Delete this, and then delete the file to remove them from your project
app.register_blueprint(hasura_examples)

from .server import *
