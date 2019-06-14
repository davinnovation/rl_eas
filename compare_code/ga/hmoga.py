import math
import random
import numpy as np
import time
import pandas as pd

"""
0 : TURN OFF status - 'turn_off_status'
6 : IDLE - 'idle'
7 : TRUN ON switch - 'turn_on'
8 : TURN OFF switch - 'turn_off'
9 : Preventive
"""

JOB_COUNT = 20 # 총 작업의 개수
job_list = ['space',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
job_processing = ['space',2,3,3,3,4,3,3,3,2,2,5,2,4,3,3,2,2,3,3,2]

job_slot_len = 120 # 총 작업가용 시간의 길이 ( = 총작업시간 + 임의의 숫자(18))
cost=[19.698, 19.537, 18.34, 10.864, 10.835999999999999, 12.243, 14.84, 17.29, 17.213, 17.451, 17.234, 18.158, 13.110999999999999, 17.472, 17.549, 13.118, 10.045, 13.174000000000001, 13.405, 13.272, 13.244000000000002, 13.244000000000002, 13.132, 13.895, 12.39, 7.735, 13.895, 14.112, 14.07, 13.909, 7.651, 7.6370000000000005, 7.7, 7.735, 7.678999999999999, 6.111000000000001, 6.111000000000001, 6.146, 6.209, 19.873, 18.27, 7.832999999999999, 6.146, 6.153, 7.791, 6.1739999999999995, 6.125, 7.756, 18.809, 18.137, 18.151, 18.396, 14.07, 7.77, 7.749, 6.188, 6.1739999999999995, 14.042, 14.322000000000001, 7.756, 20.076, 7.749, 6.125, 6.117999999999999, 7.707000000000001, 10.136000000000001, 13.209000000000001, 14.924000000000001, 10.122, 10.052, 10.087, 0.917, 19.803, 15.357999999999999, 15.414000000000001, 19.558, 19.558, 18.788, 18.802, 19.635, 19.887, 20.517, 20.636, 18.368, 19.516, 19.649, 19.684, 19.712, 19.852, 19.67, 19.425, 19.67, 19.74, 20.209, 20.447, 20.839000000000002, 21.1925, 21.546, 21.8995, 22.253, 22.6065, 22.96, 23.3135, 23.666999999999998, 24.0205, 24.374000000000002, 24.7275, 25.081, 25.4345, 25.788, 26.1415, 26.495, 26.8485, 27.201999999999998, 27.5555, 27.909000000000002, 28.2625, 28.616, 28.9695, 29.323]

preventive_number= 3 # Preventive Maintenace 개수
numerator = 4 # (pm개수+1). 즉, 전체 period에서 지정된 preventive maintenace 개수를 추가하려면 개수+1의 숫자를 나눠야함.

alpha=25

'''Initial solution 생성과 관련된 코드'''
# Job 번호와 processing time을 이어주는 코드
def translate_code(code):

    ''' 이 코드는 Machine의 상태를 보기 편하게 나타내는 코드입니다'''

    if code == 'turn_off_status':
        return [0,1][1]   # [0,1]리스트에서 1번째 index의 값을 return
    elif code == 'idle':
        return [6,1][1]
    elif code == 'turn_on':
        return [7,2][1]
    elif code == 'turn_off':
        return [8,1][1]
    elif code == 'preventive':
        return [9, 2][1]
    else:
        return job_processing[code]

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

# Job과 job 사이의 빈칸을 채워주는 코드
def status_fill(job_set, start_job, end_job):
    '''Job과 Job 사이의 채워져있지 않은(임시 turn_off_status) 칸들을 합리적으로 채우는 코드'''
    for jobs in job_set:
        jobs_copy = jobs.copy()
        for job_id in range(end_job, start_job, -1):
            distance_jobs = jobs.index(job_id) - jobs.index(job_id - 1)

            if distance_jobs == 1:  # Job과 Job 사이에 빈칸이 없으면 continue
                continue
            elif 2 <= distance_jobs <= 3:  # Job과 Job 사이에 빈칸이 1개 혹은 2개이면 그냥 idle로 채움
                for i in range(1, distance_jobs):
                    jobs[jobs.index(job_id - 1) + i] = 'idle'
            else:
                for i in range(1, distance_jobs):
                    jobs_copy[jobs_copy.index(job_id - 1) + i] = 'idle'
                idle_cost = function1(jobs_copy[0:jobs_copy.index(job_id)]) - function1(jobs_copy[0:jobs_copy.index(job_id - 1) + 1])
                jobs_copy = jobs.copy()

                jobs_copy[jobs_copy.index(job_id - 1) + 1] = 'turn_off'
                del (jobs_copy[jobs_copy.index(job_id) - 1])
                jobs_copy[jobs_copy.index(job_id) - 1] = 'turn_on'
                turn_cost = function1(jobs_copy[0:jobs_copy.index(job_id)]) - function1(jobs_copy[0:jobs_copy.index(job_id - 1) + 1])

                if idle_cost > turn_cost:
                    jobs[jobs.index(job_id - 1) + 1] = 'turn_off'
                    del (jobs[jobs.index(job_id) - 1])
                    jobs[jobs.index(job_id) - 1] = 'turn_on'
                else:
                    for i in range(1, distance_jobs):
                        jobs[jobs.index(job_id - 1) + i] = 'idle'

    return job_set

# probability 부여 함수
def give_prob(list):
    prob_list =[]
    for index in list:
        prob_list.append(cost[index])

    min_cost=min(prob_list)
    for _ in range(0,len(prob_list)):
        prob_list[_]=min_cost/(prob_list[_]+list[_])

    prob_list=np.array(prob_list)
    prob_list /= prob_list.sum()

    return prob_list

# Add preventive maintenance
def pm_addition(job_set):
    
    '''이 함수는 solution 집합에 preventive maintenance를 넣는 함수입니다.'''
    #job_set: 전체 해집합

    for i in job_set:

        consecutive_turn_off = []  #연속적인 turn_off_status  있는 index 넣는 set
        pm_feasible = 1 # 현재 period가 마지막 period인지 확인해주는 값 (1씩 증가)

        while pm_feasible <= len(i)-1:  # range의 시작을 1부터 한 이유는 schedule의 시작을 maintenance로 하지 않기 위해
            if i[pm_feasible] != 'turn_off_status':
                pm_feasible+=1
                continue

            else:
                record_point = pm_feasible
                while True:
                    try:
                        if i[pm_feasible] == 'turn_off_status':
                            pm_feasible += 1
                        else:
                            if (pm_feasible - 1 - record_point) % 2 == 0:
                                record_point += 1
                                while pm_feasible - 1 >= record_point:
                                    consecutive_turn_off.append(record_point)
                                    record_point += 2
                                break
                            else:
                                record_point += 1
                                while record_point <= pm_feasible - 1:
                                    consecutive_turn_off.append(record_point)
                                    record_point += 2
                                break
                    #excpet 쓰는 이유는 pm_feasible 1씩 증가시켰을 때 solution에 마지막 요소들이 계속 turn_off_status면 index range를 초과한다.
                    except IndexError:
                        if (pm_feasible - 1 - record_point) % 2 == 0:  #왜 -1을 해줬을까
                            record_point += 1
                            while pm_feasible - 1 >= record_point:
                                consecutive_turn_off.append(record_point)
                                record_point += 2
                            break
                        else:
                            record_point += 1
                            while record_point <= pm_feasible - 1:
                                consecutive_turn_off.append(record_point)
                                record_point += 2
                            break


        '''turn_off_status에 따라 preventive maintenance를 부여한다.'''
        if len(consecutive_turn_off)==0:
            continue

        elif len(consecutive_turn_off)==1:
            i[consecutive_turn_off[0]] = 'preventive'
            del (i[consecutive_turn_off[0] - 1])

        elif len(consecutive_turn_off)==2:
            for number in range(0,len(consecutive_turn_off)):
                i[consecutive_turn_off[len(consecutive_turn_off) - 1 - number]]= 'preventive'
                del (i[consecutive_turn_off[len(consecutive_turn_off) - 1 - number] - 1])

        else:
            if len(consecutive_turn_off)<preventive_number:
                continue
            else:
                two_selection = np.random.choice(consecutive_turn_off,preventive_number, replace=False)
                two_selection.sort()
                consecutive_turn_off = two_selection.copy()
                for number in range(0,len(consecutive_turn_off)):
                    i[consecutive_turn_off[len(consecutive_turn_off)-1-number]]= 'preventive'
                    del(i[consecutive_turn_off[len(consecutive_turn_off)-1-number]-1])

    return job_set

# 현재 solution의 period 수를 계산
def calculate_total_period(jobs):
    # 현재 solution의 total period가 얼마인지 계산해준다.
    total_period = 0
    for machine_status in jobs:
        total_period += translate_code(machine_status)

    return total_period

'''목적함수 계산 함수'''
# First function to optimize
def function1(list):
    EC = 0
    k = 0

    for i in list:
        if i in job_list: # i가 만약 job이면 translate_code 함수에서 processing time을 불러온다음에 k에 더해준다
            k+=translate_code(i)
            sumed_cost = sum([cost[k-j] for j in range(1,translate_code(i)+1)])
            EC += 4 * (sumed_cost)
        elif i == 'turn_off_status':
            k += 1
        elif i == 'idle':
            k += 1
            EC += 2 * (cost[k-1])
        elif i == 'turn_on':
            k += 2
            EC += 5 * (cost[k-1] + cost[k - 2])
        elif i == 'turn_off':
            k += 1
            EC += cost[k-1]
        elif i == 'preventive':
            k += 2

    return EC

# Second function to optimize
mu=0.5
lam=0.1
def function2(list):
    k = []
    t = 0  # 실제 시간
    m = 1
    for i in list:
        if i in job_list:
            t+= translate_code(i)
            for h in range(t - (translate_code(i) + 1), t + 1):
                k.append(1 - (mu / (lam + mu) + lam / (lam + mu) * math.exp(-(lam + mu) * (h - m))))
        elif i == 'turn_off_status':
            t += 1
            k.append(1 - (mu / (lam + mu) + lam / (lam + mu) * math.exp(-(lam + mu) * (t - m))))

        elif i == 'idle':
            t += 1
            k.append(1 - (mu / (lam + mu) + lam / (lam + mu) * math.exp(-(lam + mu) * (t - m))))

        elif i == 'turn_on':
            t += 2
            for h in range(t - 1, t + 1):
                k.append(1 - (mu / (lam + mu) + lam / (lam + mu) * math.exp(-(lam + mu) * (h - m))))

        elif i == 'turn_off':
            t += 1
            k.append(1 - (mu / (lam + mu) + lam / (lam + mu) * math.exp(-(lam + mu) * (t - m))))

        elif i == 'preventive':
            t += 2
            m = t

    value1=max(k)
    return value1

'''Crossover 관련 코드'''
# Crossover
def crossover(p1, p2):
    '''Crossover 함수는 2개의 해를 선택하여 교차 연산을 하는 함수입니다.'''

    offspring_set = [] # offspring set이 들어가는 list
    offspring_list =[] # offspring이 들어가는 list

    '''energy cost가 더 작은 parent를 base solution으로 한다.'''
    if function1(p1)<function1(p2):
        base_parent = p2
        inherit_parent = p1
    else:
        base_parent = p1
        inherit_parent = p2

    '''각 job을 기준으로 crossover하는 알고리즘을 만들어 본다.'''
    job_number=1
    for job in range(1,JOB_COUNT):
        if job == job_number:
            offspring_list=base_parent[:base_parent.index(job)+1]+inherit_parent[inherit_parent.index(job+1):]
            offspring_set.append(offspring_list)
            offspring_list=[]

            job_number+=1

        else:
            continue

    repair(offspring_set)
    pm_addition(offspring_set)

    #다 추가하면 쓸데없는 해가 추가되는 느낌 다 안추가하면 너무 추가되는게 적은 느낌
    '''offspring_energy=[]
    offspring_pm=[]
    for offspring in offspring_set:
        offspring_energy.append(function1(offspring))
        offspring_pm.append(function2(offspring))

    final_offspring_set=[]
    final_offspring_set.append(offspring_set[offspring_energy.index(min(offspring_energy))])
    final_offspring_set.append(offspring_set[offspring_pm.index(min(offspring_pm))])'''

    return offspring_set

# Repair function
def repair(job_set):
    '''이 함수는 crossover에서 만들어진 offspring을 수선하는 함수입니다.'''

    for jobs in job_set:

        # jobs 내의 preventive maintenance를 전부 turn_off_status로 바꿔준다. 'preventive'가 'turn_off_status' 2개로 바뀌는 것이다. (이유: 안바꿔주면 mutation할 때 job_slot_len보다 작은 period가 결과로 나온다.)
        for status in jobs:
            if status == 'preventive':
                jobs.insert(jobs.index(status) + 1, 'turn_off_status')
                jobs[jobs.index(status)] = 'turn_off_status'

        # 현재 solution의 total period가 얼마인지 계산해준다.
        total_period = 0
        for machine_status in jobs:
            total_period += translate_code(machine_status)

        # total period가 만약 job_slot_len을 넘었을 경우
        if total_period > job_slot_len:
            delete_numbers = total_period - job_slot_len  # 제거해야하는 period 개수

            turn_off_status_index = []  # turn_off_status가 연속으로 2개가 나오는 경우 첫번째 index를 저장
            for job in range(1, len(jobs) - 2):
                if jobs[job] == 'turn_off_status' and jobs[job + 1] == 'turn_off_status' or jobs[job] == 'idle' and jobs[job + 1] == 'idle':
                    if len(turn_off_status_index) == 0:
                        turn_off_status_index.append(job)
                    elif len(turn_off_status_index) != 0 and job - turn_off_status_index[
                        len(turn_off_status_index) - 1] > 1:  # turn_off_status가 13 14 15일 때 13,14가 리스트에 들어가는 걸 방지
                        turn_off_status_index.append(job)
                    else:
                        continue

            # 제거해야하는 turn_off_status의 수만큼 제거할 수 있는 후보가 존재하는지를 체크
            if delete_numbers <= len(turn_off_status_index):
                # 제거 가능한 index 중에서 delete_numbers(제거해야하는 수만큼) 임의로 선택
                delete_chosen_period = np.random.choice(turn_off_status_index, delete_numbers, replace=False)
                delete_chosen_period.sort()

                for delete_index in range(0, len(delete_chosen_period)):
                    del jobs[delete_chosen_period[len(delete_chosen_period) - 1 - delete_index]]

            # delete_numbers의 수가 turn_off_status_index 보다 큰 경우
            else:
                #print(jobs)
                # additional_delete = 더 제거해야하는 period 수
                additional_delete = delete_numbers - len(turn_off_status_index)
                #print(additional_delete)
                # 일단 제거할 수 있는 후보의 index를 전부 제거
                for delete_index in range(0, len(turn_off_status_index)):
                    del jobs[turn_off_status_index[len(turn_off_status_index) - 1 - delete_index]]
                turn_off_status_index = []

                # 다시 jobs에서 idle이나 turn_off_status인 index를 찾는다.
                for index in range(1, len(jobs) - 1):
                    if jobs[index] == 'turn_off_status' or jobs[index] == 'idle':
                        turn_off_status_index.append(index)

                # 제거 가능한 index 중에서 delete_numbers(제거해야하는 수만큼) 임의로 선택
                delete_chosen_period = np.random.choice(turn_off_status_index, additional_delete, replace=False)
                delete_chosen_period.sort()

                for delete_index in range(0, len(delete_chosen_period)):
                    del jobs[delete_chosen_period[len(delete_chosen_period) - 1 - delete_index]]

        # total period 와 job_slot_len이 같은 경우
        elif total_period - job_slot_len == 0:
            continue

        # 만약 total_period의 값이 더 작은 경우 부족한 period 수만큼 뒤에 turn_off_status를 붙여라.
        else:
            need_numbers = job_slot_len - total_period
            for add in range(0, need_numbers):
                jobs.append('turn_off_status')

    #PM 개수에 대한 repair 해준다.
    pm_repair(job_set)

    ''' 이 파트는 solution이 제대로 repair 되었는지 확인해줍니다.'''
    for jobs in job_set:
        if calculate_total_period(jobs) != job_slot_len:
            print(jobs)
            print('Repair has a problem!!')

    return job_set

# Preventive maintenance에 대한 repair 실행
def pm_repair(job_set):
    ''' Preventive maintenace의 수가 원하는 수를 초과했을 경우 삭제'''
    for jobs in job_set:
        pm_index_set = []
        if jobs.count('preventive') > preventive_number:
            # Preventive Maintenace인 index 전부 저장
            for index in range(0, len(jobs)):
                if jobs[index] == 'preventive':
                    pm_index_set.append(index)

            #초과한 분만큼 preventive maintenace를 제거하고 그에 대한 index를 구한다.
            save_index = []
            pm_index = 0
            while jobs.count('preventive') != preventive_number:
                jobs[pm_index_set[pm_index]] = 'turn_off_status'
                save_index.append(pm_index_set[pm_index])
                pm_index += 1

            #Preventive Maintenace는 2칸짜리이므로 turn_off_status를 하나 더 추가
            for index in range(0, len(save_index)):
                jobs.insert(save_index[len(save_index) - 1 - index], 'turn_off_status')

        else:
            continue

'''Improving 관련 코드'''
def improving(jobs):
    '''해를 mutate 하는 코드입니다.'''
    jobs_set = []
    jobs_set.append(jobs)
    fallback=jobs.copy()
    # jobs 내의 preventive maintenance를 전부 turn_off_status로 바꿔준다. 'preventive'가 'turn_off_status' 2개로 바뀌는 것이다. (이유: 안바꿔주면 mutation할 때 job_slot_len보다 작은 period가 결과로 나온다.)
    for status in jobs:
        if status == 'preventive' or status == 'turn_on':
            jobs.insert(jobs.index(status) + 1, 'turn_off_status')
            jobs[jobs.index(status)] = 'turn_off_status'

    job_number = 1  # 현재 Job의 number
    start_job = 0  # status_fill 함수를 실행하기 위해 job의 범위를 지정해주는것
    end_job = 1  # end_job 부터 start_job 사이의 공간을 채운다.
    turn_on_count = 0  # mutate 해에서 turn on이 발생하면 기존 job 해에서 turn_off_status 삭제해주기 위해 turn_on 개수 기록

    # mutate 된 완전한 해를 기록하기 위한 집합
    mutated_jobs = []

    # mutation을 하는 코드
    while job_number <= JOB_COUNT:

        if job_number == 1:

            # Job1에 대해 Mutate 된 해들을 모으기 위한 set
            job1_mutation_set = []

            # Job1의 위치가 period 2이고 그 뒤에 바로 Job2가 뒤따르는 경우 (즉, Job1의 위치를 변경할 수 없는 상태)
            if jobs.index(job_number) == 1 and jobs.index(job_number + 1) == 2:

                # 만약 위치를 변경할 수 없는 상태이면 원래 부분을 return
                mutated_jobs += [jobs[:jobs.index(job_number) + 1]]

            # Job1의 위치가 period 2이고 Job2와 최소 한 칸(1 period) 이상 떨어져 있는 상태 (즉, Job1이 뒤로밖에 움직일 수 없다.)
            elif jobs.index(job_number) == 1 and jobs.index(job_number + 1) != 2:

                start_point = jobs.index(job_number)
                end_point = jobs.index(2)

                job_moving(jobs, job_number, start_point, end_point, job1_mutation_set, mutated_jobs)

                try:
                    mutated_jobs += [np.random.choice(job1_mutation_set,1,replace=False)[0]]
                except ValueError:
                    mutated_jobs +=[job1_mutation_set[0]]


            # Job1의 위치가 period2가 아니고 Job1 뒤에 바로 Job2가 뒤따르는 상태 (즉, Job1이 앞으로만 움직일 수 있다.)
            elif jobs.index(job_number) != 1 and jobs.index(job_number + 1) == jobs.index(job_number) + 1:

                start_point = 2
                end_point = jobs.index(job_number) + 1

                job_moving(jobs, job_number, start_point, end_point, job1_mutation_set, mutated_jobs)

                try:
                    mutated_jobs += [np.random.choice(job1_mutation_set,1,replace=False)[0]]
                except ValueError:
                    mutated_jobs +=[job1_mutation_set[0]]


            # Job1의 위치가 period 2가 아니고 Job2가 바로 뒤따르지 않는 상태 (즉, Job1이 앞 뒤로 다 움직일 수 있다.)
            else:
                # Job1의 위치가 앞뒤로 움직일 수 있으므로 움직일 수 있는 범위를 지정해준다. (시작은 1 period부터 job2 직전 period까지)
                start_point = 1
                end_point = jobs.index(2)

                # Job1의 위치를 옮겨가며 mutate된 파트를 job1_mutation_set에 기록
                job_moving(jobs, job_number, start_point, end_point, job1_mutation_set, mutated_jobs)

                # job1의 위치가 매우 중요하므로 이를 랜덤으로 정한다. 다만 choice 함수가 표본이 1개이면 에러가 발생하기에 표본이 1개이면 그냥 그 1개를 선택해주는 것으로 한다.
                try:
                    mutated_jobs += [np.random.choice(job1_mutation_set,1,replace=False)[0]]
                except ValueError:
                    mutated_jobs +=[job1_mutation_set[0]]


        elif job_number == JOB_COUNT:

            job_number_energy = list(map(lambda energy1: function1(energy1), mutated_jobs))
            mutated_jobs = cost_compare(job_number_energy, mutated_jobs)

            before_mutated_jobs = []

            for part_solution in mutated_jobs:
                JOB_COUNT_mutation_set = []

                # 만약 last job이 앞뒤로 움직일 수 없는 경우
                if jobs.index(job_number) - 1 == part_solution.index(job_number - 1) and jobs.index(job_number) == len(jobs) - 2:
                    part_solution = part_solution + jobs[part_solution.index(job_number - 1) + 1:jobs.index(job_number) + 1]
                    before_mutated_jobs.append(part_solution)

                # 만약 last job이 앞으로만 움직일 수 있는 경우
                if jobs.index(job_number) - 1 != part_solution.index(job_number - 1) and jobs.index(job_number) == len(jobs) - 2:
                    start_point = part_solution.index(job_number - 1) + 1
                    end_point = jobs.index(job_number) + 1

                    job_moving(jobs, job_number, start_point, end_point, JOB_COUNT_mutation_set, part_solution)

                    status_fill(JOB_COUNT_mutation_set, start_job, end_job)

                    fill_toff(JOB_COUNT_mutation_set)

                    job_count_energy = list(map(lambda energy1: function1(energy1), JOB_COUNT_mutation_set))

                    before_mutated_jobs += cost_compare(job_count_energy, JOB_COUNT_mutation_set)

                # 만약 last job이 뒤로만 움직일 수 있는 경우
                if jobs.index(job_number) - 1 == part_solution.index(job_number - 1) and jobs.index(job_number) != len(jobs) - 2:
                    start_point = jobs.index(job_number)
                    end_point = len(jobs) - 1

                    job_moving(jobs, job_number, start_point, end_point, JOB_COUNT_mutation_set, part_solution)

                    status_fill(JOB_COUNT_mutation_set, start_job, end_job)

                    fill_toff(JOB_COUNT_mutation_set)

                    job_count_energy = list(map(lambda energy1: function1(energy1), JOB_COUNT_mutation_set))

                    before_mutated_jobs += cost_compare(job_count_energy, JOB_COUNT_mutation_set)

                # 만약 last job이 앞뒤로 전부 움직일 수 있는 경우
                if jobs.index(job_number) - 1 != part_solution.index(job_number - 1) and jobs.index(job_number) != len(jobs) - 2:
                    start_point = part_solution.index(job_number - 1) + 1
                    end_point = len(jobs) - 1

                    job_moving(jobs, job_number, start_point, end_point, JOB_COUNT_mutation_set, part_solution)

                    status_fill(JOB_COUNT_mutation_set, start_job, end_job)

                    fill_toff(JOB_COUNT_mutation_set)

                    job_count_energy = list(map(lambda energy1: function1(energy1), JOB_COUNT_mutation_set))

                    before_mutated_jobs += cost_compare(job_count_energy, JOB_COUNT_mutation_set)

            mutated_jobs = []
            for part in before_mutated_jobs:
                if type(part) == int:
                    continue
                else:
                    if part in mutated_jobs:
                        continue
                    else:
                        mutated_jobs.append(part)

        else:
            job_number_energy = list(map(lambda energy1: function1(energy1), mutated_jobs))
            mutated_jobs = cost_compare(job_number_energy, mutated_jobs)

            jobs = jobs_set[part_solution.count('turn_on')]

            before_mutated_jobs =[]
            for part_solution in mutated_jobs:

                jobs = jobs_set[part_solution.count('turn_on')]

                # Middle Job들에 대해 Mutate 된 해들을 모으기 위한 set
                middle_job_mutation_set = []

                # 마지막 job을 turn_off한 뒤에 turn_off_status가 몇개 있는지 확인
                toffs_count_in_end_period = jobs[jobs.index(JOB_COUNT):].count('turn_off_status')

                # 현재 job x의 앞뒤로 job x-1와 job x+1가 배치되어 있는경우 움직일 수 없음.
                if jobs.index(job_number) - 1 == part_solution.index(job_number - 1) and jobs.index(job_number) + 1 == jobs.index(job_number + 1):

                    # mutated jobs (job x-1까지 있는 해)과 현재 jobs에서 mutated jobs의 job x-1 index에서 현재 jobs의 job까지의 index를 복사하여 합친다.
                    part_solution = part_solution + jobs[part_solution.index(job_number - 1) + 1:jobs.index(job_number) + 1]
                    before_mutated_jobs.append(part_solution)

                # Job x 앞에 바로 Job x-1이 존재하고 Job x 뒤에 job x+1이 바로 뒤따르지 않는 경우 (즉, Job x가 뒤로밖에 움직일 수 없다.)
                elif jobs.index(job_number) - 1 == part_solution.index(job_number - 1) and jobs.index(job_number) + 1 != jobs.index(job_number + 1):
                    (jobs, part_solution) = mutate_procedure(jobs, part_solution, job_number, middle_job_mutation_set,toffs_count_in_end_period, start_job, end_job)
                    before_mutated_jobs+=part_solution

                # Job x 앞에 바로 Job x-1이 존재하지 않고 Job x 뒤에 바로 Job x+1이 뒤따르는 상태 (즉, Job x가 앞으로만 움직일 수 있다.)
                elif jobs.index(job_number) - 1 != part_solution.index(job_number - 1) and jobs.index(job_number) + 1 == jobs.index(job_number + 1):
                    (jobs, part_solution) = mutate_procedure(jobs, part_solution, job_number, middle_job_mutation_set,toffs_count_in_end_period, start_job, end_job)
                    before_mutated_jobs += part_solution

                # Job x의 전후에 다른 Job이 없는 상태  (즉, Job x가 앞 뒤로 다 움직일 수 있다.)
                else:
                    (jobs, part_solution) = mutate_procedure(jobs, part_solution, job_number, middle_job_mutation_set,
                                                            toffs_count_in_end_period, start_job, end_job)
                    before_mutated_jobs += part_solution

                # 원래 jobs에서 맨 뒤에 turn_off_status를 앞으로 땡겨왔다면 실제 jobs에서도 앞에 turn_off_status를 추가해주자. 이때, 꼭 turn_off_status가 아닌 임의의 요소라도 된다.
                if toffs_count_in_end_period != jobs[jobs.index(JOB_COUNT):].count('turn_off_status'):
                    add_count = toffs_count_in_end_period - jobs[jobs.index(JOB_COUNT):].count('turn_off_status')
                    while add_count != 0:
                        jobs.insert(0, 0)  # turn_off_status 대신한 임의의 요소 0
                        add_count -= 1

            mutated_jobs=[]
            for part in before_mutated_jobs:
                if type(part) == int:
                    continue
                else:
                    if part in mutated_jobs:
                        continue
                    else:
                        mutated_jobs.append(part)


        # 여기에 원래 job에서 toffs를 삭제하는 코드를 하나 추가하자.
        for part_solution in mutated_jobs:
            if part_solution.count('turn_on') <= turn_on_count:
                continue
            else:
                del_count = part_solution.count('turn_on') - turn_on_count
                while del_count != 0:
                    del jobs[0]
                    del_count -= 1
                jobs_set.append(jobs)
            turn_on_count = part_solution.count('turn_on')

        job_number += 1
        start_job += 1
        end_job += 1

        if len(mutated_jobs)==0:
            return fallback

    return mutated_jobs

def fill_toff(mutation_set):
    '''이 함수는 JOB_COUNT 이후에 바로 turn_off 를 하게 만들어준다. JOB_COUNT 직후의 turn_off 이후의 상태는 모드 turn_off_status로 만들어준다.'''
    for mutation_solution in mutation_set:
        # JOB_COUNT 다음에 바로 turn_off를 만들어줘야하기 때문에 JOB_COUNT에 1을 더해준다.
        toff_insert_index = mutation_solution.index(JOB_COUNT) + 1
        mutation_solution[toff_insert_index] = 'turn_off'

        #JOB_COUNT 직후의 상태를 모두 turn_off_status로 만든다.
        for index in range(toff_insert_index+1,len(mutation_solution)):
            mutation_solution[index] = 'turn_off_status'

    return mutation_solution

def job_moving(jobs, job_number, start_point, end_point,job_mutation_set, mutated_jobs):
    if job_number ==1:
        for index in range(start_point, end_point):
            jobs_copy = jobs.copy()

            # 기존 Job1과 turn on index를 turn_off_status로 변경
            jobs_copy[jobs_copy.index(job_number)] = 'turn_off_status'
            #jobs_copy[jobs_copy.index('turn_on')] = 'turn_off_status'


            # 바뀌는 파트의 index를 Job1과 그 전 index를 turn_off_status로 변경
            jobs_copy[index] = 1
            jobs_copy[index - 1] = 'turn_on'
            del jobs_copy[index - 2]
            job_mutation_set.append(jobs_copy[0:jobs_copy.index(job_number)+1])

    elif job_number == JOB_COUNT:
        # 지금까지의 mutate 된 solution을 복사
        toffs_add_mutated_jobs = mutated_jobs.copy()

        # 현재 job number에서 이전 job number사이의 distance만큼 turn_off_status를 추가
        for times in range(end_point - start_point):
            toffs_add_mutated_jobs.append('turn_off_status')

        # 위의 추가된 turn off_status를 차례로 job_number로 바꾸어 저장
        for index in range(start_point, end_point):
            jobs_copy = toffs_add_mutated_jobs.copy()

            # 바뀌는 파트의 index를 Job1과 그 전 index를 turn_off_status로 변경
            jobs_copy[index] = job_number
            job_mutation_set.append(jobs_copy+jobs[end_point:len(jobs)])

    else:
        #지금까지의 mutate 된 solution을 복사
        toffs_add_mutated_jobs = mutated_jobs.copy()

        #현재 job number에서 이전 job number사이의 distance만큼 turn_off_status를 추가
        for times in range (end_point-start_point):
            toffs_add_mutated_jobs.append('turn_off_status')

        #위의 추가된 turn off_status를 차례로 job_number로 바꾸어 저장
        for index in range(start_point, end_point):
            jobs_copy = toffs_add_mutated_jobs.copy()

            # 바뀌는 파트의 index를 Job1과 그 전 index를 turn_off_status로 변경
            jobs_copy[index] = job_number
            job_mutation_set.append(jobs_copy[0:jobs_copy.index(job_number) + 1])

    return job_mutation_set

def mutate_procedure(jobs,mutated_jobs,job_number,middle_job_mutation_set,toffs_count_in_end_period,start_job, end_job):
        start_point = mutated_jobs.index(job_number - 1) + 1
        end_point = jobs.index(job_number + 1)
        if start_point>end_point:
            return (jobs,[0])
        else:

            job_moving(jobs, job_number, start_point, end_point, middle_job_mutation_set, mutated_jobs)

            if len(middle_job_mutation_set)==0:
                return (jobs, [0])

            else:
                # jobs 끝에 있는 turn_off_status 개수만큼 현재 mutated solution 중간에 끼워넣어본다. (끝에 3개가 있으면 1개, 2개, 3개가 중간에 넣어진 solution 3개가 만들어짐)
                for add_toffs_in_middle in range(toffs_count_in_end_period):
                    last_solution_of_middle_mutation = middle_job_mutation_set[len(middle_job_mutation_set) - 1].copy()  # 현재 middle_job_set의 마지막 해를 copy
                    last_solution_of_middle_mutation.insert(len(last_solution_of_middle_mutation) - 2,'turn_off_status')  # job_number 바로 앞 지점에 turn_off_status를 끼워넣음
                    middle_job_mutation_set.append(last_solution_of_middle_mutation)  # 이를 middle_job_mutation_set에 붙여넣음


                status_fill(middle_job_mutation_set, start_job, end_job)
                job_number_energy = list(map(lambda energy1: function1(energy1), middle_job_mutation_set))
                mutated_jobs = cost_compare(job_number_energy, middle_job_mutation_set)

                # mutate 된 solution 집합
                added_mutates = middle_job_mutation_set[len(middle_job_mutation_set) - toffs_count_in_end_period:len(middle_job_mutation_set)]

                # 현재 선택된 mutate solution이  added_mutates 집합에 있으면 맨뒤의 turn_off_status들이 앞으로 당겨진 것이기 때문에 원래 jobs에서 이를 삭제
                for mutated in added_mutates:
                    if mutated_jobs == mutated:
                        for delete in range(added_mutates.index(mutated) + 1):
                            jobs.pop()

                    else:
                        continue

                return jobs, mutated_jobs

def cost_compare(energy_list,job_mutation_set):
    try:
        candidate_job_sets = []
        minimum_energy = min(energy_list)
        #기존 mutate set에서 energy가 최소인 것들을 고름
        for index in range(0,len(energy_list)):
            if abs(minimum_energy-energy_list[index])<=alpha:
                candidate_job_sets.append(job_mutation_set[index])
            else:
                continue

        #energy_list에 이제 원래 job 위치의 코스트가 들어가기 때문에 주석코드, 즉 원래 jobs와 에너지 비교해줄 필요 없음 만약 원래 job이 제일 좋다면 그것이 선택될 것이다.
        return  candidate_job_sets

    except ValueError:
        return [0]

'''Mutation 관련 코드'''
def mutation(solution):
    '''Preventive maintenance의 위치를 기존보다 좋은 곳으로 이동시켜 machine unavailability를 낮추는 코드'''
    jobs = solution.copy()
    # jobs 내의 preventive maintenance를 전부 turn_off_status로 바꿔준다. 'preventive'가 'turn_off_status' 2개로 바뀌는 것이다. (이유: 안바꿔주면 mutation할 때 job_slot_len보다 작은 period가 결과로 나온다.)
    for status in jobs:
        if status == 'preventive':
            jobs.insert(jobs.index(status) + 1, 'turn_off_status')
            jobs[jobs.index(status)] = 'turn_off_status'

    # Turn_off 와 Turn on point를 기록하는 list
    start_point = []
    end_point = []

    # Turn_off에서 Turn_on 사이의 요소를 끄집어내서 기록하는 list
    mutation_list =[]

    while True:
        # Turn off ~ Turn on status의 위치를 기록. 이때, range 시작 지점은 job1 부터 마지막 job까지.
        for status in range(jobs.index(job_list[1]),jobs.index(len(job_list)-1)):
            if jobs[status] == 'turn_off':
                start_point.append(status)

            elif jobs[status] == 'turn_on':
                end_point.append(status)

            else:
                continue

        # 원하는 구간을 따로 뽑음
        for point in range(0,len(start_point)):
            mutation_list.append(jobs[start_point[point]:end_point[point]+1])

        # 만약 mutation list에 있는 요소중 preventive maintenance를 넣기에 적절치 않다면 제거, 4의 의미는 (toff toffs toffs ton)
        for factor in mutation_list:
            if len(factor)<4:
                mutation_list.remove(factor)
            else:
                continue

        # 만약 원하는 구간이 없다면 그냥 원래 job 리턴
        if len(mutation_list) != preventive_number:
            return solution

        # 원하는 구간을 새로 배치하기 위해 기존 jobs에 있던 구간을 지움
        for point in range(0, len(start_point)):
            for del_point in range(end_point[len(end_point)-point-1],start_point[len(start_point)-point-1]-1,-1):
                del jobs[del_point]

        break

    # 끄집어낸 mutation list에서 turn off 다음에 바로 preventive maintenace 추가
    for mutation in mutation_list:
        mutation[1]='preventive'
        del mutation[2]

    # 원래 jobs list에서 어디에다가 mutation을 추가시켜줄건지 계산
    mutated={}
    start_status=0
    end_status=len(jobs)
    for number in range(0,len(mutation_list)):

        #원래 jobs에서 job과 job+1 맞붙어 있을때 mutation 추가 가능. job까지의 peirod 계산한다음에 어느 것이 최적의 장소인지 정함
        for status in range(start_status,end_status):
            if jobs[status] in job_list and jobs[status+1] in job_list:
                # 2를 더해준 이유는 job 다음에 turn off 그다음에 바로 preventive maintenace일것이기 때문. 뒤에 int는 원래의 최적의 장소 이 차이가 작은 것을 택해준다.
                mutated[jobs[status]]=calculate_total_period(jobs[0:status+1])+2-int(job_slot_len*(1+number)/numerator)

            else:
                continue

        # 다만 음수인 장소는 제외 양수인 장소만 고려
        key_number=list(mutated.keys())[0]

        while mutated[key_number]<0:

            if len(mutated)==1:
                break

            if mutated[key_number]<0:
                del mutated[key_number]

            while True:
                if key_number in mutated.keys():
                    break
                else:
                    key_number+=1


        # 차이가 가장 작은 job을 고른다.
        standard_insertion = find_key(mutated)

        # 해당 job 다음 장소에 mutation을 넣어준다.
        jobs = jobs[0:jobs.index(standard_insertion) + 1] + mutation_list[number] + jobs[jobs.index(standard_insertion) + 1:]
        mutated={}
        end_status = len(jobs)

    return jobs

def find_key(dic):
    min_value=min(dic.values())

    for job, proper_period in dic.items():
        if proper_period == min_value:
            return job


'''기존 NSGA-ii 코드'''
# Function to find index of list
def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

# Function to sort by values
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list

# Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0,len(values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(values1)):
            if (values1[p] < values1[q] and values2[p] < values2[q]) or (values1[p] <= values1[q] and values2[p] < values2[q]) or (values1[p] < values1[q] and values2[p] <= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] < values1[p] and values2[q] < values2[p]) or (values1[q] <= values1[p] and values2[q] < values2[p]) or (values1[q] < values1[p] and values2[q] <= values2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]
    return front

# Function to calculate crowding distance
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ abs((values1[sorted1[k+1]] - values1[sorted1[k-1]])) + abs((values2[sorted2[k+1]] - values2[sorted2[k-1]]))
    return distance

