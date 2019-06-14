import math
import random
import numpy as np
import time
import pandas as pd

from configuration import *

# Define Initial solution
def sol(init_job_set, job_count, job_slot_len):

    ''' sol함수는 초기해를 만드는데 사용되는 함수입니다.
    init_job_set = 초기해 개수, job_count = 총 작업의 개수'''

    job_set = []  # 초기해들을 포함하고 있는 리스트
    for _ in range(init_job_set):
        jobs = []
        for _ in range (job_slot_len):
            jobs.append('turn_off_status')

        job_set.append(jobs)

    '''초기해에서 Job을 energy cost에 따라 배치하는 방법'''
    for jobs in job_set:
        job_number = 1
        start_available_point=2
        left_processing_time = 57       #작업의 총
        job_available_index = []        #현재 job이 들어갈 수 있는 가용한 period의 index
        available_period = job_slot_len-1-left_processing_time   # 총시간-3(shutdown과 turn_off)-left_processing(남은 processing 시간)에서 +1 한 period부터 시작하면 된다.
        for job in job_list:
            if job == job_number:
                for index in range(start_available_point,available_period+1):
                    job_available_index.append(index)
                job_index=np.random.choice(job_available_index,1,replace=False,p=give_prob(job_available_index))[0]
                jobs[job_index]=job

                start_available_point=job_index+job_processing[job]
                left_processing_time-=job_processing[job]
                available_period+=job_processing[job]
                job_available_index=[]


                job_number+=1

            else:
                continue

    '''Job processing time에 따라 바로 뒤따르는 turn_off_status를 지우는것'''
    for jobs in job_set:
        job_number=1
        for job in job_list:
            if job ==job_number:
                for processing_time in range(1,job_processing[job]):
                    del jobs[jobs.index(job)+1]


                job_number+=1

            else:
                continue

    '''Job1 시작 전에 turn on, job n 가공후 turn off 배치'''
    for jobs in job_set:
        for job_id in jobs:
            if job_id == 1:
                if jobs.index(job_id) == 0:
                    job_set[0]=['turn_off_status', 'turn_on'] + jobs
                    break
                elif jobs.index(job_id) == 1:
                    jobs.insert(1,'turn_on')
                    break
                elif jobs.index(job_id) == 2:
                    jobs[1]='turn_on'
                    del(jobs[0])
                else:
                    jobs[jobs.index(job_id) - 1] = 'turn_on'
                    del (jobs[jobs.index(job_id) - 2])
            elif job_id == job_count:
                jobs[jobs.index(job_id) + 1] = 'turn_off'

    start_job = 1
    end_job = JOB_COUNT
    status_fill(job_set, start_job, end_job)

    return job_set