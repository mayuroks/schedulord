'''
    Flow of things
    --------------
    1) Get all jobs
    2) Unpickle the func
    3) Execute
    4) schedule next_runtime
    5) REPEAT
'''

import cPickle
from datetime import datetime, timedelta
from time import sleep
from server import Job, db

while True:
    ALL_JOBS = Job.query.all()

    if len(ALL_JOBS) == 0:
        print "[worker] No jobs in ALL_JOBS, sleeping for 5s"
        sleep(5)
    else:
        for job in ALL_JOBS:
            if job.next_runtime is None or not job.next_runtime:
                job.next_runtime = datetime.now() + \
                    timedelta(seconds=job.interval)
            elif job.next_runtime < datetime.now():
                print "[worker] executing job", job.name

                # Unpickle func b4 calling it
                job_func = cPickle.loads(str(job.func))
                job_func.__call__()
                job.next_runtime = datetime.now() + \
                    timedelta(seconds=job.interval)

        TIME_DIFF = []
        for job in ALL_JOBS:
            TIME_DIFF.append(job.next_runtime - datetime.now())

        # commit all udpated jobs to DB
        db.session.commit()

        # Just enuf sleep time to run nearest job
        SLEEP_TIME = min(TIME_DIFF).seconds

        if SLEEP_TIME < 1:
            print "[worker] sleep time less than 1"
            sleep(5)
        else:
            print "[worker] good sleep time = {0}".format(SLEEP_TIME)
            sleep(SLEEP_TIME)
