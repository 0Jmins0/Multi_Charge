import math
import random
import copy
import numpy as np
import global_parameter as gp

instance = {}
Dis_List = []
NonImp = 1
Max_nonimp_LS = 3
Max_nonimp_Opt = 3

T0 = 187
q = 0.88
Remove_Pool = [1,2,3] # 删除操作池
Insert_Pool = [1] # 插入操作池
LocalOperator_Pool = [1,2,3,4,5,6] # 邻域操作池

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间
Lambda_Value = 3

###############################       初始化函数     ##########################################

# 初始化任意两点距离
# 按照相同点到不同点的距离排序
def Init_Dis():
    dis_list = []
    N = instance['N']
    for i in range(0, N + 2):
        line = []
        for j in range(0, N + 2):
            pp = []
            pp.append(i)
            pp.append(j)
            pp.append(Get_Distance(i,j))
            line.append(pp)
        dis_list.append(line)
    return dis_list

def Init(Instance):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    instance = Instance
    Dis_List = Init_Dis()

# 获取初始多车路线
def Get_Init_Sol():
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    route_pool = []  # 存储多车路线的池子
    bank = [i for i in range(1, instance['N'] + 1)]  # 初始化银行，包含所有顾客编号
    for i in bank:  # 遍历银行中的每个顾客
        init_cost = Delivery_Cost + round(2 * Get_Distance(0,i) * P_Dis_Charge * P_Charge_Cost)# 初始化成本为新开一条路线的费用
        best_cost = init_cost  # 当前最小的“遗憾值”
        best_route = -1  # 插入的最佳路线
        best_idx = -1  # 插入的最佳路线的最佳位置
        for j in range(0,len(route_pool)):  # 遍历当前已有的多车路线
            cur_idx, cur_cost = Ins_Customer_To_Route(i, route_pool[j])  # 尝试插入顾客到路线中
            if cur_cost < best_cost:  # 如果插入后的成本更低
                best_route = j  # 更新最佳路线
                best_idx = cur_idx  # 更新最佳位置
                best_cost = cur_cost  # 更新最佳成本
        if best_cost == init_cost:  # 如果没有找到更好的插入位置
            route = []  # 创建一个新的路线
            route.append(0)
            route.append(i)  # 将当前顾客添加到新路线中
            route.append(instance['N'] + 1)
            route_pool.append(route)  # 将新路线添加到多车路线池中
        else:
            route_pool[best_route].insert(best_idx, i)  # 在最佳路线的最佳位置插入顾客

    init_cost = Get_Sol_Cost(route_pool)# 更新总成本
    return route_pool, init_cost  # 返回多车路线池和初始化总成本

###############################       功能类函数     ##########################################

# 返回用户点 a 和 b 之间的距离
def Get_Distance(a,b):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    try:
        p1 = instance['x'][a] - instance['x'][b]
        p2 = instance['y'][a] - instance['y'][b]
        return round(math.sqrt(p1 * p1 + p2 * p2)) # 四舍五入为整数
    except Exception as e:
        print(f"From Get_Distance get an error: {e}")
        return None

# 查询一条路径的花费,不算购车花费
def Get_Route_Cost(route):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    Len = len(route)
    dis = 0
    for i in range(0,Len - 1):
        dis +=Dis_List[route[i]][route[i + 1]][2]
    cost = round(dis * P_Dis_Charge * P_Charge_Cost)
    return cost

# 计算一个解的花费，包括距离的花费和购车花费
def Get_Sol_Cost(sol):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    cost = 0
    for route in sol:
        cost += Get_Route_Cost(route)
        cost += Delivery_Cost
    return cost

