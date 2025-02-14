# Multi_charge

## 文件

### global_parameter.py
#### 功能
声明全局常量

#### 常量介绍
```pycon
Delivery_Capacity = 500 # 送货车最大载货量
Battery_Capacity = 50 # 送货车电池容量
Delivery_Cost = 1000 # 每辆送货车的价格
P_Dis_Charge = 1 # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = 1 # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = 1 # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = 1 # 充电车距离和时间的系数，距离乘以系数为时间

```

### data_generate.py
#### 功能
数据生成文件

格式：``.csv``

#### 数据存储结构：

第一行：``N`` 表示有 `N`个客户点

后 `N + 2` 行 ：每行表示一个客户点，其中第 `2` 行和第 `N +  3` 行为仓库，且数据一样

**数据保证：**

坐标上，任意两点满电量可达。

时间窗上，至少直接从仓库出发并返回满足条件。

每行包括以下几个元素：

| 元素    | 符号  | 范围            |
|-------|-----|---------------|
| 经度    | x   | [-180, 180]   |
| 纬度    | y   | [-90, 90]     |
| 服务时间  | s   | [10, 30]      |
| 时间窗左端 | tl  | [0, 840]      |
| 时间窗右端 | tr  | [tl + s, 840] |
| 载货量   | q   | [10, 100]     |

**example** 

| 行数  | 序号  | 经度  | 纬度  | 最早开始 | 最晚开始 | 载货量 | 服务时间 |
|-----|-----|-----|------|------|------|-----|------|
| 1   | 0   | 19  | -60  | 0    | 840  | 0   | 0    |
| 2   | 1   | 229 | -153 | 374  | 432  | 75  | 25   |
| 3   | 2   | 147 | -179 | 532  | 828  | 12  | 10   |
| 4   | 3   | 166 | -93  | 439  | 764  | 1   | 15   |
| 5   | 4   | 93  | -148 | 572  | 589  | 70  | 14   |
| 6   | 5   | 164 | -167 | 152  | 705  | 65  | 14   |
| 7   | 6   | 19  | -60  | 0    | 840  | 0   | 0    |



### fit.py
入口文件

### read_data.py
读取数据，将每一个属性存成列表类型返回，具体存储结构见 `test.py` 介绍

### test.py
#### 功能
`main`函数，存储问题设定数据，设置随机种子

#### 数据存储
数据存储为一个字典类型，每一个字符串类型的键，对应一个列表类型的值，每一个列表代表 `idx` 为 `0 ~ N + 1` 客户点相应属性的值

其中，``idx`` 为 ``0,N + 1`` 的点为仓库

举例说明：查找第 5 个客户点的经度 ：``instance['x'][5]``

具体键值对如下：
```python
instance = {} # 定义问题设定字典
instance['N'] = int(N) # 客户点数
instance['x'] = x # 每个客户的经度
instance['y'] = y # 每个客户的纬度
instance['tl'] = tl # 每个客户的时间窗左端
instance['tr'] = tr # 每个客户的时间窗右端
instance['q'] = q # 每个客户的货物载量
instance['s'] = s #每个客户的服务时间 (数据保证了 tr - tl >= s)
```
#### main 函数
1. 通过  `LNS()` 获得送货车路径池
2. 通过  `check()` 获得充电车选取的充电点
3. 绘图


### LNS_SPP.py
#### 功能
获取只考虑送货车的路线池

#### 全局变量介绍
```pycon
NonImp = 0 # 连续没有提升的次数，也是每次删除操作的点数
instance = [] # 问题设定
Dis_List = [] # 任意两点距离列表
Remove_Pool = [] # 删除操作符池
Insert_Pool = [] # 插入操作符池
T0 = 187
q = 0.88
```
#### 主要函数介绍
`def Init():`
1. 作用：初始化变量，包括 `instance`、 `Dis_List`

`def Init_Dis():`
1. 作用：初始化任意两个点的距离
2. 输出：一个二维列表，每一行代表一个点和其他点的关系，每行的每个元素为一个 `[i,j,dis]` 列表 ，表示点 `i` 到点 `j` 距离为 `dis`
3. 用法： `Dis_List[i][j][2]` : 客户点 `i` 和客户点 `j` 之间的距离

`def Get_Distance(a,b):`
1. 作用：查询两个用户点之间的距离 
2. 输入：两个点的 `idx`
3. 输出：两个点的距离（四舍五入为整数）

`def Get_Init_Sol():`
1. 作用：获得一个路线池及其花费

`def Distroy_and_Repair(cur_sol,removal_id,insert_id):`
1. 作用：将当前路径池进行一次删除和擦入操作，返回操作后的路线池。
2. 输入：
    1. `cur_sol`:路线池
    2. `removal_id` : 一个删除操作的编号
    3. `insert_id` : 一个插入操作的编号
3. 输出：
    1. 一个二维列表，表示经过操作后的路线池
    2. 一个整数，表示该路线池的花费

