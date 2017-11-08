import os

try:
   if os.environ["PRODUCTION"]:
      dataUrl = "http://data.hasura/v1/query"
      dataHeaders = {"Content-Type": "application/json", "X-Hasura-Role":"anonymous", "X-Hasura-User-Id":"0"}
except KeyError:
   try:
      cluster_name = os.environ["CLUSTER_NAME"]
      dataUrl = "https://data." + cluster_name + ".hasura-app.io/v1/query"
      dataHeaders = {"Content-Type": "application/json"}
   except KeyError:
      print(  " Please set the name of your cluster as an environment variable using 'export CLUSTER_NAME=<cluster-name>', where <cluster-name> is the name of your cluster" )
      os.exit(1)
