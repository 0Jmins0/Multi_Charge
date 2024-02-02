import copy
import random
import time
import global_parameter as gp
from source.function import Get_Route_Cost, reverse_elements_between, check_time, check_dis

Remove_Pool = gp.Remove_Pool # 删除操作池
Insert_Pool = gp.Insert_Pool # 插入操作池
LocalOperator_Pool = gp.LocalOperator_Pool # 邻域操作池

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间
Lambda_Value = gp.Lambda_Value

Max_Time = gp.Max_Time

#单个路径内

# 选取一个路线中的任意两点，翻转包括其在内的中间的点
def opt2_exchange(new_sol,instance,Dis_List):

    num_of_route = len(new_sol)
    # print("OPT_before",new_sol,'\n',Get_Sol_Cost(new_sol))
    for idx in range(num_of_route):
        # 选取一条路径处理
        route_idx = idx
        route = copy.deepcopy(new_sol[route_idx])

        route_cost = Get_Route_Cost(route,instance,Dis_List)

        # 路径中少于两个点
        if(len(route) < 4):
            continue

        for i in range(1,len(route) - 2):
            for j in range(i + 1,len(route) - 1):
                index1 ,index2= i,j
                tmp_route = reverse_elements_between(route, index1, index2)
                tmp_cost = Get_Route_Cost(tmp_route,instance,Dis_List)

                if (len(check_time(tmp_route,instance,Dis_List)) == 0 or check_dis(tmp_route,instance,Dis_List) == 0):
                    continue
                # 检查是否代价更小
                if (tmp_cost < route_cost):
                    new_sol[route_idx] = tmp_route
                    # print(tmp_cost,route_cost,Get_Sol_Cost(new_sol))
                    return new_sol
    # print("OPT_after", new_sol,'\n',Get_Sol_Cost(new_sol))
    return new_sol

# 选取一条路线中连续的两点，将其放在其他位置
def or_opt(new_sol,instance,Dis_List):
    Count = 1

    num_of_route = len(new_sol)
    # print("OPT_before",new_sol,'\n',Get_Sol_Cost(new_sol))
    for idx in range(num_of_route):
        # 选取一条路径处理
        route_idx = idx
        route = copy.deepcopy(new_sol[route_idx])
        route_cost = Get_Route_Cost(route,instance,Dis_List)
        # print('1',len(route))
        # 路径中少于三个点
        if(len(route) < 5):
            Count = Count + 1
            continue

        for i in range(1,len(route) - 2):
            for j in range(1,len(route) - 4):
                # 选取路径中连续的两点
                index1 = i
                index2 = index1 + 1

                ele1 = route[index1]
                ele2 = route[index2]

                route.remove(ele1)
                route.remove(ele2)

                index3 = j
                index4 = index3 + 1

                route.insert(index3, ele1)
                route.insert(index4, ele2)

                tmp_cost = Get_Route_Cost(route,instance,Dis_List)

                if (len(check_time(route,instance,Dis_List)) == 0 or check_dis(route,instance,Dis_List) == 0):
                    continue

                # 检查是否代价更小
                if (tmp_cost < route_cost):
                    new_sol[route_idx] = route
                    # print(tmp_cost,route_cost,Get_Sol_Cost(new_sol))
                    return new_sol
        # print('2',len(route))
    # print("OPT_after", new_sol,'\n',Get_Sol_Cost(new_sol))
    return new_sol

# 路径间

