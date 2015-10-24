from requests import get,post,patch
import cPickle
import json
from datetime import datetime,timedelta
from time import sleep
from app import Job,db
# Flow of things
# 1) Get job
# 2) Unpickle the func
# 3) Execute and schedule next_run
# 4) Pickle func n store in DB


while True:
    all_jobs = Job.query.all()
    all_jobs_dict = {}

    # all_jobs_dict is prepared
    for job in all_jobs:
        if job.next_runtime is not None:
            # If the next_runtime is none set it to NOW
            job.next_runtime = datetime.now()
        all_jobs_dict[job.name] = job

    # print "[worker] all jobs dict", all_jobs_dict
    if len(all_jobs_dict) == 0:
        print "[worker] No jobs in all_jobs_dict, sleeping for 5s"
        sleep(5)
    else:
        for job_name, job in all_jobs_dict.items():
            if job.next_runtime == None:
                job.next_runtime = datetime.now() + \
                    timedelta(seconds=job.interval)

                # update job next run
                all_jobs_dict[job_name] = job
            elif job.next_runtime < datetime.now():
                print "[worker] executing job", job_name

                # Unpickle func b4 calling it
                job_func = cPickle.loads(str(job.func))
                job_func.__call__()
                job.next_runtime = datetime.now() + \
                    timedelta(seconds=job.interval)

                # update job next run
                all_jobs_dict[job_name] = job
        
        
        # print "[worker] All jobs dict", all_jobs_dict
        time_diff = []
        for job_name, job in all_jobs_dict.items():
            time_diff.append(job.next_runtime - datetime.now())

        # commit all udpated jobs to DB
        db.session.commit()

        # Just enuf sleep time to run nearest job
        SLEEP_TIME = min(time_diff).seconds

        if SLEEP_TIME < 1:
            print "[worker] sleep time less than 1"
            sleep(5)
        else:
            print "[worker] good sleep time = {0}".format(SLEEP_TIME)
            sleep(SLEEP_TIME)
