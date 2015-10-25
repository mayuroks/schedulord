# schedulord
Scheduler as a service. Built using Python.

# Installation
```
$ git clone https://github.com/mayuroks/schedulord
$ cd schedulord
$ pip install -r requirements.txt
```

# Usage
**Start the webserver**
```
$ python server.py
```

**Start the scheduler**
```
$ python scheduler.py
```

Now we are ready to send our functions over REST API.
```python

##CREATE
from utils import function_sender

def hello_world():
    print "=== Hello World ==="

# interval is in seconds
function_sender(func=hello_world, interval=10)
{u'next_runtime': None, u'interval': 7, u'id': 1, u'func': u'c__main__\nhello\np1\n.', u'name': u'hello'}

##DELETE
from requests import delete
HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

delete("http://127.0.0.1:5000/api/jobs/1",headers=HEADERS)
```

# Limitations

- The scheduling is not as exclusive as cron.

- Interval can only be specified in seconds. Hours,minutes, days are not handled.
