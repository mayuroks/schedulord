from requests import get, post, patch
import cPickle
import json
from datetime import datetime, timedelta
from time import sleep

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}


def json_to_pickle(job):
    job['func'] = cPickle.loads(str(job['func']))
    return job


def get_all_jobs():
    # contents of res its all json
    res = get('http://127.0.0.1:5000/api/jobs')
    # need to convert the function to python object
    return map(json_to_pickle, res.json()['objects'])


while True:
    all_jobs = get_all_jobs()
    all_jobs_dict = {}

    # all_jobs_dict is prepared
    for job in all_jobs:
        if job['next_runtime'] is not None:
            job['next_runtime'] = datetime.strptime(
                job['next_runtime'], "%Y-%m-%d %H:%M:%S.%f")
        all_jobs_dict[job['name']] = job

    # print "[worker] all jobs dict", all_jobs_dict
    updated_jobs = []
    if len(all_jobs_dict) == 0:
        print "[worker] No jobs in all_jobs_dict, sleeping for 5s"
        sleep(5)
    else:
        for job_name, job in all_jobs_dict.items():
            if job['next_runtime'] == None:
                job['next_runtime'] = datetime.now() + \
                    timedelta(seconds=job['interval'])

                # update job details
                all_jobs_dict[job_name] = job
                # print "[worker] job looks like", job
                updated_jobs.append(job)
            elif job['next_runtime'] < datetime.now():
                print "[worker] executing job", job_name
                job['func'].__call__()
                job['next_runtime'] = datetime.now() + \
                    timedelta(seconds=job['interval'])

                # update job details
                all_jobs_dict[job_name] = job
                updated_jobs.append(job)

        # print "Updated jobs", updated_jobs_json
        # print "[worker] All jobs dict", all_jobs_dict

        # print "[worker] All jobs dict", all_jobs_dict
        time_diff = []
        for job_name, job in all_jobs_dict.items():
            time_diff.append(job['next_runtime'] - datetime.now())

        for job in updated_jobs:
            job['func'] = cPickle.dumps(job['func'])
            job['next_runtime'] = str(job['next_runtime'])
            url = 'http://127.0.0.1:5000/api/jobs/' + str(job['id'])
            res = patch(url=url, data=json.dumps(job), headers=headers)
            print "[worker] Updated jobs. Response code ", res.status_code

        # patch('http://127.0.0.1:5000/api/jobs', data=json.dumps(updated_jobs_json), headers=headers)

        # Just enuf sleep time to run nearest job
        SLEEP_TIME = min(time_diff).seconds

        if SLEEP_TIME < 1:
            print "[worker] sleep time less than 1"
            sleep(5)
        else:
            print "[worker] good sleep time = {0}".format(SLEEP_TIME)
            sleep(SLEEP_TIME)