# 选择路径1的节点A和路径2的节点B，交换它们，并将A后面的节点接到B的位置，将B后面的节点接到A的位置。
def opt2_exchange_mul(new_sol,instance,Dis_List):
    # Opt-2交换多次的局部搜索函数

    num_of_route = len(new_sol)
    if num_of_route  < 2:
        return new_sol

    for index1 in range(num_of_route):
        for index2 in range(index1 + 1,num_of_route):
        # 选择两个路径
            route1 = copy.deepcopy(new_sol[index1])
            route2 = copy.deepcopy(new_sol[index2])

            # 计算当前两路径的成本
            cost = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

            # 如果某个路径的长度小于4，则无法进行切割交换
            if len(route1) < 4 or len(route2) < 4:
                continue

            # 选择切割点
            for cut1 in range(1,len(route1) - 2):
                for cut2 in range(1, len(route2) - 2):
                    # 切割并交换部分路径
                    route1_L = route1[:cut1]
                    route1_R = route1[cut1:]
                    route2_L = route2[:cut2]
                    route2_R = route2[cut2:]

                    route1_new = route1_L + route2_R
                    route2_new = route2_L + route1_R

                    # 检查交换后路径的约束条件
                    if (len(check_time(route1_new,instance,Dis_List)) == 0 or check_dis(route1_new,instance,Dis_List) == 0 or
                            len(check_time(route2_new,instance,Dis_List)) == 0 or check_dis(route2_new,instance,Dis_List) == 0):
                        continue

                    # 计算交换后的成本
                    cost_new = Get_Route_Cost(route1_new,instance,Dis_List) + Get_Route_Cost(route2_new,instance,Dis_List)

                    # 如果成本降低，则接受新解，并立即返回
                    if cost > cost_new:
                        new_sol[index1] = route1_new
                        new_sol[index2] = route2_new
                        return new_sol

    return new_sol

#选择路径1的节点A，将A从路径1中删除，并将A插入到路径2的合适位置。
def relocate_operator(new_sol,instance,Dis_List):
    # 重新定位操作符的局部搜索函数

    num_of_route = len(new_sol)
    if num_of_route < 2:
        return new_sol

    for index1 in range(num_of_route):
        for index2 in range(index1 + 1, num_of_route):
            # 选择两个路径
            route1 = copy.deepcopy(new_sol[index1])
            route2 = copy.deepcopy(new_sol[index2])

            # 计算当前两路径的成本
            cost = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

            # 如果某个路径的长度小于3，则无法进行重新定位
            if len(route1) < 4 or len(route2) < 3:
                continue

            # 选择一个节点并将其从一个路径中移除，插入到另一路径中的比较好的位置
            for node_index in range(1, len(route1) - 1):
                for insert_index in range(1,len(route2) - 1):
                    tmp_r1 = copy.deepcopy(route1)
                    tmp_r2 = copy.deepcopy(route2)
                    relocated_node = tmp_r1.pop(node_index)
                    tmp_r2.insert(insert_index, relocated_node)

                    # 检查路径约束条件
                    if not (check_time(tmp_r1,instance,Dis_List) and check_dis(tmp_r1,instance,Dis_List) and
                            check_time(tmp_r2,instance,Dis_List) and check_dis(tmp_r2,instance,Dis_List)):
                        continue

                    # 计算重新定位后的成本
                    cost_new = Get_Route_Cost(tmp_r1,instance,Dis_List) + Get_Route_Cost(tmp_r2,instance,Dis_List)

                    # 如果成本降低，则接受新解，立即返回
                    if cost > cost_new:
                        new_sol[index1] = tmp_r1
                        new_sol[index2] = tmp_r2
                        return new_sol


    return new_sol

#选择路径1的节点A和路径2的节点B，交换它们，将A放回路径1，将B放回路径2。
def exchange_operator(new_sol,instance,Dis_List):

    num_of_route = len(new_sol)
    if num_of_route < 2:
        return new_sol

    for index1 in range(num_of_route):
        for index2 in range(index1 + 1, num_of_route):

            route1 = copy.deepcopy(new_sol[index1])
            route2 = copy.deepcopy(new_sol[index2])

            cost = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

            if len(route1) < 3 or len(route2) < 3:
                continue
            for node_index1 in range(1, len(route1) - 1):
                for node_index2 in range(1, len(route2) - 1):
                    route1[node_index1], route2[node_index2] = route2[node_index2], route1[node_index1]

                    if not (check_time(route1,instance,Dis_List) and check_dis(route1,instance,Dis_List) and
                            check_time(route2,instance,Dis_List) and check_dis(route2,instance,Dis_List)):
                        continue

                    cost_new = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

                    if cost > cost_new:
                        new_sol[index1] = route1
                        new_sol[index2] = route2
                        return new_sol

    return new_sol

