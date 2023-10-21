import random
import numpy
import numpy as np
from LNS_SPP import distance

Battery_Capacity = 100 # 电池容量
p_dis_cost = 1 # 距离和花费的系数，距离乘该系数为花费
p_dis_charge = 1 #距离和电量的系数，距离乘以系数为耗电量
def check(route_pool,instance): #DP部分
    bank = []
    for route in route_pool:
        node_number = len(route) #路径中点的数量
        dp = np.zeros([node_number + 10,Battery_Capacity + 10])
        for i in range(0,node_number):
            for j in range(0,Battery_Capacity):
                for k in range(0,i):
                    dis = distance(route[i],route[k],instance)
                    consumption =  dis * p_dis_charge
                    if(j >= consumption):
                        dp[route[i]][j] = min(dp[route[i]][j],dp[route[k]][j - consumption] + dis)
        Min_charge = float('inf')
        Min_dis = float('inf')
        now_node = node_number - 1
        for i in range(0,Battery_Capacity):
            if(Min_dis > dp[route[node_number]][i]):
                Min_dis = dp[route[node_number]][i]
                Min_charge = i
        now_charge = Min_charge
        for i in range(node_number + 1,0,-1):
            dis = distance(now_node,i,instance)
            consumption = dis * p_dis_charge
            if(dp[i][now_charge - consumption] + dis == dp[now_node][now_charge]):
                now_charge -= consumption
                now_node = i
                bank.append(i)
    return bank