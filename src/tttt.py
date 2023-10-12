import random


def regret2_Ins(customer, pro_tmp, current_route, num_pair, routes_pool, pre_wt):
    # 计算将顾客插入当前路线中的成本
    insertion_costs = calculate_insertion_costs(customer, current_route)

    # Find the best and second best insertion costs
    best_cost_idx = min(range(len(insertion_costs)), key=insertion_costs.__getitem__)
    best_cost = insertion_costs[best_cost_idx]

    # Remove the best cost to find the second best
    insertion_costs.pop(best_cost_idx)
    if insertion_costs:
        second_best_cost = min(insertion_costs)
    else:
        second_best_cost = best_cost
    # 计算遗憾值
    regret = second_best_cost - best_cost

    # 复制当前路线以创建一个最佳路线的副本
    optimal_route = current_route.copy()
    # Insert the customer at the best position in the route
    optimal_route.insert(best_cost_idx, customer)

    return regret, optimal_route, routes_pool

def generate_solution_for_single_vehicle(bank, pro_tmp, routes_pool, pre_wt):
    vehicle_route = []# 初始化车辆路径为空
    while len(bank) != 0 and len(vehicle_route) < 4: # 当还有顾客未服务时
        cur_max = float('-inf') # 当前最大的“遗憾值”
        best_customer_idx = -1# 最佳顾客的索引
        best_vehicle_route = None# 最佳车辆路径

        for i in range(len(bank)): # 遍历未被访问的顾客
            # 调用regret2_Ins函数获取当前顾客的“遗憾值”，潜在路径和更新后的路径池
            dif, potential_route, routes_pool = regret2_Ins(bank[i], pro_tmp, vehicle_route, len(bank), routes_pool, pre_wt)

            if dif > cur_max:# 如果当前“遗憾值”更大
                cur_max = dif# 更新最大“遗憾值”
                best_vehicle_route = potential_route# 更新最佳车辆路径
                best_customer_idx = i# 更新最佳顾客索引

        if best_customer_idx != -1:# 如果找到了最佳顾客
            vehicle_route = best_vehicle_route# 将最佳车辆路径设置为当前车辆路径
            bank.pop(best_customer_idx) # 从银行中移除最佳顾客
    return vehicle_route, bank, routes_pool# 返回车辆路径、更新后的银行和路径池

def generate_initial_solution(h, num_pair, pre_wt):
    solutions = []# 初始化解列表
    routes_pool = []  # 假设你有一个初始路径池
    bank = [i for i in range(1, num_pair + 1)]# 初始化银行，包含所有顾客编号
    pro_tmp = 0# 初始化临时“收益”值

    for _ in range(h): # 针对每辆车辆执行h次
        # 调用generate_solution_for_single_vehicle函数生成每辆车辆的路径
        sol_for_vehicle, bank, routes_pool = generate_solution_for_single_vehicle(bank, pro_tmp, routes_pool, pre_wt)
        solutions.append(sol_for_vehicle)# 将生成的路径添加到解列表

    return solutions# 返回所有车辆的初始解

def calculate_insertion_costs(customer, route):
    # 检查路径中每对顾客之间的插入情况
    costs = []
    if(len(route) == 0) :
        costs.append(0)
        return costs
    for i in range(len(route) + 1):
        if i == 0:
            costs.append(distance(customer, route[i]))
        elif i == len(route):
            costs.append(distance(route[i - 1], customer))
        else:
            costs.append(
                distance(route[i - 1], customer) + distance(customer, route[i]) - distance(route[i - 1], route[i]))
    return costs
def distance(a,b):
    return random.randint(0,100)
# Example usage:
h = 3
num_pair = 10  # for example
pre_wt = []  # your pre_wt value
initial_solutions = generate_initial_solution(h, num_pair, pre_wt)# 生成初始解
print(initial_solutions) # 打印初始解列表




