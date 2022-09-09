# Run

- Create an Virtual Environment
- install all requirements

```
$ pip install -r requirements.txt
```
- run the appp

```
$ python app.py
```

- start redis server
```
$  celery -A app.celery worker --loglevel=info
```
```
$ celery -A app.celery beat --loglevel=info
```
    
  
