import math

""" configuration """

energy_ratio = {
    'idle' : 2,
    'turn_on' : 5,
    'turn_off' : 1,
    'job' : 4
}

JOB_COUNT = 20 # 총 작업의 개수
job_list = ['space',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
job_processing = ['space',2,3,3,3,4,3,3,3,2,2,5,2,4,3,3,2,2,3,3,2]

energy_cost_table = [19.698, 19.537, 18.34, 10.864, 10.835999999999999, 12.243, 14.84, 17.29, 17.213, 17.451, 17.234, 18.158, 13.110999999999999, 17.472, 17.549, 13.118, 10.045, 13.174000000000001, 13.405, 13.272, 13.244000000000002, 13.244000000000002, 13.132, 13.895, 12.39, 7.735, 13.895, 14.112, 14.07, 13.909, 7.651, 7.6370000000000005, 7.7, 7.735, 7.678999999999999, 6.111000000000001, 6.111000000000001, 6.146, 6.209, 19.873, 18.27, 7.832999999999999, 6.146, 6.153, 7.791, 6.1739999999999995, 6.125, 7.756, 18.809, 18.137, 18.151, 18.396, 14.07, 7.77, 7.749, 6.188, 6.1739999999999995, 14.042, 14.322000000000001, 7.756, 20.076, 7.749, 6.125, 6.117999999999999, 7.707000000000001, 10.136000000000001, 13.209000000000001, 14.924000000000001, 10.122, 10.052, 10.087, 0.917, 19.803, 15.357999999999999, 15.414000000000001, 19.558, 19.558, 18.788, 18.802, 19.635, 19.887, 20.517, 20.636, 18.368, 19.516, 19.649, 19.684, 19.712, 19.852, 19.67, 19.425, 19.67, 19.74, 20.209, 20.447, 20.839000000000002, 21.1925, 21.546, 21.8995, 22.253, 22.6065, 22.96, 23.3135, 23.666999999999998, 24.0205, 24.374000000000002, 24.7275, 25.081, 25.4345, 25.788, 26.1415, 26.495, 26.8485, 27.201999999999998, 27.5555, 27.909000000000002, 28.2625, 28.616, 28.9695, 29.323]

""" functions """

def energy_reward(job_list):
    '''
    job_list (list) : action list
    '''
    EC = 0 # energy cost
    time = 0

    for i in job_list:
        if i == 'idle': # 1 time
            EC += energy_ratio[i] * (energy_cost_table[time])
        elif i == 'turn_on': # 2 time
            time += 1
            EC += energy_ratio[i] * (energy_cost_table[time] + energy_cost_table[time-1])
        elif i == 'turn_off': # 1 time
            EC += energy_ratio[i] * energy_cost_table[time]
        elif i == 'preventive': # 1 time
            time += 1
        else: # job takes N time
            time += job_processing[i] - 1
            sumed_cost = sum([energy_cost_table[time-j] for j in range(0,job_processing[i])])
            EC += energy_ratio['job'] * sumed_cost
        time += 1
    return EC

def ma_reward(job_list): # machine availability
    '''
    job_list (list) : status list
    '''
    def calc_value(ind, m, mu=0.5, lam=0.1):
        return 1 - (mu / (lam + mu) + lam / (lam + mu) * math.exp(-(lam + mu) * (ind - m)))

    k = []
    time = 0
    m = 1

    for i in job_list:
        if i == 'turn_off_stauts':
            time += 1
            k.append(calc_value(time, m))
        elif i == 'idle':
            time += 1
            k.append(calc_value(time, m))
        elif i == 'turn_on':
            time += 2
            for t in [time-1,time]: k.append(calc_value(t, m))
        elif i == 'turn_off':
            time += 1
            k.append(calc_value(time, m))
        elif i == 'preentive':
            time += 2
            m = time
        else:
            time += job_processing[i]
            for t in range(time - (job_processing[i] - 1), time + 1):
                k.append(calc_value(time, m))

    return max(k)

def pm_addition():
    pass