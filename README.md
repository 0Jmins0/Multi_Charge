# Multi_charge

## 文件
### data_geneerate.py
#### 功能
数据生成文件

格式：``.csv``

#### 数据存储结构：

第一行：``num`` 表示有 `num`个客户点

后 `num + 2` 行 ：每行表示一个客户点，其中第 `2` 行和第 `num +  3` 行为仓库，且数据一样

每行包括以下几个元素：

| 元素    | 符号  | 范围            |
|-------|-----|---------------|
| 经度    | x   | [0, 360]      |
| 纬度    | y   | [-180, 180]   |
| 服务时间  | s   | [10, 30]      |
| 时间窗左端 | tl  | [0, 840]      |
| 时间窗右端 | tr  | [tl + s, 840] |
| 载货量   | q   | [10, 100]     |

**example** （表头，以及最左一列的行数仅做说明，文件中没有存储）

| 行数  | 序号  | 经度  | 纬度  | 时间窗左端 | 时间窗右端 | 载货量 | 服务时间 |
|-----|-----|-----|------|-------|-------|-----|------|
| 1   | 5   |     |      |       |       |     |      |
| 2   | 0   | 19  | -60  | 0     | 840   | 0   | 0    |
| 3   | 1   | 229 | -153 | 374   | 432   | 75  | 25   |
| 4   | 2   | 147 | -179 | 532   | 828   | 12  | 13   |
| 5   | 3   | 166 | -93  | 439   | 764   | 1   | 15   |
| 6   | 4   | 93  | -148 | 572   | 589   | 70  | 14   |
| 7   | 5   | 164 | -167 | 152   | 705   | 65  | 14   |
| 8   | 6   | 19  | -60  | 0     | 840   | 0   | 0    |

### global_parameter.py
#### 功能
声明全局常量

#### 常量介绍
```pycon
Delivery_Capacity = 500 # 送货车最大载货量
Battery_Capacity = 100 # 送货车电池容量
Delivery_Cost = 1000 # 每辆送货车的价格
P_Dis_Charge = 1 # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = 1 # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = 1 # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = 1 # 充电车距离和时间的系数，距离乘以系数为时间

```

### fit.py
入口文件

### read_data.py
读取数据，将每一个属性存成列表类型返回，具体存储结构见 `test.py` 介绍

### test.py
#### 功能
`main`函数，存储问题设定数据，设置随机种子

#### 数据存储
数据存储为一个字典类型，每一个字符串类型的键，对应一个列表类型的值，每一个列表代表 `idx` 为 `0 ~ num + 1` 客户点相应属性的值

其中，``idx`` 为 ``0,num + 1`` 的点为仓库

举例说明：查找第 5 个客户点的经度 ：``instance['x'][5]``

具体键值对如下：
```python
num, x, y, tl, tr, q ,s= readmain(a)
instance = {} # 定义问题设定字典
instance['num'] = int(num) # 客户点数
instance['x'] = x # 每个客户的经度
instance['y'] = y # 每个客户的纬度
instance['tl'] = tl # 每个客户的时间窗左端
instance['tr'] = tr # 每个客户的时间窗右端
instance['q'] = q # 每个客户的货物载量
instance['s'] = s #每个客户的服务时间 (数据保证了 tr - tl >= s)
```

### LNS_SPP.py
#### 功能
获取只考虑送货车的路线池

#### 全局变量介绍
```pycon
NonImp = 0 # 连续没有提升的次数，也是每次删除操作的点数
instance = [] # 问题设定
Dis_List = [] # 任意两点距离列表
T0 = 187
q = 0.88
```
#### 主要函数介绍
`def Init():`
1. 作用：初始化变量，包括 `instance`、 `Dis_List`

`def Init_Dis():`
1. 作用：初始化任意两个点的距离
2. 输出：一个二维列表，每一行代表一个点和其他点的关系，每行的每个元素为一个 `[i,j,dis]` 列表 ，表示点 `i` 到点 `j` 距离为 `dis`,且每行按照 `dis` 递减 

`def Get_Init_Sol():`
1. 作用：获得一个路线池及其花费

`def Distance(a,b):`
1. 作用：查询两个用户点之间的距离 
2. 输入：两个点的 `idx`
3. 输出：两个点的距离（四舍五入为整数）

