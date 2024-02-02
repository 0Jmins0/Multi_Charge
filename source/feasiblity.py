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
        dp = np.zeros((N + 2,Battery_Capacity + 1,5)).tolist()
        Pre_Node = [[] for _ in range(N)]
        Pre_Node[0].append(0)

        for i in range(0,N + 1):
            for j in range(0,Battery_Capacity + 1):
                dp[i][j][0] = float('inf')
                dp[i][j][1] = -1
                dp[i][j][2] = Time_Window[index][i][0] # 点 i 的最早到达时间（可能还不能开始服务）,但可以开始充电
                dp[i][j][3] = Time_Window[index][i][1] + instance['s'][route[i]] # 点 i 的最晚离开的时间
                dp[i][j][4] = 0 # 充电时间

        dp[0][Battery_Capacity][0] = 0
        dp[0][Battery_Capacity][1] = 0

        for i in range(1,N):
            dis = Dis_List[route[i]][route[i - 1]][2]
            charge = dis * P_Dis_Charge
            time  = dis * P_Delivery_Speed

            # 不充电
            for j in range(0,Battery_Capacity):
                if(j + charge <= Battery_Capacity):
                    dp[i][j][0] = dp[i - 1][j + charge][0]
                    dp[i][j][1] = dp[i - 1][j + charge][1]

                    early_charge_finish = dp[i - 1][j + charge][2] + dp[i - 1][j + charge][4]
                    early_serve_finish = max(dp[i - 1][j + charge][2],instance['tl'][route[i]]) + instance['s'][route[i]]

                    dp[i][j][2] = max(early_charge_finish,early_serve_finish) + time


            # 充电
            for j in range(Battery_Capacity - 1,0,-1):
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
        #     print(i + 1,":",Pre_Node[i])

        # 回溯
        for node in Pre_Node[N - 1]:
            if(node != 0 and node != N - 1):
                ANS.append(route[node])

    return ANS


def checkk(route_pool,instance,Dis_List): #DP部分
    ANS = []
    for route in route_pool:
        N = len(route) - 2

        # 初始化
        dp = np.zeros((N + 2, Battery_Capacity + 1, Battery_Capacity + 1, 4)).tolist()
        for i in range(0,N + 2):
            for j in range(0,Battery_Capacity + 1):
                for k in range(0,Battery_Capacity + 1):
                    dp[i][j][k][0] = float('inf')
                    dp[i][j][k][1] = -1
                    dp[i][j][k][2] = -1
                    dp[i][j][k][3] = 0

        dp[0][Battery_Capacity][0][0] = 0

        # 转移
        for i in range(1,N + 2):
            cus = round(Dis_List[route[i]][route[i - 1]][2] * P_Dis_Charge)
            for j in range(0,Battery_Capacity + 1):
                for k in range(0,Battery_Capacity - j + 1):
                    for kk in range(0,min(Battery_Capacity,j + cus + 1)):
                        # 不充电
                        # j - kk + cus >= 0
                        # j + k <= Battery_Capacity
                        if(j - kk + cus > Battery_Capacity ):
                            continue

                        p = dp[i - 1][j - kk + cus][kk][1]
                        if (dp[i][j][0][0] > dp[i - 1][j - kk + cus][kk][0]):
                            dp[i][j][0][0] = dp[i - 1][j - kk + cus][kk][0]
                            dp[i][j][0][1] = p
                            dp[i][j][0][2] = p
                            dp[i][j][0][3] = kk

                        # 充电
                        if (dp[i][j][k][0] > dp[i - 1][j - kk + cus][kk][0] + round(Dis_List[route[i]][route[p]][2] * P_Dis_Charge + k) * P_Charge_Cost):
                            dp[i][j][k][0] = dp[i - 1][j - kk + cus][kk][0] + round(Dis_List[route[i]][route[p]][2] * P_Dis_Charge + k) * P_Charge_Cost
                            dp[i][j][k][1] = i
                            dp[i][j][k][2] = p
                            dp[i][j][k][3] = kk

        # 回溯
        ans = float('inf')
        J = K = KK = now = pre = 0
        for j in range(0,Battery_Capacity + 1):
            for k in range(0,Battery_Capacity - j + 1):
                if(ans > dp[N +1][j][k][0]):
                    ans = dp[N + 1][j][k][0]
                    J = j
                    K = k
        now = dp[N + 1][J][K][1]
        pre = dp[N + 1][J][K][2]
        KK = dp[N + 1][J][K][3]
        now = N + 1
        print(f'route{route}')
        print(dp[1])
        print(f'now:{route[now]},pre:{route[pre]},K:{K},KK:{KK}')
        ANS_K = []
        while (pre != -1):
            ANS.append(route[pre])
            ANS_K.append(KK)
            cus = round(Dis_List[route[now]][route[pre]][2] * P_Dis_Charge)
            print(f"J:{J},K:{K},now:{route[now]},pre:{route[pre]},KK:{KK}")
            J = J + cus - KK  # pre 点对应的剩余电量
            K = KK  # pre 点对应的充电量
            now = pre
            pre = dp[now][J][K][2]  # pre 的前一个点
            KK = dp[now][J][K][3]  # pre 前一个点对应的充电量
        print("ANS:",ANS)
        print("ANS_K",ANS_K)
        charge = Battery_Capacity
        pos = len(ANS_K) - 1
        for i in range(0,N + 1):
            charge -= Dis_List[route[i]][route[i + 1]][2] * P_Dis_Charge
            print(f"DIS {route[i]} -> {route[i + 1]} {Dis_List[route[i]][route[i + 1]][2] * P_Dis_Charge}")
            print(f'node:{route[i + 1]},charge:{charge}')
            if(route[i + 1] in ANS):
                charge += ANS_K[pos]
                print(f"add_charge:{ANS_K[pos]}")
                pos -= 1

    return ANS