'''
    Basic examples to add and delete a job.
    These are REST calls basically
'''

import jsonpickle
from requests import post, delete
import cPickle
from datetime import datetime

HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Simple job functions


def say_hello():
    print "##### Hello ##### ", datetime.strftime(datetime.now(), "%T")


def goodbye():
    print "====== Goodbye ======", datetime.strftime(datetime.now(), "%T")


def awesome_stuff():
    print "----- AWESOME -----", datetime.strftime(datetime.now(), "%T")


# sample Inputs
FUNC_DATA_1 = {
    'func': dat_awesome_stuff,
    'name': 'really_nice_stuff',
    'interval': 5,
}

FUNC_DATA_2 = {
    'func': say_hello,
    'name': 'say_hello',
    'interval': 10,
}

FUNC_DATA_3 = {
    'func': goodbye,
    'name': 'goodbye',
    'interval': 7,
    'next_runtime': None
}


FUNC_DATA_1['func'] = cPickle.dumps(FUNC_DATA_1['func'])

# Creating a job
post("http://127.0.0.1:5000/api/jobs",
     data=jsonpickle.encode(FUNC_DATA_1),
     headers=HEADERS
     )

# Delete a job
delete("http://127.0.0.1:5000/api/jobs/1",
       headers=HEADERS
       )