`def Route_Cost(route):`
1. 作用：查询一条路径的花费
2. 输入：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)
3. 输出：路径总花费（四舍五入为整数）

`def Sol_Cost(sol):`
1. 作用：查询一个解（路线池）的总花费
2. 输入：路线池，一个二维列表，每一行为一条路径，每条路径包括一些用户的 `idx`(每行第一个和最后一个元素分别为 `0，num + 1`)
3. 输出：一个整数，表示这个路径池的总消费（包括距离换算成电量，电量换算为花费，加上每条路径购置送货车的花费）

`def Check_Time(route):`
1. 作用：检查一条路径是否符合时间窗，如果符合，则返回该路径下，每个点的时间窗。
2. 输入：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)、
3. 输出：二维列表，每行代表一个点的时间窗，当列表为空的时候，表示不合法路径

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

### feasilblity.py
#### 功能
挑选充电的点

#### 函数
`def check(route_pool,instance): `
1. 输入 
   1.  `route_pool` : 路线池
   2.  `instance` : 问题设定
2. 输出
   1. 一个列表，存储需要充电的点的 `idx`
3. 思路
   1. 方程 `dp[i][j][k][0/1]` : 刚走到第 `i` 个点时，还剩 `j` 个电量，在 `i` 点充了 `k` 个电，
      1. 0：花费，
      2. 1：最晚充电的点
   2. 初始化
      1. `dp[][][][0] = INF`
      2. `dp[][][][1] = -1`
      3. `dp[0][100][0][0] = 0`
      4. `dp[0][100][0][1] = 0`
   3. 转移
      1. `cus = dis(i,i-1) * P_Dis_Charge` ： `i` 到 `i - 1` 的耗电量
      2. 
      ```python
      # 不充电：
      p = dp[i - 1][j - kk + cus][kk][1]
      if(dp[i][j][0][0] > dp[i - 1][j - kk + cus][kk][0]):
           dp[i][j][0][1] = p
           dp[i][j][0][0] = dp[i - 1][j - kk + cus][kk][0]
      
      # 充电
      if(dp[i][j][k][0] > dp[i - 1][j - kk + cus][kk][0] + (dis(i,p) * p_dis_charge + k) * P_Charge_Cost):
          dp[i][j][k][0] = dp[i - 1][j - kk + cus][kk][0] + (dis(i,p) * p_dis_charge + k) * P_Charge_Cost
          dp[i][j][k][1] = i
      ```
   4. 答案
      1. `ans = min(dp[n][][][0])`,对应 `J` 的剩余电量，充电量 `K` ,最后一次充电点 `now = dp[n][J][K][1]`
      2. 路线：
      ```python
      # for(pre = now - 1,pre >= 1,pre --)
      cus = dis(pre,now) * p_dis_charge
      if (ans == dp[pre][J + cus - kk][kk][0] + (dis(now,pre) * p_dis_charge + K) * P_Charge_Cost):
          ans -= (dis(now,pre) * p_dis_charge + K) * P_Charge_Cost
          now = pre
          K = kk
          J -= cus
          ANS.append(now)
      ```
   

                                          
## 流程
1. 入口 ： ``fit.py``
2. 调 ``test.py`` 读入数据，同时调用 ``main``获取初始路线池
3. ``LNS``:
   1. 获取初始解 ``get_init_sol``： 按顺序尝试每一个可插入位置，找到最佳目前最佳插入位置，不能插入时，新建一条路线。
   2. 退火：通过不同的删除和插入操作，不断重构解，如果变好了，就保留，如果变差了，就概率保留。
3. 删除操作：
   1. ``Random_Remove(instance,NonImp,cur_sol)`` 从当前路径池 ``cur_sol`` 中，随机删除 ``NonImp`` 个点
   2. ``Distance_Related_Remove(instasnce,NonUImp,Cur_sol,Dis_List`` 随机挑选一个点，删除掉与这个点距离最近的 ``min(N - 1,NonImp)`` 个点
   3. 
4. 插入操作：
   1. ``Random_Ins(instance,cur_sol,bank)`` 将删除掉的 ``bank`` 中的点，随机的插入到当前解 ``cur_sol`` 中





