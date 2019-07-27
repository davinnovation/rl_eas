from hmoga import *

####################################################
'''여기서부터는 main 함수입니다.'''
# Generation parameters
gen_no=0
max_gen = 10

# Population parameters
standard_pop_size = 120
population_size = 200
next_generation_pop_size = 50

start_time = time.time()

# Step 0 Making Initial_solution
solution=[]
while len(solution) <=standard_pop_size:
    temporal_solution_set = sol(50,job_count=20,job_slot_len=120)
    for temporal_solution in temporal_solution_set:
        if temporal_solution not in solution:
            solution.append(temporal_solution)

        else:
            continue

pm_addition(solution)


# Step1~Step5
while(gen_no<max_gen):

    # Step 1 Determining non_dominated rank
    function1_values = [function1(solution[i]) for i in range(0, len(solution))]
    function2_values = [function2(solution[i]) for i in range(0, len(solution))]
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])

    # Show the solution of rank 0
    print("The best front for Generation number ", gen_no, " is")
    for valuez in non_dominated_sorted_solution[0]:
        print(function1(solution[valuez]), function2(solution[valuez]), end=" ")
        print(solution[valuez])
        pass
    print("\n")

    # Step 2.1 Generating offsprings through crossover
    child_set=[]
    while len(solution)+len(child_set) <= population_size:
        p1 = random.randint(0, len(solution) - 1)
        p2 = random.randint(0, len(solution) - 1)
        offspring = crossover(solution[p1], solution[p2])
        child_set+=offspring

    # Step 2.2 Add children_set to the solution_set
    for child in child_set:
        if child not in solution:
            solution.append(child)

        else:
            continue

    # Step 3.1 Generating optimal solution through improving
    improved_set = []
    before_calculate=[]
    for chromosome in solution:
        if np.random.rand()>0.7:
            solution_copy = chromosome.copy()
            first_imp=improving(solution_copy)

            if type(first_imp[0]) == list:
                before_calculate += first_imp
            else:
                before_calculate += [first_imp]

            for imp_sol in before_calculate:
                if calculate_total_period(imp_sol) != job_slot_len:
                    continue
                else:
                    improved_set.append(imp_sol)

        else:
            continue

#    pm_addition(improved_set)

    # Step 3.2 Add improved solution to the solution set
    for chromosome in improved_set:
        if chromosome not in solution:
            solution.append(chromosome)
        else:
            continue

    # Step 4.1 Generating a new mutated solution which has a better unavailability
    pm_mutation_set = []
    for chromosome in solution:
        if np.random.rand() > 0.3:
            pm_mutation_set.append(mutation(chromosome))

    # Step 4.2 Add pm mutated solution to the solution set
    for chromosome in pm_mutation_set:
        if chromosome not in solution:
            solution.append(chromosome)
        else:
            continue

    # Step 5.1 Finding the non_dominated rank of solutions in solution_set
    function1_values2 = [function1(solution[i]) for i in range(0, len(solution))]
    function2_values2 = [function2(solution[i]) for i in range(0, len(solution))]
    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:])
    crowding_distance_values = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        crowding_distance_values.append(crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))

    # Step 5.2 Generating next_generation_set
    new_solution = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in range(0, len(non_dominated_sorted_solution2[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values[i][:])
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0, len(non_dominated_sorted_solution2[i]))]
        front.reverse()
        for value in front:
            new_solution.append(value)
            if (len(new_solution) == next_generation_pop_size):
                break
        if (len(new_solution) == next_generation_pop_size):
            break
    next_generation = [solution[i] for i in new_solution]
    solution = next_generation

    for i in solution:
        if i.count('preventive')!=preventive_number or calculate_total_period(i)!=job_slot_len:
            solution.remove(i)

    # Step 6 Terminate_Condition
    gen_no = gen_no + 1

print("start_time",start_time)
print("--- %s seconds" %(time.time()-start_time))

print("The best front for Final Generation is")
for valuez in non_dominated_sorted_solution[0]:
    print(function1(solution[valuez]), function2(solution[valuez]), end=" ")
    print(solution[valuez])
print("\n")


function1_values = [function1(solution[i]) for i in range(0, len(solution))]
function2_values = [function2(solution[i]) for i in range(0, len(solution))]
non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])

solution_value=[]
for valuez in non_dominated_sorted_solution[0]:
    solution_value.append([function1(solution[valuez]),function2(solution[valuez])])
dataframe = pd.DataFrame(solution_value)
dataframe.to_csv("solution_value.csv",header=False,index=False)

for i in solution:
    print(calculate_total_period(i),i.count('preventive'))

print(len(solution))

