import math
import random
import copy
from feasiblity import check
Max_cap = 500 # 车辆最大载货量
Vehicle_Cost = 1000 # 每辆车的价格
Speed = 1
Service_Time = 100 # 服务时间
p_dis_cost = 1 # 距离和花费的系数，距离乘该系数为花费
T0 = 187
q = 0.88
#返回用户点 a 和 b 之间的距离
def distance(a,b,instance):
    p1 = instance['x'][a] - instance['x'][b]
    p2 = instance['y'][a] - instance['y'][b]
    return math.sqrt(p1 * p1 + p2 * p2)

#检查路线route是否符合时间窗
def check_time(route,instance):
    # print("check time",route)
    last_arrval = instance['tr'][route[-1]] - Service_Time
    for i in range(len(route) - 1,0,-1):
        time_i_j = distance(route[i],route[i - 1],instance) / Speed
        last_arrval -= time_i_j
        # print(last_arrval + Service_Time,instance['tr'][i - 1])
        if(last_arrval + Service_Time > instance['tr'][i - 1] or last_arrval < 0):
            # print('fail')
            return 0
        last_arrval = max(last_arrval,instance['tl'][i - 1])
    # print(route , "success")
    return 1

#返回将用户 customer 插入到路线 route 中的最佳位置和相应 cost
def ins_customer_to_route(customer,instance,route):
    sum_q = sum(instance['q'][i] for i in route) # 该路线总载货量
    # print("sum :",sum_q)
    # print("ins_customer_to_route",customer,route)
    if(sum_q + instance['q'][customer] > Max_cap):
        return -1,float('inf')
    # print("ins_customer_to_route")
    best_dis = float('inf')
    best_idx = -1
    #未插入的route距离
    dis = distance(0,route[0],instance) + distance(0,route[len(route) - 1],instance)# 该路线总距离
    for i in range(1,len(route)):
        dis += distance(route[i - 1],route[i],instance)

    #尝试所有位置
    for idx in range(0,len(route) + 1):
        cur_dis = dis
        route_copy = copy.deepcopy(route)
        route_copy.insert(idx,customer)
        #如果该位置插入不符合时间窗则跳过
        if(check_time(route_copy,instance) == 0):
            continue
        #插入头
        if(idx == 0):
            cur_dis -= distance(0,route[idx],instance)
            cur_dis += distance(0,customer,instance)
            cur_dis += distance(customer,route[0],instance)
        #插入尾
        elif(idx == len(route)):
            cur_dis -= distance(0,route[idx - 1],instance)
            cur_dis += distance(0,customer,instance)
            cur_dis += distance(customer,route[idx - 1],instance)
        #插中间
        else:
            # print(len(route),idx)
            cur_dis -= distance(route[idx - 1],route[idx],instance)
            cur_dis += distance(route[idx - 1],customer,instance)
            cur_dis += distance(route[idx],customer,instance)

        if(cur_dis < best_dis):
            best_dis = cur_dis
            best_idx = idx
    return best_idx,best_dis

# 获取初始多车路线
def get_init_sol(instance):
    route_pool = []  # 存储多车路线的池子
    init_cost = 0  # 初始化总成本为0
    bank = [i for i in range(1, instance['num'] + 1)]  # 初始化银行，包含所有顾客编号
    for i in bank:  # 遍历银行中的每个顾客
        init_cost = Vehicle_Cost + 2 * distance(i, 0, instance)  # 初始化成本为车辆成本加上顾客到仓库的往返距离
        best_cost = init_cost  # 当前最小的“遗憾值”
        best_route = -1  # 插入的最佳路线
        best_idx = -1  # 插入的最佳路线的最佳位置
        for j in range(len(route_pool)):  # 遍历当前已有的多车路线
            cur_idx, cur_cost = ins_customer_to_route(i, instance, route_pool[j])  # 尝试插入顾客到路线中
            if cur_cost < best_cost:  # 如果插入后的成本更低
                best_route = j  # 更新最佳路线
                best_idx = cur_idx  # 更新最佳位置
                best_cost = cur_cost  # 更新最佳成本
        if best_cost == init_cost:  # 如果没有找到更好的插入位置
            route = []  # 创建一个新的路线
            route.append(i)  # 将当前顾客添加到新路线中
            route_pool.append(route)  # 将新路线添加到多车路线池中
        else:
            route_pool[best_route].insert(best_idx, i)  # 在最佳路线的最佳位置插入顾客
        init_cost += best_cost  # 更新总成本
    return route_pool, init_cost  # 返回多车路线池和初始化总成本

