import global_parameter as gp
import numpy as np


Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间


def check(route_pool,instance,Dis_List): #DP部分
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
        while (pre != -1):
            ANS.append(route[pre])
            cus = round(Dis_List[route[now]][route[pre]][2] * P_Dis_Charge)
            J = J + cus - KK  # pre 点对应的剩余电量
            K = KK  # pre 点对应的充电量
            now = pre
            pre = dp[now][J][K][2]  # pre 的前一个点
            KK = dp[now][J][K][3]  # pre 前一个点对应的充电量

    return ANS