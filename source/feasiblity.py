import copy

import global_parameter as gp
import numpy as np

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间
P_Charge_Time =  gp.P_Charge_Time # 充电量和时间的关系系数，时间乘以系数为充电量


def check(route_pool,instance,Dis_List,Time_Window):
    ANS = []

    for route in route_pool:
        N = len(route)
        dp = np.zeros((N + 2,Battery_Capacity + 1,2)).tolist()
        Pre_Node = [[] for _ in range(N)]
        Pre_Node[0].append(0)

        for i in range(0,N + 1):
            for j in range(0,Battery_Capacity + 1):
                dp[i][j][0] = float('inf')
                dp[i][j][1] = -1

        dp[0][Battery_Capacity][0] = 0
        dp[0][Battery_Capacity][1] = 0

        for i in range(1,N):
            dis = Dis_List[route[i]][route[i - 1]][2]
            charge = dis * P_Dis_Charge

            # 不充电
            for j in range(0,Battery_Capacity):
                if(j + charge <= Battery_Capacity):
                    dp[i][j][0] = dp[i - 1][j + charge][0]
                    dp[i][j][1] = dp[i - 1][j + charge][1]

            # 充电
            for j in range(0,Battery_Capacity):
                pre = dp[i][j][1]
                if(pre == -1):
                    continue
                disj = Dis_List[route[i]][route[pre]][2]
                chargej = disj * P_Dis_Charge
                if(dp[i][Battery_Capacity][0] > dp[i][j][0] + disj):
                    dp[i][Battery_Capacity][0] = dp[i][j][0] + disj
                    Pre_Node[i] = copy.deepcopy(Pre_Node[dp[i][j][1]])
                    Pre_Node[i].append(i)

            dp[i][Battery_Capacity][1] = i

        # for i in range(N):
        #     print(i,":",Pre_Node[i])

        # 回溯
        for node in Pre_Node[N - 1]:
            if(node != 0 and node != N - 1):
                ANS.append(route[node])

    return ANS


