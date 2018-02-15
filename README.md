## What does this come with

- Boilerplate code, configuration for:
  - python3 flask setup with a `requirements.txt` file
  - Gunicorn integration
  - Auto-reloading for local development
  - Ready to go Dockerfile that will automatically install deps from `requirements.txt`


### Deployment instructions

### Basic deployment:

* Press the **Clone & Deploy** button above and follow the instructions.
   * The `hasura quickstart` command clones the project repository to your local system and also creates a **free Hasura cluster** where the project will be hosted for free.
   * A git remote (called hasura) is created and initialized with your project directory.
   * `git push hasura master` builds and deploys the project to the created Hasura cluster.
* The python-flask app is deployed as a microservice called **app**.
   * Run the below command to open your app:
``` shell
 $ hasura microservice open app
```

### Making changes to your source code and deploying

* To make changes to the app, browse to `/microservices/app/src` and edit the python files according to your requirements.
* For example, make changes to `server.py` or to `templates/index.html` to change the landing page.
* Commit the changes, and run `git push hasura master` to deploy the changes.


## Adding backend features

This section will help you bootstrap some backend features using Hasura. If you want to continue vanilla python development, you can skip this section.

Hasura makes it easy to add backend features to your python apps.
- Add auth using an inbuilt UI or APIs for username, email-verification, mobile-otp, social login.
- Integrate with the database easily.
  -  Use data APIs from python to query postgres without an ORM
  -  Or use data APIs directly from the client-side code
- Add file upload/download features using Hasura's file APIs with customisable permissions to configure sharing

You can use Hasura APIs from your client side javascript directly, or from your python code.
Open your app and head to the different example routes:

```
# Open your app in a browser
$ hasura microservice open app

# Head to any of these URLs on the app
/examples/data
/examples/auth
/examples/filestore
```

Read more about Hasura [data](https://hasura.io/features/data), [auth](https://hasura.io/features/auth) & [filestore](https://hasura.io/features/filestore) APIs. They are powerful and can help you save a lot of time and code when building out your applications.

### API console

Hasura gives you a web UI to manage your database and users. You can also explore the Hasura APIs and automatically generate API code in the language of your choice.

#### Run this command inside the project directory

```bash
$ hasura api-console
```
![api-explorer.png](https://filestore.hasura.io/v1/file/463f07f7-299d-455e-a6f8-ff2599ca8402)


## View server logs

If the push fails with an error `Updating deployment failed`, or the URL is showing `502 Bad Gateway`/`504 Gateway Timeout`,
follow the instruction on the page and checkout the logs to see what is going wrong with the microservice:

```bash
# see status of microservice app
$ hasura microservice list

# get logs for app
$ hasura microservice logs app
```

## Adding dependencies

### Add a python dependency

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

### Add a system dependency

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

## Deploying your existing Flask app

Read this section if you already have a Flask app and want to deploy it on Hasura.

- Replace the contents of `src/` directory with your own app's python files.
- Leave `k8s.yaml`, `Dockerfile` and `conf/` as it is.
- Make sure there is already a `requirements.txt` file present inside the new `src/` indicating all your python dependencies (see [above](#add-a-python-dependency)).
- If there are any system dependencies, add and configure them in `Dockerfile` (see [above](#add-a-system-dependency)).
- If the Flask app is not called `app`, change the last line in `Dockerfile` reflect the same.
  For example, if the app is called `backend`, the `CMD` line in `Dockerfile` will become:
  ```dockerfile
  CMD ["gunicorn", "--config", "./conf/gunicorn_config.py", "src:backend"]
  ```

## Local development

Running your python-flask code locally works as it usually would. 

### Running a development server with auto-reload

```bash
# OPTIONAL: http://docs.python-guide.org/en/latest/dev/virtualenvs/
# OPTIONAL: setup pipenv or virtualenv and activate it and update .gitignore

# go to app directory
$ cd microservices/app

# install dependencies
$ pip install -r src/requirements.txt

# run the development server (change bind address if it's already used)
$ gunicorn --reload --bind "0.0.0.0:8080" src:app
```

Go to [http://localhost:8080](http://localhost:8080) using your
browser to see the development version on the app. You can keep the
gunicorn server running and when you edit source code and save the
files, the server will be reload the new code automatically.

**Note**: You can also build and test with docker locally.

### Handling dependencies on other microservices
Your flask app will at some point depend on other microservices like the database,
or Hasura APIs. In this case, when you're developing locally, you'll have to change your
the endpoints you're using. Ideally, you can use an environment variable to switch between
'DEVELOPMENT' or 'PRODUCTION' mode and use different endpoints.

This is something that you're already probably familiar with if you've worked with databases
before.

#### Flask app running on the cluster (after deployment)
Example endpoints:
```
if not os.getenv('DEVELOPMENT'):
  postgres = 'postgres.hasura' #postgres)
  dataUrl  = 'data.hasura'     #Hasura data APIs)
```

#### Flask app running locally (during dev or testing)
Example endpoints:
```
else:
  postgres = 'localhost:5432' #postgres)
  dataUrl  = 'localhost:9000'     #Hasura data APIs)
```

And in the background, you will have to expose your Hasura microservices on these ports locally:

```bash
# Access postgres locally
$ hasura microservice port-forward postgres -n hasura --local-port 5432


# Access Hasura data APIs locally
$ hasura microservice port-forward data -n hasura --local-port 9000
```

