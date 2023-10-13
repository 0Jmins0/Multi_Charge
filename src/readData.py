import csv
def readmain(p):
    x = [] # 经度
    y = [] # 纬度
    tl = [] # 时间窗最早
    tr = [] # 时间窗最晚
    q = [] # 载货量
    s = [] # 服务时间
    n = 0
    # 打开CSV文件
    ipad = '/private/var/mobile/Containers/Data/Application/BD13E5CF-FC75-4FE8-910E-9E061253A0E7/Documents/Multi_Charge.git/data/data'+ str(p) + '.csv'
    other = '../data/data' + str(p) + '.csv'
    with open(other, newline='') as csvfile:
        # 创建CSV读取器对象
        csv_reader = csv.reader(csvfile)

        # 遍历每一行数据
        for row in csv_reader:
            if(len(row) == 1):
                n = int(row[0])
                continue
            # row是一个列表，包含CSV文件中的一行数据
            # 你可以通过索引访问每个字段，例如row[0], row[1]等
            x.append(int(row[1]))
            y.append(int(row[2]))
            tl.append(int(row[3]))
            tr.append(int(row[4]))
            q.append(int(row[5]))
            s.append(int(row[6]))
    return n,x,y,tl,tr,q,s
# n ,x,y,tl,tr,q = readmain(10)
# print(n)