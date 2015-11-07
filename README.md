# schedulord (Scheduler as a Service.)
**DISCLAIMER:** This is **just an implementation of a concept** not a product ready package.

Scheduler as a service over REST API. Basic workflow implemented here is as below
- write a job in python file
- send it to server
- scheduler takes care of the REST

Sounds like a lot of work!
KK then lets copy paste below examples to get started.

# Installation:
There is no package available in pypi as of yet.
```
$ git clone https://github.com/mayuroks/schedulord
$ cd schedulord
$ pip install -r requirements.txt
```

# Usage:
## Start the webserver

```
$ python server.py
```

## Start the scheduler
```
$ python scheduler.py
```
## Write a job
**main function** is what the scheduler will execute
```
$ cat dummy_job_files/great.py

from datetime import datetime

def main():
    print datetime.now()
```
Now we are ready to send our functions over REST API.

## CREATE a job
```python
$ ipython

from utils import task_sender

task_sender(file_path='dummy_job_files/great.py', interval=5, name='great task')

great.py has been uploaded

```

## Get all jobs
```python
$ ipython

from requests import get
HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

r = get("http://127.0.0.1:5000/jobs",headers=HEADERS)
r.json()
{u'jobs': {u'great task': {u'id': 1, u'interval': 5, u'name': u'great task'}}}

```
## DELETE a job
```python
$ ipython

from requests import delete
HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

res = delete("http://127.0.0.1:5000/jobs/1",headers=HEADERS)
```

# Limitations

- This is **just an implementation of a concept** not a product ready package.

- The scheduling is not as exclusive as cron.

- Interval can only be specified in seconds. Hours, minutes, days are not handled.

- BUGS WILL show up.

# LICENSE
MIT