`def LNS(instance):` 
1. 作用：获得一个路线池及其花费
2. 输入：
   1. `instance`: 问题设定
3. 输出：
   1. `best_sol`: 最佳路线池
   2. `best_cost`: 最佳路线池对应的花费
   3. `Dis_List`: 任意两点距离列表
   4. `time_window`: 最佳路线池对应的时间窗

#### 删除操作符
`def Random_Remove(cur_sol):`
1. 编号：1
2. 方法：随机

`def Distance_Related_Remove(cur_sol):`
1. 编号：2
2. 方法：计算所有其他客户与所选择客户之间的距离，并删除距离较近的客户。

#### 插入操作符
`def Random_Ins(cur_sol,bank):`
1. 编号：1
2. 方法：随机



### local_search.py
#### 功能
邻域搜索，对LNS中，更优秀的解进行邻域搜索

**基本思路：** 按顺序尝试每一个邻域搜索操作符，如果经过某个操作符后，结果变好了，则退回到第一个操作符。

**结束条件：** 直到连续尝试了len(LocalOperator_Pool) 个操作符都没有提升。

### function.py
#### 功能
存储一些通用的功能类函数


#### 主要函数介绍
`def Get_Route_Cost(route):`
1. 作用：查询一条路径的花费,不算购车花费
2. 输入：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，N + 1`)
3. 输出：路径总花费（四舍五入为整数）


`def Get_Sol_Cost(sol):`
1. 作用：查询一个解（路线池）的总花费
2. 输入：路线池，一个二维列表，每一行为一条路径，每条路径包括一些用户的 `idx`(每行第一个和最后一个元素分别为 `0，num + 1`)
3. 输出：一个整数，表示这个路径池的总消费（包括距离换算成电量，电量换算为花费，加上每条路径购置送货车的花费）


`def Check_Time(route):`
1. 作用：检查一条路径是否符合时间窗，如果符合，则返回该路径下，每个点的时间窗。
2. 输入：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)、
3. 输出：二维列表，每行代表一个点到达的时间窗，一个时间窗包括两个元素，第一个元素为最早到达时间，第二个元素为最晚离开时间，当列表为空的时候，表示不合法路径
      e.g:`time_window[i][0]`: `route[i]` 的最早可达时间
          `time_window[i][1]`: `toure[i]` 的最晚离开时间
4. 思路：
   1. 从后向前遍历，获得每个点可以最晚离开的时间，如果一个点的最晚离开时间 + 服务时间 > tr 则判定为不合法
   2. 从前到后遍历，获得每个点可以最早到达的时间


`def Ins_Customer_To_Route(customer,route):`
1. 作用：将一个用户插入到一条路径的最佳位置，如果不能插入，则返回 `INF`
2. 输入：
   1. `customer`:一个 `idx`
   2. `route`：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)
3. 输出：
   1. 最佳插入位置
   2. 插入该位置后，路线的总消费，不包括购车花费。

`def Remove(bank, cur_sol):`
1. 从当前路线池中，删除一些点，返回操作后的路线池
2. 输入：
   1. `bank`:一个存有需要删除点的 `idx` 的列表
   2. `cur_sol`:路线池，一个二维列表，每一行为一条路径，每条路径包括一些用户的 `idx`(每行第一个和最后一个元素分别为 `0，num + 1`)
3. 输出：一个二维列表，表示删除相应点后的路线池


### feasiblity.py
#### 功能
挑选充电的点

#### 函数
`def check(route_pool,instance,Dis_List): `
1. 输入 
   1.  `route_pool` : 路线池
   2.  `instance` : 数据
2. 输出
   1. 一个列表，存储需要充电的点的 `idx`
3. 问题设定：假设充电时间是远小于服务时间的，在不考虑时间时间窗的条件下，求解每条线路的最佳充电位置
4. 思路：
   1. 对于每一个点，只有充电或者不冲电两种选择（贪心的讲，如果充电则直接充满）
   2. ```python
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
      ```
   

`def check_with_regular_time(route_pool,instance,Dis_List,Time_Window): `
1. 问题设定：考虑时间窗和充电时间问题，假设服务结束后马上离开，从0时刻出发，预处理每个点的充电时长 `f[i]`
2. 思路：
   1. 对于每一点，也只有充电或者不充电俩种选择，充电则冲到固定时间（不超过电池容量）
   2. 状态表示
      ```python
        dp[0][Battery_Capacity][1][0] = 0 # 离开0点，有B的电量，没有充电，的代价
        dp[0][Battery_Capacity][1][1] = 0 # 离开0点，有B的电量，充电后，最后一个充电的点
      ```
   2. ```python
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

                if(j <= Battery_Capacity - f[i]): # 不会充溢出
                    dp[i][j + f[i]][1][0] = dp[i][j][0][0] + disj
                    dp[i][j + f[i]][1][1] = i
                    Pre_Node[i][j + f[i]][1] = copy.deepcopy(Pre_Node[i][j][0])
                    Pre_Node[i][j + f[i]][1].append(i)

                else:
                    dp[i][Battery_Capacity][1][1] = i
                    if (dp[i][Battery_Capacity][1][0] > dp[i][j][0][0] + disj):
                        dp[i][Battery_Capacity][1][0] =dp[i][j][0][0] + disj
                        Pre_Node[i][Battery_Capacity][1] = copy.deepcopy(Pre_Node[i][j][0])
                        Pre_Node[i][Battery_Capacity][1].append(i)
       ```   


`def check_with_timewindow(route_pool,instance,Dis_List,Time_Window):`
1. 问题设定：考虑时间窗，同时每个点可以线性的充电，根据时间窗限制，每个点有一个最长充电时间（跟当前状态也有关）
2. 思路：
   1. 每个点要根据转移来的状态，确定当前状态可以充电的时间范围，选择充电量
   2. 状态表示：离开 i 点，有 j 电量，充了 k $$ \belong [0,B]$$  的电
      3. ```python
        dp[0][Battery_Capacity][Battery_Capacity][0] = 0 # 代价
        dp[0][Battery_Capacity][Battery_Capacity][1] = 0 # 最后一个充电的点
        dp[0][Battery_Capacity][Battery_Capacity][2] = 0 # 到达时间
        dp[0][Battery_Capacity][Battery_Capacity][3] = 0 # 离开时间
         ```
   3. ```python
        for i in range(1,N):

            dis = Dis_List[route[i]][route[i - 1]][2]
            charge = dis * P_Dis_Charge
            time = dis * P_Delivery_Speed

            time_R = Time_Window[index][i][1] + instance['s'][route[i]] # 必须，最晚离开的时间

            # 不充电
            for j in range(0,Battery_Capacity + 1):
                if(j + charge <= Battery_Capacity):
                    for k in range(0,Battery_Capacity + 1):
                        if(k <= j + charge):
                            if(dp[i][j][0][0] >= dp[i - 1][j + charge][k][0] and dp[i - 1][j + charge][k][3] + time + instance['s'][route[i]] <= time_R):
                                if(dp[i][j][0][0] > dp[i - 1][j + charge][k][0]):
                                    dp[i][j][0][0] = dp[i - 1][j + charge][k][0]
                                    dp[i][j][0][1] = dp[i - 1][j + charge][k][1]
                                    dp[i][j][0][2] = dp[i - 1][j + charge][k][3] + time # 到达时间
                                    dp[i][j][0][3] = max(dp[i][j][0][2],instance['tl'][route[i]]) + instance['s'][route[i]] # 离开时间
                                    Pre_Node[i][j][0] = copy.deepcopy(Pre_Node[i - 1][j + charge][k])
                                else:# 代价相等，取离开时间更早的，
                                    tmp_3 = max(dp[i - 1][j + charge][k][3] + time,instance['tl'][route[i]]) + instance['s'][route[i]] # 离开时间
                                    if(dp[i][j][0][3] > tmp_3):
                                        dp[i][j][0][1] = dp[i - 1][j + charge][k][1]
                                        dp[i][j][0][2] = dp[i - 1][j + charge][k][3] + time  # 到达时间
                                        dp[i][j][0][3] = max(dp[i][j][0][2], instance['tl'][route[i]]) + instance['s'][
                                            route[i]]  # 离开时间
                                        Pre_Node[i][j][0] = copy.deepcopy(Pre_Node[i - 1][j + charge][k])
            # 充电
            for j in range(0,Battery_Capacity + 1):
                k1 = Battery_Capacity - j
                k2 = dp[i][j][0][2]
                for k in range(1, j + 1):
                    charge_time = k * P_Charge_Time
                    pre = dp[i][j - k][0][1]
                    if (pre == -1):
                        continue
                    dp[i][j][k][0] = dp[i][j - k][0][0] + Dis_List[route[i]][route[pre]][2]
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

        ```

### draw.py
#### 功能
绘制该问题设定的图像，内容包括：
1. 仓库：红色五角星
2. 客户点：蓝色圆圈（注释为 `number:time_l,time_r` 点编号：最早到达，最晚离开）
3. 送货车路线：不同路线设置为不同颜色（注释为，两点之间的时间花费）
4. 选取的充电点：黄色圆圈
                                          
## 流程
1. 入口 ： ``fit.py``
2. 调 ``test.py`` 读入数据，同时调用 ``main``获取初始路线池
3. ``LNS``:
   1. 获取初始解 ``get_init_sol``： 按顺序尝试每一个可插入位置，找到最佳目前最佳插入位置，不能插入时，新建一条路线。
   2. 退火：通过不同的删除和插入操作，不断重构解，如果变好了，就保留，如果变差了，就概率保留。
4. `check()`:获取充电点


## 题目假设
1. 任意两点，满电量可达
