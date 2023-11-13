# Created on iPad.
import random
import copy

from LNS_SPP import instance
from LNS_SPP import Dis_List
from LNS_SPP import NonImp
import LNS_SPP as LS
import global_parameter as gp

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间

def Distroy_and_Repair(cur_sol,Removal_id,Insert_id):
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


def Random_Remove(cur_sol): #Rem-1
    bank = [] #删除的节点
    new_sol = [] #新路线
    N = instance['N']
    bank = random.sample(range(1,N + 1),min(NonImp,N))
    # 如果不在被删除的列表里，则添加到新列表里
    new_sol = LS.Remove(bank,cur_sol)
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
    new_sol = LS.Remove(bank,cur_sol)
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
    new_sol = LS.Remove(bank,cur_sol)
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
    bank_copy = copy.deepcopy(bank)
    # print("bank",bank)
    for _ in range(len(bank_copy)):
        node = random.choice(bank)
        best_route = -1
        best_idx = -1
        best_cost = Delivery_Cost + 2 * LS.Get_Distance(0,node) * P_Dis_Charge * P_Charge_Cost
        for j in range(len(cur_sol)):
            # print(node,bank)
            cur_idx ,cur_cost = LS.Ins_Customer_To_Route(node,cur_sol[j])
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
    finall_cost = LS.Get_Sol_Cost(cur_sol)
    return cur_sol,finall_cost

