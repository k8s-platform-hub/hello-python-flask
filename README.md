# hello-python-flask

Boilerplate Hasura project with [Flask](http://flask.pocoo.org/) microservice.

## Prerequisites

- [Hasura CLI](https://docs.hasura.io/0.15/manual/install-hasura-cli.html)
- [Git](https://git-scm.com)
- [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) (required only for local development)

## Getting started

### Quickstart

```bash
# Quickstart from this boilerplate 
$ hasura quickstart hello-python-flask
```

The `quickstart` command does the following:

1. Creates a new directory `hello-python-flask` in the current working directory
2. Creates a free Hasura cluster and sets it as the default for this project
3. Sets up `hello-python-flask` as a git repository and adds `hasura` remote to push code
4. Adds your SSH public key to the cluster so that you can push to it

### Deploy

```bash
# Navigate to the project directory
$ cd hello-python-flask

# git add, commit and push to deploy
$ git add . && git commit -m "First commit"
$ git push hasura master
```

Once the git push completes, the Flask microservice (called `app`) will be available at a URL.

```bash
# Open the flask app url in browser
$ hasura microservice open app
```

If the browser shows a "Hasura Hello World" page, everything is working as expected.
If it doesn't, go through the previous steps and see if you missed anything.

## Flask Microservice

### Directory structure

The microservice is located in `microservices/app` directory in your Hasura project with the following structure:

```bash
.
├── Dockerfile
├── k8s.yaml
├── conf
│   └── gunicorn_config.py
└── src
    ├── config.py
    ├── hasuraExamples.py
    ├── __init__.py
    ├── requirements.txt
    ├── server.py
    ├── static
    └── templates
```

### Change and deploy code

#### Edit

`server.py` is where the main app is present. You can edit this file and deploy the changes.
For example, un-comment lines `2`, `11-13` to add new URL `/json`:

```python
from flask import jsonify

@app.route("/json")
def json_message():
    return jsonify(message="Hello World")
```

These lines will add `/json` which returns `{"message": "Hello World"}`.

#### Deploy

Save the file, git add, commit and push to deploy the changes:

```bash
# git add, commit and push to deploy
$ git add src/server.py
$ git commit -m "add new url /json"
$ git push hasura master
```

#### Verify

To checkout the new URL, open the microservice URL in a browser and navigate to `/json`:

```bash
# open the url in browser
$ hasura microservice open app

# add /json at the end of the url
```

#### Debug

If the push fails with an error `Updating deployment failed`, or the URL is showing `502 Bad Gateway`/`504 Gateway Timeout`,
follow the instruction on the page and checkout the logs to see what is going wrong with the microservice:

```bash
# see status of microservice app
$ hasura microservice list

# get logs for app
$ hasura microservice logs app
```

You can deploy further changes by going through Edit->Deploy->Verify->Debug cycle again and again.

### Local development

With Hasura's easy and fast git-push-to-deploy feature, you hardly need to run your code locally.
However, you can follow the steps below in case you have to run the code in your local machine.

#### Without Docker

It is recommended to use a [Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for Python when you are running locally.
Don't forget to add these directories to `.gitignore` to avoid committing packages to source code repo.

```bash
# setup pipenv or virtualenv and activate it (see link above)

# go to app directory
$ cd microservices/app

# install dependencies
$ pip install -r src/requirements.txt

# Optional: set an environment variable to run Hasura examples 
# otherwise, remove Hasura examples, 
#   delete lines 5-8 from `src/__init__.py`
#   remove files `src/config.py` and `src/hasuraExamples.py`
$ export CLUSTER_NAME=[your-hasura-cluster-name]

# run the development server (change bind address if it's already used)
$ gunicorn --reload --bind "0.0.0.0:8080" src:app
```

Go to [http://localhost:8080](http://localhost:8080) using your browser to see the development version on the app.
You can keep the gunicorn server running and when you edit source code and save the files, the server will be reload the new code automatically.
Once you have made required changes, you can [deploy them to Hasura cluster](#deploy).

#### With Docker

Install [Docker CE](https://docs.docker.com/engine/installation/) and cd to app directory:

```bash
# go to app directory
$ cd microservices/app

# build the docker image
$ docker build -t hello-python-flask-app .

# run the image with port bindings and CLUSTER_NAME environment variable
# as mentioned above, remove Hasura examples if you don't want to add CLUSTER_NAME
$ docker run --rm -it -p 8080:8080 -e CLUSTER_NAME=[your-hasura-cluster-name] hello-python-flask-app

# app will be available at `http://localhost:8080`
# press Ctrl+C to stop the running container
```

For any change you make to the source code, you will have to stop the container, build the image again and run a new container.
If you mount the current directory as a volume, you can live-reload your code changes:

```bash
# go to app directory
$ cd microservices/app

# build the docker image
$ docker build -t hello-python-flask-app .

# run the container
$ docker run --rm -it -p 8080:8080 \
             -e CLUSTER_NAME=[your-hasura-cluster-name] \
             -v $(pwd):/app \
             hello-python-flask-app \ 
             gunicorn --reload --bind "0.0.0.0:8080" src:app
             
# app will be available at `http://localhost:8080`
# press Ctrl+C to stop the running container
```

Now, any change you make to your source code will be immediately updated on the running app.

### Customize

Hasura runs [microservices](https://docs.hasura.io/0.15/manual/custom-microservices/index.html) as Docker containers on a Kubernetes cluster.
You can read about [Hasura architecture](https://docs.hasura.io/0.15/manual/cluster/architecture.html) in case you want to know more.

#### Add a python dependency

In order use new python package in your app, you can just add it to `src/requirements.txt` and the git-push or docker build process will
automatically install the package for you. If the `pip install` steps thorw some errors in demand of a system dependency,
you can install those by adding it to the `Dockerfile` at the correct place.

```
# src/requirements.txt:

flask
requests
gunicorn

# add your new packages one per each line
```

#### Add a system dependency

The base image used in this boilerplate is [python:3](https://hub.docker.com/_/python/) debian. Hence, all debian packages are available for installation.
You can add a package by mentioning it in the `Dockerfile` among the existing `apt-get install` packages.

```dockerfile
# Dockerfile

FROM python:3

# install required debian packages
# add any package that is required after `python-dev`, end the line with \
RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev \
&& rm -rf /var/lib/apt/lists/*

# install requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# set /app as working directory
WORKDIR /app

# copy current directory to /app
COPY . /app

# run gunicorn server
# port is configured through the gunicorn config file
CMD ["gunicorn", "--config", "./conf/gunicorn_config.py", "src:app"]

```

#### Deploy your existing Flask app

If you already have a Flask app and want to deploy it onto Hasura, you can replace the contents of `src/` directory with your own app.

- Leave `k8s.yaml`, `Dockerfile` and `conf/` as it is.
- Make sure there is already a `requirements.txt` file present inside the new `src/` indicating all your python dependencies.
- If there are any system dependencies, add and configure them in `Dockerfile`.
- If the Flask app is not called `app`, change the last line in `Dockerfile` reflect the same.  
  For example, if the app is called `backend`, the `CMD` line in `Dockerfile` will become:  
  ```dockerfile
  CMD ["gunicorn", "--config", "./conf/gunicorn_config.py", "src:backend"]
  ```