#检查路线route是否符合时间窗 返回一个点最早可以开始服务旳时间和最晚必须开始服务的时间
def check_time(route): # 检查时间框可行性
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    Len = len(route)
    time_window = [[0, 840] for _ in range(Len)]
    last_arr = 840 # 最晚到达
    last_leave = 840 # 最晚离开
    for i in range(Len - 1,0,-1):
        L = instance['tl'][route[i - 1]]
        R = instance['tr'][route[i - 1]]
        s = instance['s'][route[i - 1]]
        dis_time = round(Dis_List[route[i]][route[i - 1]][2] * P_Delivery_Speed)
        last_leave = last_arr - dis_time # 当前点最晚离开时间
        last_arr = min(R,last_leave - s) # 当前点最晚到达时间
        time_window[i - 1][1] = last_arr
        if(last_arr < L):
            return []

    early_arr = 0 # 最早到达
    early_leave = 0 # 最早离开
    for i in range(0,Len - 1):
        L = instance['tl'][route[i + 1]]
        s = instance['s'][route[i + 1]]
        dis_time = round(Dis_List[route[i]][route[i + 1]][2] * P_Delivery_Speed)
        early_arr = early_leave + dis_time
        early_leave = max(early_arr,L) + s
        time_window[i + 1][0] = early_arr
    return time_window


#检查路线route是否满足两点间满电量可达
def check_dis(route):
    N = len(route)
    for i in range(0,N - 1):
        dis = Dis_List[route[i]][route[i + 1]][2]
        charge = dis * P_Dis_Charge
        if(charge > Battery_Capacity) :
            return 0

    return 1


#返回将用户 customer 插入到路线 route 中的最佳位置和相应路线的总 cost
def Ins_Customer_To_Route(customer,route):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    sum_q = sum(instance['q'][i] for i in route) # 该路线总载货量
    if(sum_q + instance['q'][customer] > Delivery_Capacity):
        return -1,float('inf')

    best_dis = float('inf')
    best_idx = -1
    best_cost = float('inf')

    #未插入的route距离
    cur_dis = 0
    Len = len(route)
    for i in range(0,Len - 1):
        cur_dis += Dis_List[route[i]][route[i + 1]][2]

    #尝试所有位置
    for idx in range(1,Len):
        route_copy = copy.deepcopy(route)
        route_copy.insert(idx,customer)
        #如果该位置插入不符合时间窗则跳过
        if(len(check_time(route_copy)) == 0 or check_dis(route_copy) == 0):
            continue
        cur_dis = Get_Distance(route[idx],customer) + Get_Distance(customer,route[idx - 1])\
                  - Get_Distance(route[idx],route[idx - 1])
        if(cur_dis < best_dis):
            best_dis = cur_dis
            best_idx = idx

    if(best_dis != float('inf')):
        best_cost = round(best_dis * P_Dis_Charge * P_Charge_Cost)
    return best_idx,best_cost

#将一些点，从当前解中删除
def Remove(bank, cur_sol):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    new_sol = []# 创建一个空列表来存储新的解决方案
    for route in cur_sol:# 遍历当前解决方案中的每一条路径
        new_route = [node for node in route if node not in bank]# 创建一个新路径，其中包含不在银行中的节点
        new_sol.append(new_route) # 将新路径添加到新解决方案中
    return new_sol# 返回经过过滤后的新解决方案

#将列表中两坐标之间的元素翻转
def reverse_elements_between(lst, index1, index2):
    # 确保 index1 和 index2 在列表范围内
    if 0 <= index1 < len(lst) and 0 <= index2 < len(lst):
        # 选择要翻转的部分
        start_index = min(index1, index2)
        end_index = max(index1, index2)
        sublist = lst[start_index:end_index+1]

        # 翻转部分
        lst[start_index:end_index+1] = reversed(sublist)

    return lst



def Distroy_and_Repair(cur_sol,Removal_id,Insert_id):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    try:
        # print("D_R")
        new_sol = cur_sol
        bank = []
        cost = float('inf')

        # Removal
        if(Removal_id == 1):
            # print("D_R_B1")
            bank,new_sol = Random_Remove(cur_sol)
            # print("D_R_1")
        elif(Removal_id == 2):
            # print("D_R_B2")
            bank,new_sol = Distance_Related_Remove(cur_sol)
            # print("D_R_2")
        elif(Removal_id == 3):
            # print("D_R_B3")
            bank,new_sol = String_Remove(cur_sol)
            # print("D_R_3")

        new_sol = [sol for sol in new_sol if(len(sol) != 2)] #有些路线被删除为空，只剩下起点和终点，需要删除这些路线

        # print("D_R_Remove")
        # Insert
        if(Insert_id == 1):
            new_sol,cost = Random_Ins(new_sol,bank)

        # print("D_R_INsert")
        return new_sol,cost
    except Exception as e:
        print(f"From Distroy_and_Repair get an error: {e}")

