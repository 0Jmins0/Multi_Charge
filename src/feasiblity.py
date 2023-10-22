import random
import numpy
import numpy as np
from LNS_SPP import distance

Battery_Capacity = 100 # 电池容量
p_dis_cost = 1 # 距离和花费的系数，距离乘该系数为花费
p_dis_charge = 1 #距离和电量的系数，距离乘以系数为耗电量
def check(route_pool,instance): #DP部分
    bank = []
    number = instance['num'] # 客户总数
    for route in route_pool:
        route.insert(0, 0) # 加入起点仓库
        route.append(number + 1) # 加入最后一个点为 num + 1 ,代表仓库
        node_number = len(route) # 路径中点的数量
        # route[0],route[node_number - 1] 为仓库
        # route[1:node_number - 2] 为客户点

        #初始化dp矩阵为最大值
        dp: np.ndarray = np.array([[float('inf')] * (node_number + 10)] * (Battery_Capacity + 10))

        # 求距离前缀和
        sum_dis = 0
        sum_dis_list = []
        sum_dis_list.append(0)
        for i in range(1,node_number):
            sum_dis += distance(route[i],route[i - 1],instance)
            sum_dis_list.append(sum_dis)

        dp[0][Battery_Capacity] = 0 #满电量出发
        for i in range(0,node_number):
            for j in range(0,Battery_Capacity + 1):
                for k in range(0,i):
                    # 电车从 i 经过一系列点到 k 的耗电量
                    sum_dis = sum_dis_list[i] - sum_dis_list[k - 1]
                    consumption = int(sum_dis * p_dis_charge)

                    # 充电车从 i 到 k 的距离
                    dis = distance(route[i], route[k], instance)

                    #上一个充电的点，充电到 p 电量
                    for p in range(consumption,Battery_Capacity + 1):
                        dp[route[i]][j] = min(dp[route[i]][j],dp[route[k]][p] + dis)

        #回溯寻找路径
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