def check_with_timewindow(route_pool,instance,Dis_List,Time_Window):
    ANS = []

    for index,route in enumerate(route_pool):
        N = len(route)
        dp = np.zeros((N + 2,Battery_Capacity + 1,Battery_Capacity + 1,4)).tolist()

        Pre_Node = [[[[] for _ in range(Battery_Capacity + 1)] for _ in range(Battery_Capacity + 1)] for _ in range(N + 1)]


        for i in range(0,N + 1):
            for j in range(0,Battery_Capacity + 1):
                for k in range(0,Battery_Capacity + 1):
                    dp[i][j][k][0] = float('inf')
                    dp[i][j][k][1] = -1
                    dp[i][j][k][2] = 0
                    dp[i][j][k][3] = 0

        dp[0][Battery_Capacity][Battery_Capacity][0] = 0
        dp[0][Battery_Capacity][Battery_Capacity][1] = 0
        dp[0][Battery_Capacity][Battery_Capacity][2] = 0 # 到达时间
        dp[0][Battery_Capacity][Battery_Capacity][3] = 0 # 离开时间

        for i in range(1,N):

            dis = Dis_List[route[i]][route[i - 1]][2]
            charge = dis * P_Dis_Charge
            time = dis * P_Delivery_Speed

            time_L = Time_Window[index][i][0] + instance['s'][route[i]] # 能够，最早离开旳时间
            time_R = Time_Window[index][i][1] + instance['s'][route[i]] # 必须，最晚离开的时间

            # 不充电
            for j in range(0,Battery_Capacity + 1):
                if(j + charge <= Battery_Capacity):
                    # dp[i][j][0][0] = dp[i - 1][j + charge][0][0]
                    # dp[i][j][0][1] = dp[i - 1][j + charge][0][1]
                    for k in range(0,Battery_Capacity + 1):
                        if(k <= j + charge):
                            if(dp[i][j][0][0] > dp[i - 1][j + charge][k][0] and dp[i - 1][j + charge][k][3] + time + instance['s'][route[i]] < time_R):
                                dp[i][j][0][0] = dp[i - 1][j + charge][k][0]
                                dp[i][j][0][1] = dp[i - 1][j + charge][k][1]
                                dp[i][j][0][2] = dp[i - 1][j + charge][k][3] + time # 到达时间
                                dp[i][j][0][3] = max(dp[i][j][0][2],instance['tl'][route[i]]) + instance['s'][route[i]] # 离开时间
                                Pre_Node[i][j][0] = copy.deepcopy(Pre_Node[i - 1][j + charge][k])

                # print('i:',i," j:",j," prenode:",Pre_Node[i][j][0])
                    # early_charge_finish = dp[i - 1][j + charge][2] + dp[i - 1][j + charge][4]
                    # early_serve_finish = max(dp[i - 1][j + charge][2],instance['tl'][route[i]]) + instance['s'][route[i]]

            # 充电
            for j in range(0,Battery_Capacity + 1):
                for k in range(1, j + 1):
                    charge_time = k * P_Charge_Time
                    pre = dp[i][j - k][0][1]
                    if (pre == -1):
                        continue
                    dp[i][j][k][0] = dp[i][j - k][0][0] + Dis_List[route[pre]][route[i]][2]
                    dp[i][j][k][1] = i
                    dp[i][j][k][2] = dp[i][j - k][0][2]
                    if(dp[i][j][k][2] < instance['tl'][route[i]]): # 如果到达时间小于最早服务时间，可以先开始充电，可边服务边充电
                        dp[i][j][k][3] = max(dp[i][j][k][2] + charge_time,instance['tl'][route[i]] + instance['s'][route[i]])
                    else:
                        dp[i][j][k][3] = dp[i][j][k][2] + max(charge_time,instance['s'][route[i]])
                    if(dp[i][j][k][3] > time_R):
                        dp[i][j][k][0] = float('inf')
                        dp[i][j][k][1] = -1
                        continue
                    Pre_Node[i][j][k] = copy.deepcopy(Pre_Node[i][j - k][0])
                    Pre_Node[i][j][k].append(i)
                    # print('i:',i," j:",j,' k:',k, " pre:", pre, "prenode:",Pre_Node[i][j][k],"pre list",Pre_Node[i][j - k][0])

        Min_dis = float('inf')
        Min_disj = -1
        Min_disk = -1

        for j in range(0,Battery_Capacity + 1):
            for k in range(1,Battery_Capacity + 1):
                if(Min_dis > dp[N - 1][j][k][0]):
                    Min_dis = dp[N - 1][j][k][0]
                    Min_disj = j
                    Min_disk = k
        # print("Min_dis",Min_dis)
        # print("Min_disj",Min_disj)
        # print("Min_disk",Min_disk)
        # print(Pre_Node[N - 1][Min_disj][Min_disk])

        # print(Pre_Node)

        # for i in range(N):
        #     print(i,":",Pre_Node[i])

        # 回溯
        for node in Pre_Node[N - 1][Min_disj][Min_disk]:
            if (node != 0 and node != N - 1):
                ANS.append(route[node])

    return ANS