def Local_Operate(new_sol,new_cost,Operator_id):
    if(Operator_id == 1):
        # print("LS_1")
        return opt2_exchange(new_sol)
    elif(Operator_id == 2):
        # print("LS_2")
        return or_opt(new_sol)
    elif(Operator_id == 3):
        return opt2_exchange_mul(new_sol)
    elif(Operator_id == 4):
        return relocate_operator(new_sol)
    elif(Operator_id == 5):
        return exchange_operator(new_sol)
    elif(Operator_id == 6):
        return cross_exchange_operator(new_sol)

def LS(new_sol,new_cost):
    Operator_id = random.choice(LocalOperator_Pool)
    new_sol = Local_Operate(new_sol,new_cost,Operator_id)
    new_sol = [sol for sol in new_sol if (len(sol) != 2)]  # 有些路线被删除为空，只剩下起点和终点，需要删除这些路线
    new_cost = Get_Sol_Cost(new_sol)
    return new_sol,new_cost

###############################       删除操作符     ##########################################

def Random_Remove(cur_sol): #Rem-1
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    bank = [] # 删除的节点
    new_sol = [] # 新路线
    N = instance['N']
    bank = random.sample(range(1,N + 1),min(NonImp,N))
    # 如果不在被删除的列表里，则添加到新列表里
    new_sol = Remove(bank,cur_sol)
    return bank,new_sol


#计算所有其他客户与所选择客户之间的距离，并删除距离较近的客户。
def Distance_Related_Remove(cur_sol): #Rem-2
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    cost_node = []
    bank = []
    Num = instance['N']
    Min = min(Num,NonImp)
    node = random.randint(1,Num)
    List = copy.deepcopy(Dis_List[node])
    List.sort(key=lambda x: x[2])
    for i in range(0,Min):
        if(List[i][1] == 0 or List[i][1] == Num + 1):
            continue
        bank.append(List[i][1])
    new_sol = Remove(bank,cur_sol)
    return bank,new_sol

#在每个路线中选择一个随机的起始点和一个随机的客户序列长度
def String_Remove(cur_sol): #Rem-3
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    bank = []
    # print("Strint_Remove",len(cur_sol))

    for sol in cur_sol:
        Len = len(sol) - 2
        start = random.randint(1,Len)
        Del_len = min(NonImp,Len - start + 1)
        random_len = random.randint(0,Del_len)
        for i in range(start,start + random_len):
            bank.append(sol[i])

    new_sol = Remove(bank,cur_sol)
    return bank,new_sol

#于每个客户，计算如果将该客户从其当前路线中移除，会导致总成本发生多大的变化。
#通常包括了行驶距离、时间窗口违规、容量违规等因素。对于每个客户，记录下其对总成本的影响。
def Worst_removal(instance,NonImp,cur_sol):
    return

#对于每个客户，计算其最早出发时间和最晚服务时间窗口之间的差异。
#从上一步骤计算出的差异中，选择那些差异显著的客户，即那些最早出发时间和最晚服务时间窗口之间的差异较大的客户。
def Late_Arrival_Removal(instance,NonImp,cur_sol):
    return

#将送货选项（客户）根据其地理位置划分为多个矩形区域。区域数量预先设置
#从预定义的矩形区域中随机选择一个区域。
#随机选择一个区域，将当前解决方案中属于该区域的所有客户从其当前路线中移除。
def Zone_Removal(instance,NonImp,cur_sol):
    return

#随机选择一个客户，对于每个客户，计算其出发时间与所选择客户的出发时间之间的接近程度。
#删除那些出发时间与所选择客户接近的客户。
def Time_Related_Removal(instance,NonImp,cur_sol):
    return

#随机选择一条路线，然后使用Kruskal算法将这条路线上的客户分成两个簇（clusters），然后随机选择一个簇中的所有客户进行移除
#从两个簇中随机选择一个簇，然后将该簇中的所有客户都移除。
def Cluster_Removal():
    return


###############################       插入操作符     ##########################################

