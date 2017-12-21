# Quickstart - git based pipeline

Follow the steps mentioned below for git based pipeline

1. Ensure that you have a git project
2. Edit `app/src/server.py`
3. Commit your changes

    ```bash
    $ git add .
    $ git commit -m "message"
    ```

4. Push the changes to git

    ```bash
    $ git push <remote> master
    ```

# Local development

Here, <cluster-name> is the name of your cluster. (Not the alias)
( You can get the cluster name from the `hasura cluster status` command )
```bash
$ cd app/src
$ pip install -r requirements.txt
$ FLASK_APP=__init__.py CLUSTER_NAME=<cluster_name> flask run
```
# Advanced usage

### **Port**

Default Port for application is `8080` .

Application port can be changed by modifying the variable `bind` in  `app/conf/gunicorn_config.py` or setting Environment Variable

```python
bind = "0.0.0.0:" + os.environ.get("APP_PORT", "<NEW_PORT>")
```

