import math
import random
import copy
import global_parameter as gp
instance = {}
Dis_List = []
NonImp = 0
T0 = 187
q = 0.88
Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间

Remove_Pool = [1,2] # 删除操作池
Insert_Pool = [1] # 插入操作池

# 初始化任意两点距离
# 按照相同点到不同点的距离排序
def Init_Dis():
    dis_list = []
    N = instance['N']
    for i in range(0, N + 1):
        line = []
        for j in range(0, N + 1):
            pp = []
            pp.append(i)
            pp.append(j)
            pp.append(Get_Distance(i,j))
            line.append(pp)
        dis_list.append(line)
    # dis_list = sorted(dis_list, key=lambda x: x[2])
    # dis_list = sorted(dis_list, key=lambda x: x[0])
    return dis_list

def Init(Instance):
    global instance,Dis_List,NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    instance = Instance
    Dis_List = Init_Dis()

# 返回用户点 a 和 b 之间的距离
def Get_Distance(a,b):
    try:
        p1 = instance['x'][a] - instance['x'][b]
        p2 = instance['y'][a] - instance['y'][b]
        return round(math.sqrt(p1 * p1 + p2 * p2)) # 四舍五入为整数
    except Exception as e:
        print(f"From Get_Distance get an error: {e}")
        return None

# 查询一条路径的花费,不算购车花费
def Get_Route_Cost(route):
    Len = len(route)
    dis = 0
    for i in range(0,Len - 1):
        dis += Get_Distance(route[i],route[i + 1])
    cost = dis * P_Dis_Charge * P_Charge_Cost
    return cost

# 计算一个解的花费，包括距离的花费和购车花费
def Get_Sol_Cost(sol):
    cost = 0
    for route in sol:
        cost += Get_Route_Cost(route)
        cost += Delivery_Cost
    return cost

#检查路线route是否符合时间窗
def check_time(route): # 检查时间框可行性
    Len = len(route)
    time_window = [[0, 840] for _ in range(Len)]
    last_arr = 0 # 最晚到达
    last_leave = 840 # 最晚离开
    for i in range(0,Len,-1):
        R = instance['tr'][i]
        s = instance['s'][i]
        dis_time = Get_Distance(i,i + 1) * P_Delivery_Speed
        last_leave = last_arr - dis_time
        last_arr = min(R,last_leave) - s
        time_window[i][1] = last_leave
        if(last_leave + s > R):
            return []

    early_arr = 0 # 最早到达
    early_leave = 0 # 最早离开
    for i in range(0,Len):
        L = instance['tl'][i]
        s = instance['s'][i]
        dis_time = Get_Distance(i,i + 1) * P_Delivery_Speed
        early_arr = early_leave + dis_time
        early_leave = max(early_arr,L) + s
        time_window[i + 1][0] = early_arr
    return time_window

#返回将用户 customer 插入到路线 route 中的最佳位置和相应路线的总 cost
def Ins_Customer_To_Route(customer,route):
    sum_q = sum(instance['q'][i] for i in route) # 该路线总载货量
    # print("sum :",sum_q)
    # print("ins_customer_to_route",customer,route)
    # print(customer)
    if(sum_q + instance['q'][customer] > Delivery_Capacity):
        return -1,float('inf')
    # print("ins_customer_to_route")
    best_dis = float('inf')
    best_idx = -1
    #未插入的route距离
    # print("len", len(route))
    # print(route[len(route) - 1])
    cur_dis = 0
    Len = len(route)
    for i in range(0,Len):
        cur_dis += Dis_List[route[i]][route[i + 1]][2]
    #尝试所有位置
    for idx in range(1,Len):
        route_copy = copy.deepcopy(route)
        route_copy.insert(idx,customer)
        #如果该位置插入不符合时间窗则跳过
        if(len(check_time(route_copy)) == 0):
            continue
        cur_dis = Get_Distance(route[idx],customer) + Get_Distance(customer,route[idx + 1])\
                  - Get_Distance(route[idx],route[idx + 1])
        if(cur_dis < best_dis):
            best_dis = cur_dis
            best_idx = idx
        best_cost = float('inf')
        if(best_dis != float('inf')):
            best_cost = best_dis * P_Dis_Charge * P_Charge_Cost
    return best_idx,best_cost

#将一些点，从当前解中删除
def Remove(bank, cur_sol):
    new_sol = []# 创建一个空列表来存储新的解决方案
    for route in cur_sol:# 遍历当前解决方案中的每一条路径
        new_route = [node for node in route if node not in bank]# 创建一个新路径，其中包含不在银行中的节点
        new_sol.append(new_route) # 将新路径添加到新解决方案中
    return new_sol# 返回经过过滤后的新解决方案

