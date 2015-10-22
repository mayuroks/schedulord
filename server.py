from flask import Flask, request
import jsonpickle
import cPickle
from datetime import datetime, timedelta
app = Flask(__name__)

STATE_FILE = '/tmp/statefile.pickle'


@app.route('/')
def index():
    '''
    Show all jobs
    '''
    pass


@app.route('/create', methods=['POST'])
def create():
    '''
    POST
    create new job
    job = {
            'func': myfunc
            'name': 'myfunc is awesome'
            'interval': 5 #secs
            'next_runtime': datetime shit
        }
    '''
    if request.method == 'POST':
        # recieve a job hash
        job = jsonpickle.decode(request.data)
        # set the next_runtime
        job['next_runtime'] = datetime.now(
        ) + timedelta(seconds=job['interval'])

        with open(STATE_FILE, 'rb') as statefile:
            jobstore = cPickle.load(statefile)

        with open(STATE_FILE, 'wb') as statefile:
            jobstore[job['name']] = job
            cPickle.dump(jobstore, statefile)

    return "function submitted", 201


@app.route('/edit/<id>', methods=['POST'])
def edit(id):
    '''
    Edit existing job
    '''
    pass


@app.route('/delete/<id>', methods=['POST'])
def delete():
    '''
    POST
    Delete a job
    '''
    pass


@app.route('/<id>')
def show(id):
    '''
    GET
    get a job with job id
    '''
    pass

if __name__ == "__main__":
    # start with empty job store
    jobstore = {}
    with open(STATE_FILE, 'wb') as statefile:
        cPickle.dump(jobstore, statefile)
    app.run(debug=True)