def cross_exchange_operator(new_sol,instance,Dis_List):
    num_of_route = len(new_sol)
    if num_of_route < 2:
        return new_sol

    for path_index1 in range(num_of_route):
        for path_index2 in range(path_index1 + 1, num_of_route):
            route1 = copy.deepcopy(new_sol[path_index1])
            route2 = copy.deepcopy(new_sol[path_index2])

            cost = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

            if len(route1) < 5 or len(route2) < 5:
                continue
            for node_index1 in range(1, len(route1) - 2):
                node_index2 = node_index1 + 1
                # 获取第一个子序列
                segment1 = route1[node_index1:node_index2 + 1]
                # 随机选择该路径上的两个连续的节点，构成另一个路径的子序列
                for node_index3 in range(1, len(route2) - 2):
                    node_index4 = node_index3 + 1
                    # 获取第二个子序列
                    segment2 = route2[node_index3:node_index4 + 1]

                    # 将第一个子序列放到第二个子序列的位置
                    route2[node_index3:node_index4 + 1] = segment1
                    # 将第二个子序列放到第一个子序列的位置
                    route1[node_index1:node_index2 + 1] = segment2

                    if not (check_time(route1,instance,Dis_List) and check_dis(route1,instance,Dis_List) and
                            check_time(route2,instance,Dis_List) and check_dis(route2,instance,Dis_List)):
                        continue

                    cost_new = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

                    if cost > cost_new:
                        new_sol[path_index1] = route1
                        new_sol[path_index2] = route2
                        return new_sol

    return new_sol


def lambda_interchange_operator(new_sol,instance,Dis_List):
    num_of_route = len(new_sol)
    if num_of_route < 2:
        return new_sol

    for index1 in range(num_of_route):
        for index2 in range(index1 + 1, num_of_route):

            route1 = copy.deepcopy(new_sol[index1])
            route2 = copy.deepcopy(new_sol[index2])

            cost = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

            if len(route1) < Lambda_Value + 3 or len(route2) < Lambda_Value + 3:
                continue

            # 随机选择 λ 个节点，进行交换
            nodes_indices1 = random.sample(range(1, len(route1) - 1), Lambda_Value)
            nodes_indices2 = random.sample(range(1, len(route2) - 1), Lambda_Value)

            # 交换选定的节点
            for i in range(Lambda_Value):
                route1[nodes_indices1[i]], route2[nodes_indices2[i]] = route2[nodes_indices2[i]], route1[nodes_indices1[i]]

            if not (check_time(route1,instance,Dis_List) and check_dis(route1,instance,Dis_List) and
                    check_time(route2,instance,Dis_List) and check_dis(route2,instance,Dis_List)):
                continue

            cost_new = Get_Route_Cost(route1,instance,Dis_List) + Get_Route_Cost(route2,instance,Dis_List)

            if cost > cost_new:
                new_sol[index1] = route1
                new_sol[index2] = route2
                return new_sol
    return new_sol

def Local_Operate(new_sol,Operator_id,instance,Dis_List):
    if(Operator_id == 1):
        # print("LS_1")
        return opt2_exchange(new_sol,instance,Dis_List)
    elif(Operator_id == 2):
        # print("LS_2")
        return or_opt(new_sol,instance,Dis_List)
    elif(Operator_id == 3):
        return opt2_exchange_mul(new_sol,instance,Dis_List)
    elif(Operator_id == 4):
        return relocate_operator(new_sol,instance,Dis_List)
    elif(Operator_id == 5):
        return exchange_operator(new_sol,instance,Dis_List)
    elif(Operator_id == 6):
        return cross_exchange_operator(new_sol,instance,Dis_List)

def LS(new_sol,instance,Dis_List):
    # print("befor_LS",new_sol)
    begin_time = time.time()
    end_time = begin_time
    tmp_sol = new_sol
    cnt = 0
    pos = 0
    # print("LS",len(new_sol))
    while(end_time - begin_time < Max_Time and cnt != len(LocalOperator_Pool) - 1):
        # print("befor",new_sol)
        # print(LocalOperator_Pool[pos])
        new_sol = Local_Operate(new_sol,LocalOperator_Pool[pos],instance,Dis_List)
        # print("after",new_sol)
        # print(LocalOperator_Pool[pos],len(new_sol))
        if(tmp_sol != new_sol):
            cnt = 0
        else:
            cnt = cnt + 1

        pos = (pos + 1) % (len(LocalOperator_Pool) - 1)

    # print("After_LS",new_sol)
    return new_sol