def Remove(bank, cur_sol):
    new_sol = []# 创建一个空列表来存储新的解决方案
    for route in cur_sol:# 遍历当前解决方案中的每一条路径
        new_route = [node for node in route if node not in bank]# 创建一个新路径，其中包含不在银行中的节点
        new_sol.append(new_route) # 将新路径添加到新解决方案中
    return new_sol# 返回经过过滤后的新解决方案

def Random_Remove(instance,NonImp,cur_sol): #Rem-1
    bank = [] #删除的节点
    new_sol = [] #新路线
    N = instance['num']
    bank = random.sample(range(1,N + 1),min(NonImp,N))
    # 如果不在被删除的列表里，则添加到新列表里
    new_sol = Remove(bank,cur_sol)
    return bank,new_sol

#选取删除后，距离减少最多的点删除
def Distance_Related_Remove(instance,NonImp,cur_sol): #Rem-2
    cost_node = []
    bank = []
    for route in cur_sol:
        for i in range (len(route)):
            cost = 0
            #该路线只有一个点
            if(i == 0 and i + 1 != len(route) - 1):
                cost = distance(0,i,instance) + distance(i ,i + 1,instance)
            #仓库出来访问的第一个点
            elif(i == 0):
                cost = distance(0,i,instance) * 2
            #回到仓库的最后一个点
            elif(i == len(route) - 1):
                cost = distance(0,i,instance) + distance(i - 1,i, instance)
            #其他点
            else:
                cost = distance(i ,i + 1,instance) + distance(i, i - 1,instance)
            tt = []
            tt.append(cost)
            tt.append(i)
            cost_node.append(tt)
    sort_list = sorted(cost_node,key = lambda x : x[0])
    for i in range(NonImp):
        bank.append(sort_list[i][1])
    new_sol = Remove(bank,cur_sol)
    return bank,new_sol

def Random_Ins(instance,cur_sol,bank): #Ins-1
    bank_copy = copy.deepcopy(bank)
    finall_cost = float('inf')
    for _ in range(len(bank_copy)):
        node = random.choice(bank)
        best_route = -1
        best_idx = -1
        best_cost = float('inf')
        for j in range(len(cur_sol)):
            cur_idx ,cur_cost = ins_customer_to_route(node,instance,cur_sol[j])
            if(cur_cost < best_cost):
                best_idx = cur_idx
                best_cost = best_cost
                best_route = j
        if best_route != -1:
            cur_sol[best_route].insert(best_idx, node)
        finall_cost = best_cost
    
    return cur_sol,finall_cost


def Distroy_and_Repair(cur_sol,Removal_id,Insert_id,instance,NonImp):
    new_sol = cur_sol
    bank = []
    cost = float('inf')
    if(Removal_id == 1):
        bank,new_sol = Random_Remove(instance,NonImp,cur_sol)
    elif(Removal_id == 2):
        bank,new_sol = Distance_Related_Remove(instance,NonImp,cur_sol)
    if(Insert_id == 1):
        new_sol,cost = Random_Ins(instance,new_sol,bank)
    return new_sol,cost

def LNS(instance):
    init_sol ,init_cost= get_init_sol(instance)
    best_sol , best_cost= init_sol,init_cost
    cur_sol , cur_cost = init_sol, init_cost
    T = T0
    MaxI = 100 #最大迭代次数
    Terminal = 0 #迭代次数
    NonImp = 0
    while Terminal < MaxI:
        Removal_id = random.randint(1, 2) #挑选操作
        Reinsert_id = random.randint(1, 1)
        new_sol , new_cost= Distroy_and_Repair(cur_sol,Removal_id,Reinsert_id,instance,NonImp) #重构解
        T *= q #降温

        diff = new_cost - cur_cost

        if diff < 0:# 操作后结果变优秀了
            cur_sol = new_sol
            cur_cost = new_cost
        else:
            #有概率保留
            r = random.random()
            if T >= 0.01 and math.exp((diff) / (10000 * T)) >= r:
                cur_sol = new_sol
                cur_cost = new_cost

        if new_cost > best_cost:
            NonImp = 0 #连续没有提升的次数归零
            best_sol = new_sol
            best_cost = new_cost
        else:
            NonImp += 1
        Terminal += 1
    return best_sol,best_cost