def check_with_regular_time(route_pool,instance,Dis_List,Time_Window): #DP部分

    ANS = []
    for route in route_pool:
        N = len(route)

        begin = 0 # 到达时间
        end = 0 # 离开时间
        f = np.zeros(N).tolist()

        # 预处理充电量
        for i in range(1,N):
            begin = end + Dis_List[route[i]][route[i - 1]][2] * P_Delivery_Speed
            end = max(instance['tl'][route[i]] + instance['s'][route[i]],begin + instance['s'][route[i]])
            f[i] = (end - begin) * P_Charge_Time

        # print('f',f)
        # dp[i][j][0/1][0/1]
        # 离开第 i 个点，有 j 的电量时，（不充/充电）时的（消费/上一个充电的点）
        dp = np.zeros((N + 2, Battery_Capacity + 1,2, 2)).tolist()

        # Pre_Node[i][j][0/1]
        # 离开第 i 个点，有 j 的电量时, （不充/充电）的充电路径列表
        Pre_Node = [[[[] for _ in range(2)] for _ in range(Battery_Capacity + 1)] for _ in range(N + 1)]
        # Pre_Node[0].append(0)

        for i in range(0, N + 1):
            for j in range(0, Battery_Capacity + 1):
                dp[i][j][0][0] = float('inf')
                dp[i][j][0][1] = -1
                dp[i][j][1][0] = float('inf')
                dp[i][j][1][1] = -1

        # 默认仓库一定为充满电出发
        dp[0][Battery_Capacity][1][0] = 0
        dp[0][Battery_Capacity][1][1] = 0



        for i in range(1, N):

            # i - 1 到 i 的耗电量
            dis = Dis_List[route[i]][route[i - 1]][2]
            charge = dis * P_Dis_Charge

            # 不充电
            # dp[i][j][0][0] <--- dp[i - 1][j + charge][0/1][0]
            for j in range(0, Battery_Capacity):
                if (j + charge <= Battery_Capacity):
                    if(dp[i - 1][j + charge][0][0] < dp[i][j + charge][1][0]):
                        dp[i][j][0][0] = dp[i - 1][j + charge][0][0]
                        dp[i][j][0][1] = dp[i - 1][j + charge][0][1]
                        Pre_Node[i][j][0] = copy.deepcopy(Pre_Node[i - 1][j + charge][0])
                    else:
                        dp[i][j][0][0] = dp[i - 1][j + charge][1][0]
                        dp[i][j][0][1] = dp[i - 1][j + charge][1][1]
                        Pre_Node[i][j][0] = copy.deepcopy(Pre_Node[i - 1][j + charge][1])

            # 充电
            for j in range(0, Battery_Capacity):
                pre = dp[i][j][0][1]
                if(pre == -1):
                    continue
                disj = Dis_List[route[i]][route[pre]][2]
                chargej = disj * P_Dis_Charge

                if(j <= Battery_Capacity - f[i]):
                    dp[i][j + f[i]][1][0] = dp[i][j][0][0] + disj
                    dp[i][j + f[i]][1][1] = i
                    Pre_Node[i][j + f[i]][1] = copy.deepcopy(Pre_Node[i][j][0])
                    Pre_Node[i][j + f[i]][1].append(i)

                else:
                    dp[i][Battery_Capacity][1][1] = i
                    if (dp[i][Battery_Capacity][1][0] > dp[i][j][0][0] + disj):
                        dp[i][Battery_Capacity][1][0] = min(dp[i][Battery_Capacity][1][0],dp[i][j][0][0] + disj)
                        Pre_Node[i][Battery_Capacity][1] = copy.deepcopy(Pre_Node[i][j][0])
                        Pre_Node[i][Battery_Capacity][1].append(i)
                # if(i == N - 1 and Min_dis > dp[i][min(j + f[i],Battery_Capacity)][1][0]):
                #     Min_dis = dp[i][min(j + f[i],Battery_Capacity)][1][0]

        Min_dis = float('inf')
        Min_disj = -1
        Min_disk = -1

        for j in range(f[N - 1],Battery_Capacity + 1):
            for k in range(1,2):
                if(Min_dis > dp[N - 1][j][k][0]):
                    Min_dis = dp[N - 1][j][k][0]
                    Min_disj = j
                    Min_disk = k

        # print("Min_dis",Min_dis)
        # print("Min_disj",Min_disj)
        # print("Min_disk",Min_disk)
        # print(Pre_Node[N - 1][Min_disj][Min_disk])


        # for i in range(N):
        #     print(i,":",Pre_Node[i])

        # 回溯
        for node in Pre_Node[N - 1][Min_disj][Min_disk]:
            if (node != 0 and node != N - 1):
                ANS.append(route[node])

    return ANS