def Random_Ins(cur_sol,bank): #Ins-1
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    try:
        bank_copy = copy.deepcopy(bank)
        for _ in range(len(bank_copy)):
            node = random.choice(bank)
            bank.remove(node)
            best_route = -1
            best_idx = -1
            best_cost = Delivery_Cost + round(2 * Get_Distance(0,node) * P_Dis_Charge * P_Charge_Cost)
            for j in range(len(cur_sol)):
                cur_idx ,cur_cost = Ins_Customer_To_Route(node,cur_sol[j])
                if(cur_cost < best_cost):
                    best_idx = cur_idx
                    best_cost = best_cost
                    best_route = j
            if best_route != -1:
                cur_sol[best_route].insert(best_idx, node)
            else:
                route = []
                route.append(0)
                route.append(node)
                route.append(instance['N'] + 1)
                cur_sol.append(route)
        finall_cost = Get_Sol_Cost(cur_sol)
        return cur_sol,finall_cost
    except Exception as e:
        print(f"From Random_Ins get an error: {e}")


###############################       邻域操作符     ##########################################
###记得加 checktime 和 checkdis

#单个路径内

# 选取一个路线中的任意两点，翻转包括其在内的中间的点
def opt2_exchange(new_sol):
    Count = 1
    # print("OPT_before",new_sol,'\n',Get_Sol_Cost(new_sol))
    while(Count < Max_nonimp_Opt):
        # 随机选取一条路径处理
        route_idx = random.choice(range(len(new_sol)))
        route = copy.deepcopy(new_sol[route_idx])
        route_cost = Get_Route_Cost(route)

        # 路径中少于两个点
        if(len(route) < 4):
            Count = Count + 1
            continue

        #随机选取路径中的两点，翻转其中间的元素
        index1,index2 = random.sample(range(1,len(route) - 1),2) # 随机选取两个坐标
        tmp_route = reverse_elements_between(route,index1,index2)
        tmp_cost = Get_Route_Cost(tmp_route)

        if(len(check_time(tmp_route)) == 0 or check_dis(tmp_route) == 0):
            Count = Count + 1
            continue

        #检查是否代价更小
        if(tmp_cost < route_cost):
            new_sol[route_idx] = tmp_route
            # print(tmp_cost,route_cost,Get_Sol_Cost(new_sol))
            Count = 1
        else:
            Count = Count + 1
    # print("OPT_after", new_sol,'\n',Get_Sol_Cost(new_sol))
    return new_sol

# 选取一条路线中连续的两点，将其放在其他位置
def or_opt(new_sol):
    Count = 1
    # print("OPT_before",new_sol,'\n',Get_Sol_Cost(new_sol))
    while(Count < Max_nonimp_Opt):
        # 随机选取一条路径处理
        route_idx = random.choice(range(len(new_sol)))
        route = copy.deepcopy(new_sol[route_idx])
        route_cost = Get_Route_Cost(route)
        # print('1',len(route))
        # 路径中少于三个点
        if(len(route) < 5):
            Count = Count + 1
            continue
        # print('2',len(route))
        #随机选取路径中连续的两点
        index1= random.choice(range(1,len(route) - 2)) # 随机选取一个坐标
        index2 = index1 + 1

        ele1 = route[index1]
        ele2 = route[index2]

        route.remove(ele1)
        route.remove(ele2)

        index3 = index1
        while(index3 == index1):
            index3 = random.choice(range(1, len(route)))  # 随机选取一个坐标
            # print("index",index3,index1)
        index4 = index3 + 1

        route.insert(index3,ele1)
        route.insert(index4,ele2)


        tmp_cost = Get_Route_Cost(route)

        if(len(check_time(route)) == 0 or check_dis(route) == 0):
            Count = Count + 1
            continue

        #检查是否代价更小
        if(tmp_cost < route_cost):
            new_sol[route_idx] = route
            # print(tmp_cost,route_cost,Get_Sol_Cost(new_sol))
            Count = 1
        else:
            Count = Count + 1
    # print("OPT_after", new_sol,'\n',Get_Sol_Cost(new_sol))
    return new_sol

# 路径间

