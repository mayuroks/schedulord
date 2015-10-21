from datetime import datetime, timedelta
from time import sleep
import cPickle
from server import STATE_FILE

jobstore = {}
try:
    with open(STATE_FILE, 'rb') as statefile:
        jobstore = cPickle.load(statefile)
except EOFError:
    print "State File un-inited"


while True:
    if len(jobstore) == 0:
        print "[worker] No jobs in jobstore, sleeping for 5s"
        sleep(5)
    else:
        for job in jobstore:
            if job['next_runtime'] == datetime.now():
                job['func'].__call__()
                job['next_runtime'] = datetime.now + \
                    timedelta(seconds=job['interval'])

        time_diff = []
        for job in jobstore:
            time_diff.append([job['next_runtime'] - datetime.now()])

        with open(STATE_FILE, 'wb') as statefile:
            cPickle.dump(jobstore, statefile)
        sleep(min(time_diff))
