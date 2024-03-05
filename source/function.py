import copy
import math
import global_parameter as gp

Remove_Pool = gp.Remove_Pool  # 删除操作池
Insert_Pool = gp.Insert_Pool  # 插入操作池
LocalOperator_Pool = gp.LocalOperator_Pool  # 邻域操作池

Delivery_Capacity = gp.Delivery_Capacity  # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity  # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost  # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge  # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost  # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed  # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed  # 充电车距离和时间的系数，距离乘以系数为时间
Lambda_Value = gp.Lambda_Value



# 查询一条路径的花费,不算购车花费
def Get_Route_Cost(route, instance, Dis_List):
    global Delivery_Capacity, Battery_Capacity, \
    Delivery_Cost, P_Dis_Charge, P_Charge_Cost, P_Delivery_Speed, P_Charge_Speed
    Len = len(route)
    dis = 0
    for i in range(0,Len - 1):
        # print(route[i],route[i + 1])
        # print(Dis_List)
        dis += Dis_List[route[i]][route[i + 1]][2]
    cost = round(dis * P_Dis_Charge * P_Charge_Cost)
    return cost

# 计算一个解的花费，包括距离的花费和购车花费
def Get_Sol_Cost(sol,instance,Dis_List):
    global NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
    Delivery_Cost,P_Dis_Charge,P_Charge_Cost,P_Delivery_Speed,P_Charge_Speed
    cost = 0
    for route in sol:
        cost += Get_Route_Cost(route,instance,Dis_List)
        cost += Delivery_Cost
    return cost

#检查路线route是否符合时间窗 返回一个点最早可以开始服务旳时间和最晚必须开始服务的时间
def check_time(route,instance,Dis_List): # 检查时间框可行性
    global NonImp,T0,q,Delivery_Capacity,Battery_Capacity, \
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
def check_dis(route,instance,Dis_List):
    N = len(route)
    for i in range(0,N - 1):
        dis = Dis_List[route[i]][route[i + 1]][2]
        charge = dis * P_Dis_Charge
        if(charge > Battery_Capacity) :
            return 0

    return 1


#返回将用户 customer 插入到路线 route 中的最佳位置和相应路线的总 cost
def Ins_Customer_To_Route(customer,route,instance,Dis_List):
    global NonImp,T0,q,Delivery_Capacity,Battery_Capacity,\
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
        if(len(check_time(route_copy,instance,Dis_List)) == 0 or check_dis(route_copy,instance,Dis_List) == 0):
            continue
        cur_dis = Dis_List[route[idx]][customer][2] + Dis_List[customer][route[idx - 1]][2]\
                  - Dis_List[route[idx]][route[idx - 1]][2]
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