# 选择路径1的节点A和路径2的节点B，交换它们，并将A后面的节点接到B的位置，将B后面的节点接到A的位置。
def opt2_exchange_mul(new_sol):
    # Opt-2交换多次的局部搜索函数
    if len(new_sol) < 2:
        return new_sol
    Count = 1
    while Count < Max_nonimp_Opt:
        # 随机选择两个路径
        index1, index2 = random.sample(range(0, len(new_sol)), 2)
        route1 = copy.deepcopy(new_sol[index1])
        route2 = copy.deepcopy(new_sol[index2])

        # 计算当前两路径的成本
        cost = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        # 如果某个路径的长度小于4，则无法进行切割交换
        if len(route1) < 4 or len(route2) < 4:
            Count = Count + 1
            continue

        # 随机选择切割点
        cut1 = random.choice(range(1, len(route1) - 2))
        cut2 = random.choice(range(1, len(route2) - 2))

        # 切割并交换部分路径
        route1_L = route1[:cut1]
        route1_R = route1[cut1:]
        route2_L = route2[:cut2]
        route2_R = route2[cut2:]

        route1_new = route1_L + route2_R
        route2_new = route2_L + route1_R

        # 检查交换后路径的约束条件
        if (len(check_time(route1_new)) == 0 or check_dis(route1_new) == 0 or
                len(check_time(route2_new)) == 0 or check_dis(route2_new) == 0):
            Count = Count + 1
            continue

        # 计算交换后的成本
        cost_new = Get_Route_Cost(route1_new) + Get_Route_Cost(route2_new)

        # 如果成本降低，则接受新解，重新开始计数
        if cost > cost_new:
            new_sol[index1] = route1_new
            new_sol[index2] = route2_new
            Count = 1
        else:
            Count = Count + 1

    return new_sol

#选择路径1的节点A，将A从路径1中删除，并将A插入到路径2的合适位置。
def relocate_operator(new_sol):
    # 重新定位操作符的局部搜索函数
    if len(new_sol) < 2:
        return new_sol

    count = 1
    while count < Max_nonimp_Opt:
        # 随机选择两个路径
        index1, index2 = random.sample(range(0, len(new_sol)), 2)
        route1 = copy.deepcopy(new_sol[index1])
        route2 = copy.deepcopy(new_sol[index2])

        # 计算当前两路径的成本
        cost = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        # 如果某个路径的长度小于3，则无法进行重新定位
        if len(route1) < 4 or len(route2) < 3:
            count += 1
            continue

        # 随机选择一个节点并将其从一个路径中移除，插入到另一路径中的比较好的位置
        node_index = random.choice(range(1, len(route1) - 1))
        relocated_node = route1.pop(node_index)
        best_idx ,best_cost= Ins_Customer_To_Route(relocated_node,route2)
        route2.insert(best_idx, relocated_node)

        # 检查路径约束条件
        if not (check_time(route1) and check_dis(route1) and
                check_time(route2) and check_dis(route2)):
            count += 1
            continue

        # 计算重新定位后的成本
        cost_new = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        # 如果成本降低，则接受新解，重新开始计数
        if cost > cost_new:
            new_sol[index1] = route1
            new_sol[index2] = route2
            count = 1
        else:
            count += 1

    return new_sol

#选择路径1的节点A和路径2的节点B，交换它们，将A放回路径1，将B放回路径2。
def exchange_operator(new_sol):
    if len(new_sol) < 2:
        return new_sol

    count = 1
    while count < Max_nonimp_Opt:
        index1, index2 = random.sample(range(0, len(new_sol)), 2)
        route1 = copy.deepcopy(new_sol[index1])
        route2 = copy.deepcopy(new_sol[index2])

        cost = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        if len(route1) < 3 or len(route2) < 3:
            count += 1
            continue

        node_index1 = random.choice(range(1, len(route1) - 1))
        node_index2 = random.choice(range(1, len(route2) - 1))

        route1[node_index1], route2[node_index2] = route2[node_index2], route1[node_index1]

        if not (check_time(route1) and check_dis(route1) and
                check_time(route2) and check_dis(route2)):
            count += 1
            continue

        cost_new = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        if cost > cost_new:
            new_sol[index1] = route1
            new_sol[index2] = route2
            count = 1
        else:
            count += 1

    return new_sol

