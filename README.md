Command to run Flask App (from root directory)

Set up the database

```python
pipenv shell
FLASK_APP=web_app flask db init
FLASK_APP=web_app flask db migrate
FLASK_APP=web_app flask db upgrade
```

```python
pipenv shell
FLASK_APP=web_app flask run
```
