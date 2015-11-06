'''
    Flow of things
    --------------
    1) Get all jobs
    2) Execute the script
    3) schedule next_runtime
    4) REPEAT
'''

from datetime import datetime, timedelta
from time import sleep
from server import Job, db
from importlib import import_module
from site import addsitedir
from server import app

# adding script folder to site path
# enables us to import modules from 
# our upload path
addsitedir(app.config.get('UPLOAD_FOLDER'))

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

                # Get script + execute it
                job_script = import_module(job.script_name)
                job_script.main()
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
