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