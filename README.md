# Multi_ch
## DP方案

``dp[i][j]``  : 走到点 `i` 进行充电，且充到 `j` 格电量，充电车走的最短距离

``dp[i][j] = min(dp[k][p] + dis(i,k),dp[i][j])``  : 上一个充电的点为 `k` ，且充到了 `p` 格电

``dis(i,k)``  : 充电车从 `i` 到 `k` 的距离

``sum_dis[i][k]``  : 电车从 `i` 经过一系列点，走到 `k` 一共需要的距离

``p_dis_charge``  : 距离和电量消耗的关系系数

`p` 的范围 ：`[sum_dis[i][k] * p_dis_charge,Battery_Capacity]`

复杂度：$O(n^4)$

```C++
# node_number 该条路径上的客户点加起点终点的数量
# route[0],route[node_number - 1] 为仓库
# route[1:node_number - 2] 为客户点
# dp数组初始化为 INF
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
```


## 一些问题

1. 何时检查一段路径相邻两点距离是否超过了满电量能走的距离，初始化路径的时候没有check这个问题，初始化的时候，如果和时间一起check很有可能找不到解陷入死循环，（e.g : 其他路径已经插不下了，当前剩下的点从仓库直接去不了），或者可以考虑造数据的时候，避免这种事情，保证仓库和任意点可达。
2. 充电时间对时间窗合法性的关系 ，挑选充电的点的同时如何保证在这些点充电可以始终满足时间窗（或者直接假设充电时间小于服务时间，但有点不符合实际）
3. 数据类型，距离为小数，电量为整数，直接四舍五入？





