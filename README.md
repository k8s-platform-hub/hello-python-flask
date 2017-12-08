# hello-python-flask

This quickstart consists of a basic hasura project with a simple Flask app running on it. Once this project is deployed, you will have the Flask app running on your [cluster](https://docs.hasura.io/0.15/manual/getting-started/index.html#concept-2-a-hasura-cluster).

Follow along below to learn about how this quickstart works.

## Prerequisites

* Ensure that you have the [hasura cli](https://docs.hasura.io/0.15/manual/install-hasura-cli.html) tool installed on your system.

```sh
$ hasura version
```

Once you have installed the hasura cli tool, login to your Hasura account

```sh
$ # Login if you haven't already
$ hasura login
```

* You should also have [git](https://git-scm.com) installed.

```sh
$ git --version
```

## Getting started

```sh
$ # Get the project folder and create the cluster in one shot
$ hasura quickstart hasura/hello-python-flask

$ # Navigate into the Project
$ cd hello-python-flask

```

![Quickstart](https://raw.githubusercontent.com/hasura/hello-python-flask/master/assets/quickstart.png "Quickstart")

The `quickstart` command does the following:
1. Creates a new folder in the current working directory called `hello-python-flask`
2. Creates a new trial hasura cluster for you and sets that cluster as the default cluster for this project. (In this case, the cluster created is called `bogey45`)
3. Initializes `hello-python-flask` as a git repository and adds the necessary git remotes.

## The Hasura Cluster

Everytime you perform a `hasura quickstart <quickstart-name>`, hasura creates a free cluster for you. Every cluster is given a name, in this case, the name of the cluster is `bogey45`. To view the status and other information about this cluster:

```sh
$ hasura cluster status
```

![ClusterStatus](https://raw.githubusercontent.com/hasura/hello-python-flask/master/assets/clusterstatus.png "ClusterStatus")

The `Cluster Configuration` says that the local and cluster configurations are different, this is because we have not deployed our local project to our cluster. Let's do that next.

## Deploy app to cluster

```sh
$ # Ensure that you are in the hello-python-flask directory
$ # Git add, commit & push to deploy to your cluster
$ git add .
$ git commit -m 'First commit'
$ git push hasura master
```

Once the above commands complete successfully, your project is deployed to your cluster.

To check out your `flask` app

```sh
$ # www is the name of the flask app
$ hasura microservice open www
```

Alternatively, you can also open up the URL directly in your browser by navigating to `https://www.<cluster-name>.hasura-app.io` (Replace `<cluster-name>` with your cluster name, this case `bogey45`)

The URL should render a webpage (`index.html`) from `microservices/www/app/src/templates/index.html`.

## More on deployment

### Deploying changes

Now, lets make some changes to our `flask` app and then deploy those changes.

Modify the `server.py` file at `microservices/www/app/src/server.py` by uncommenting line 12 - 14

```python
@app.route('/new')
def new():
  return "Hello world from new"

```

The above code is adding another route `/new` which returns "Hello world from new".

Save `server.py`.

To deploy these changes to your cluster, you just have to commit the changes to git and perform a git push to the `hasura` remote.

```sh
$ # Git add, commit & push to deploy to your cluster
$ git add .
$ git commit -m 'Added a new route'
$ git push hasura master
```

To see the changes, open the URL and navigate to `/new` (`https://www.<cluster-name>.hasura-app.io/new`, replace `<cluster-name>` with your cluster name)

### View Logs

To view the logs for your microservice

```sh
$ # www is the service name
$ hasura microservice logs www
```

## Customize your deployment

### Dockerfile

Microservices on Hasura are deployed as Docker containers managed on a Kubernetes cluster. You can know more about this [here](https://docs.hasura.io/0.15/manual/custom-microservices/develop-custom-services/index.html#using-a-dockerfile)

A `Dockerfile` contains the instructions for building the docker image. Therefore, understanding how the `Dockerfile` works will help you tweak this quickstart for your own needs.

```Dockerfile

# Fetches a base container which has python installed on it
FROM python:3.5.2-alpine

WORKDIR /usr/src/app

# install requirements
# this way when you build you won't need to install again
# and since COPY is cached we don't need to wait
COPY app/src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY app /usr/src/app

# App port number is configured through the gunicorn config file
CMD ["gunicorn", "--config", "./conf/gunicorn_config.py", "src:app"]

```

### Migrating existing app

If you already have a prebuilt flask app and would want to use that. You have to replace the contents inside the `microservices/www/app/src` directory with your app files.

What matters is that the `Dockerfile` and the `k8s.yaml` file remain where they are, i.e at `microservices/www/`. Ensure that you make the necessary changes to the `Dockerfile` such that it runs your app. You can learn more about `Docker` and `Dockerfiles` from [here](https://docs.docker.com/)

## Running the app locally

Everytime you push, your code will get deployed on a public URL. However, for faster iteration you should locally test your changes.

You can use the following steps to test out your dockerfile locally before pushing it to your cluster

```sh
$ # Navigate to the www directory
$ cd microservices/www

$ # Build the docker image (Note the . at the end, this searches for the Dockerfile in the current directory)
$ docker build -t python-flask .

$ # Run the command inside the container and publish the containers port 8080 to the localhost 8080 of your machine
$ docker run -p 8080:8080 -ti python-flask
```
