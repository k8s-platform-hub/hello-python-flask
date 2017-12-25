import os
import sys

PRODUCTION_ENV = os.environ.get("PRODUCTION")
if PRODUCTION_ENV == "true":
    dataUrl = "http://data.hasura/v1/query"
    dataHeaders = {
       "Content-Type": "application/json",
       "X-Hasura-Role": "anonymous",
       "X-Hasura-User-Id": "0"
    }
else:
    cluster_name = os.environ.get("CLUSTER_NAME")
    if cluster_name is None:
        print("""Set the name of your cluster as an environment variable and try again:

        $ export CLUSTER_NAME=<cluster-name>

        """)
        sys.exit(1)
    dataUrl = "https://data." + cluster_name + ".hasura-app.io/v1/query"
    dataHeaders = {
       "Content-Type": "application/json"
    }
