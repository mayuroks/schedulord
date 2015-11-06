'''
Make life easier with util funcs
'''
from requests import post, delete


def task_sender(name=None, file_path=None, interval=None):
    '''
        :name => name of task
        :file_path => '/path/to/your_script.py'
        :interval => time interval in seconds
        returns job id
    '''

    if not all([name,file_path,interval]):
        print "Currect Usage:\nfunction_sender(name='my_task',file_path='/path/to/hello.py', interval=10)"
    else:
        files = {'file': open(file_path, 'rb')}
        job_data = dict(name=name, interval=interval)
        url = "http://127.0.0.1:5000/jobs/create"
        res = post(url=url, data=job_data, files=files)
        print res.text
