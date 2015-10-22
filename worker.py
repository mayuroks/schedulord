from datetime import datetime, timedelta
from time import sleep
import cPickle
from server import STATE_FILE

jobstore = {}


while True:
    try:
        with open(STATE_FILE, 'rb') as statefile:
            jobstore = cPickle.load(statefile)
    except EOFError:
        print "[worker] State File un-inited"


    if len(jobstore) == 0:
        print "[worker] No jobs in jobstore, sleeping for 5s"
        sleep(5)
    else:
        for job_name, job in jobstore.items():
            # print "Doing job name {0}".format(job_name)
            if job['next_runtime'] == None:
                job['next_runtime'] = datetime.now() + \
                    timedelta(seconds=job['interval'])
            elif job['next_runtime'] < datetime.now():
                job['func'].__call__()
                job['next_runtime'] = datetime.now() + \
                    timedelta(seconds=job['interval'])

        time_diff = []
        for job_name, job in jobstore.items():
            time_diff.append(job['next_runtime'] - datetime.now())

        with open(STATE_FILE, 'wb') as statefile:
            cPickle.dump(jobstore, statefile)


        # print "Time diff here is ",time_diff
        SLEEP_TIME = min(time_diff).seconds

        if SLEEP_TIME < 1:
            print "[worker] sleep time less than 1"
            sleep(5)
        else:
            print "[worker] good sleep time = {0}".format(SLEEP_TIME)
            sleep(SLEEP_TIME)