# 获取初始多车路线
def Get_Init_Sol():
    route_pool = []  # 存储多车路线的池子
    bank = [i for i in range(1, instance['N'] + 1)]  # 初始化银行，包含所有顾客编号
    for i in bank:  # 遍历银行中的每个顾客
        init_cost = Delivery_Cost + 2 * Get_Distance(0,i) * P_Dis_Charge * P_Charge_Cost# 初始化成本为新开一条路线的费用
        best_cost = init_cost  # 当前最小的“遗憾值”
        best_route = -1  # 插入的最佳路线
        best_idx = -1  # 插入的最佳路线的最佳位置
        for j in range(0,len(route_pool)):  # 遍历当前已有的多车路线
            # print("sd",route_pool[j])
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


def Distroy_and_Repair(cur_sol,Removal_id,Insert_id):
    try:
        new_sol = cur_sol
        bank = []
        cost = float('inf')
        #Removal
        if(Removal_id == 1):
            bank,new_sol = Random_Remove(cur_sol)
        elif(Removal_id == 2):
            bank,new_sol = Distance_Related_Remove(cur_sol)
        elif(Removal_id == 3):
            bank,new_sol = String_Remove(cur_sol)
        # print(Removal_id)
        # print(new_sol)

        new_sol = [sol for sol in new_sol if(len(sol) != 0)] #有些路线被删除为空，需要删除这些路线
        #Insert
        if(Insert_id == 1):
            new_sol,cost = Random_Ins(instance,new_sol,bank)
        # print(new_sol)
        return new_sol,cost
    except Exception as e:
        print(f"From Distroy_and_Repair get an error: {e}")


def Random_Remove(cur_sol): #Rem-1
    bank = [] #删除的节点
    new_sol = [] #新路线
    N = instance['N']
    bank = random.sample(range(1,N + 1),min(NonImp,N))
    # 如果不在被删除的列表里，则添加到新列表里
    new_sol = Remove(bank,cur_sol)
    return bank,new_sol


#计算所有其他客户与所选择客户之间的距离，并删除距离较近的客户。
def Distance_Related_Remove(cur_sol): #Rem-2
    cost_node = []
    bank = []
    Num = instance['N']
    Min = min(Num,NonImp)
    node = random.randint(1,Num)
    List = copy.deepcopy(Dis_List[node])
    List.sort(key=lambda x: x[2])
    # print("bankk",node,Num,start,len(Dis_List))
    for i in range(0,Min):
        if(List[i][1] == 0 or List[i][1] == Num + 1):
            continue
        bank.append(List[i][1])
    new_sol = Remove(bank,cur_sol)
    # print("bank",bank)
    return bank,new_sol

#在每个路线中选择一个随机的起始点和一个随机的客户序列长度
def String_Remove(cur_sol): #Rem-3
    bank = []
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
    try:

        bank_copy = copy.deepcopy(bank)
        # print("bank",bank)
        for _ in range(len(bank_copy)):
            node = random.choice(bank)
            best_route = -1
            best_idx = -1
            best_cost = Delivery_Cost + 2 * Get_Distance(0,node) * P_Dis_Charge * P_Charge_Cost
            for j in range(len(cur_sol)):
                # print(node,bank)
                cur_idx ,cur_cost = Ins_Customer_To_Route(node,cur_sol[j])
                if(cur_cost < best_cost):
                    best_idx = cur_idx
                    best_cost = best_cost
                    best_route = j
            if best_route != -1:
                cur_sol[best_route].insert(best_idx, node)
                bank.remove(node)
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



def LNS(Instance):
    Init(Instance) #初始化任意两点距离
    print(Dis_List)
    init_sol , init_cost= Get_Init_Sol()
    best_sol , best_cost= init_sol,init_cost
    cur_sol , cur_cost = init_sol, init_cost
    T = T0
    MaxI = 100 # 最大迭代次数
    Terminal = 0 # 迭代次数
    NonImp = 0
    while Terminal < MaxI:
        Removal_id = random.choice(Remove_Pool) # 挑选删除操作
        Reinsert_id = random.choice(Insert_Pool) # 挑选插入操作

        new_sol , new_cost= Distroy_and_Repair(cur_sol,Removal_id,Reinsert_id) #重构解
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
            print(NonImp,best_cost, best_sol)
            NonImp = 0 #连续没有提升的次数归零

        else:
            NonImp += 1
        Terminal += 1
    return best_sol,best_cost
