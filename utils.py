'''
Make life easier with util funcs
'''
import jsonpickle
from requests import post, delete
import cPickle
from datetime import datetime

HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def function_sender(func=None, interval=None):
    '''
        :func => function to be scheulded
        :interval => time interval in seconds
        returns job id
    '''

    if func == None or interval == None:
        print "Currect Usage\nfunction_sender(func=hello_world, interval=10)"
    else:
        data = {
                'func': cPickle.dumps(func),
                'name': func.func_name,
                'interval': interval,
                }
        
        res = post("http://127.0.0.1:5000/api/jobs",
                data=jsonpickle.encode(data),
                headers=HEADERS
                )
        print res.json()
