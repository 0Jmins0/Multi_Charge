# Multi_ch、

## 文件
### Data_Geneerate
数据生成文件

数据存储结构：

文件：``.csv``

第一行：``num`` 表示有 `num`个客户点

后 `num + 2` 行 ：每行表示一个客户点，其中第 `2` 行和第 `num +  3` 行为仓库，且数据一样

每行包括以下几个元素：经度`(0-360)`，纬度`(-180,180)`，时间窗左端`(0-840)`，时间窗右端 `(时间窗左端-840)`，载货量 `(0-100)`，服务时间(`(10,30)`，数据保证小于时间窗)
### fit.py
入口文件
### readData.py
读取数据，将每一个属性存成列表类型返回，具体存储结构见 `test.py` 介绍

### test.py
`main`函数，存储数据，设置随机种子

数据读取和存储为一个字典类型，每一个字符串类型的键，对应一个列表类型的值，每一个列表代表 `idx` 为 `0 ~ num + 1` 客户点相应属性的值

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
获取只考虑送货车的路线池

#### 变量介绍
```pycon
Delivery_Capacity = 500 # 送货车最大载货量
Battery_Capacity = 100 # 送货车电池容量
Delivery_Cost = 1000 # 每辆送货车的价格
P_Dis_Charge = 1 # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = 1 # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = 1 # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = 1 # 充电车距离和时间的系数，距离乘以系数为时间
T0 = 187
q = 0.88
```
#### 主要函数介绍
`def LNS():` 邻域搜索获得一个路线池

`def Distance(a,b):`
1. 输入：两个点的 `idx`
2. 输出：两个点的距离（四舍五入为整数）

`def Route_Dis(route):`
1. 输入：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)
2. 输出：路径总长度（四舍五入为整数）

`def Sol_Cost(sol):`
1. 输入：路线池，一个二维列表，每一行为一条路径，每条路径包括一些用户的 `idx`(每行第一个和最后一个元素分别为 `0，num + 1`)
2. 输出：一个整数，表示这个路径池的总消费（包括距离换算成电量，电量换算为花费，加上每条路径购置送货车的花费）

`def Check_Time(route):`
1. 输入：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)、
2. 输出：二维列表，每行代表一个点的时间窗，当列表为空的时候，表示不合法路径

`def Ins_Customer_To_Route(customer,route):`
1. 输入：
   1. `customer`:一个 `idx`
   2. `route`：一个存有一条 **完整** 路径 `idx` 的列表(完整：第一个元素和最后一个元素分别为 `0，num + 1`)
2. 输出：
   1. 最佳插入位置
   2. 插入该位置后，路线的总消费，不包括购车花费。

`def Remove(bank, cur_sol):`
1. 输入：
   1. `bank`:一个存有需要删除点的 `idx` 的列表
   2. `cur_sol`:路线池，一个二维列表，每一行为一条路径，每条路径包括一些用户的 `idx`(每行第一个和最后一个元素分别为 `0，num + 1`)
2. 输出：一个二维列表，表示删除相应点后的路线池

`def Distroy_and_Repair(cur_sol,Removal_id,Insert_id,NonImp,Dis_List):`

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
## DP方案


``DP[i][j][k][0/1]``: 充电车到 ``i`` 点，还剩 ``j`` 的电量，充 ``k`` 的电量

0: 总消耗 pd * distance + pk * charge (系数 * 距离 + 系数 * 充电量)

1：最晚充电的点( ``k > 0``,``dp[i][j][k][1] = i``、``k == 0`` , 前一个转移来的点的 ``1``)

范围 ： ``[node_num][0-100][0-100]``

## 一些个问题设定
1. 充电时间远小于服务时间

## 一些问题

1. 何时检查一段路径相邻两点距离是否超过了满电量能走的距离，初始化路径的时候没有check这个问题，初始化的时候，如果和时间一起check很有可能找不到解陷入死循环，（e.g : 其他路径已经插不下了，当前剩下的点从仓库直接去不了），或者可以考虑造数据的时候，避免这种事情，保证仓库和任意点可达。
2. 充电时间对时间窗合法性的关系 ，挑选充电的点的同时如何保证在这些点充电可以始终满足时间窗（或者直接假设充电时间小于服务时间，但有点不符合实际）
3. 数据类型，距离为小数，电量为整数，直接四舍五入？