def cross_exchange_operator(new_sol):
    if len(new_sol) < 2:
        return new_sol

    count = 1
    while count < Max_nonimp_Opt:
        path_index1, path_index2 = random.sample(range(0, len(new_sol)), 2)
        route1 = copy.deepcopy(new_sol[path_index1])
        route2 = copy.deepcopy(new_sol[path_index2])

        cost = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        if len(route1) < 5 or len(route2) < 5:
            count += 1
            continue

        # 随机选择两个连续的节点，构成一个路径的子序列
        node_index1 = random.choice(range(1, len(route1) - 2))
        node_index2 = node_index1 + 1

        # 获取第一个子序列
        segment1 = route1[node_index1:node_index2 + 1]

        # 随机选择该路径上的两个连续的节点，构成另一个路径的子序列
        node_index3 = random.choice(range(1, len(route2) - 2))
        node_index4 = node_index3 + 1

        # 获取第二个子序列
        segment2 = route2[node_index3:node_index4 + 1]

        # 将第一个子序列放到第二个子序列的位置
        route2[node_index3:node_index4 + 1] = segment1

        # 将第二个子序列放到第一个子序列的位置
        route1[node_index1:node_index2 + 1] = segment2

        if not (check_time(route1) and check_dis(route1) and
                check_time(route2) and check_dis(route2)):
            count += 1
            continue

        cost_new = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        if cost > cost_new:
            new_sol[path_index1] = route1
            new_sol[path_index2] = route2
            count = 1
        else:
            count += 1

    return new_sol


def lambda_interchange_operator(new_sol):
    if len(new_sol) < 2 or Lambda_Value < 1:
        return new_sol

    count = 1
    while count < Max_nonimp_Opt:
        path_indices = random.sample(range(0, len(new_sol)), 2)
        route1 = copy.deepcopy(new_sol[path_indices[0]])
        route2 = copy.deepcopy(new_sol[path_indices[1]])

        cost = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        if len(route1) < Lambda_Value + 3 or len(route2) < Lambda_Value + 3:
            count += 1
            continue

        # 随机选择 λ 个节点，进行交换
        nodes_indices1 = random.sample(range(1, len(route1) - 1), Lambda_Value)
        nodes_indices2 = random.sample(range(1, len(route2) - 1), Lambda_Value)

        # 交换选定的节点
        for i in range(Lambda_Value):
            route1[nodes_indices1[i]], route2[nodes_indices2[i]] = route2[nodes_indices2[i]], route1[nodes_indices1[i]]

        if not (check_time(route1) and check_dis(route1) and
                check_time(route2) and check_dis(route2)):
            count += 1
            continue

        cost_new = Get_Route_Cost(route1) + Get_Route_Cost(route2)

        if cost > cost_new:
            new_sol[path_indices[0]] = route1
            new_sol[path_indices[1]] = route2
            count = 1
        else:
            count += 1

    return new_sol


def LNS(Instance):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    Init(Instance) #初始化任意两点距离
    init_sol , init_cost= Get_Init_Sol()
    best_sol , best_cost= init_sol,init_cost
    cur_sol , cur_cost = init_sol, init_cost
    T = T0
    MaxI = 100 # 最大迭代次数
    Terminal = 0 # 迭代次数
    NonImp = 1
    print("初始化结束")
    while Terminal < MaxI:
        Removal_id = random.choice(Remove_Pool) # 挑选删除操作
        Reinsert_id = random.choice(Insert_Pool) # 挑选插入操作
        new_sol , new_cost= Distroy_and_Repair(cur_sol,Removal_id,Reinsert_id) #重构解

        # print("new_before_LS",new_cost)
        #LS
        if(new_cost < best_cost):
            nonimp = 1
            while nonimp < Max_nonimp_LS:
                tmp_sol ,tmp_cost = LS(new_sol,new_cost)
                if(tmp_cost < new_cost):
                    print(tmp_cost, new_cost)
                    new_cost = tmp_cost
                    new_sol = tmp_sol
                    nonimp = 1
                else:
                    nonimp = nonimp + 1
                # print("LS",nonimp)

        # print("new_after_LS", new_cost)
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

        if cur_cost < best_cost:
            best_sol = cur_sol
            best_cost = cur_cost
            NonImp = 1 #连续没有提升的次数归零
        else:
            NonImp += 1
        Terminal += 1


    time_window = []
    print("best_cost",best_cost)
    for route in best_sol:
        time_window.append(check_time(route))
    return best_sol,best_cost,Dis_List,time_window
