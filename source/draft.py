a = [0,1,2,3,4,5]
b = a[:3]
c = a[3:]

d = b + c
print("b",b)
print("c",c)

print("d",d)

Pre_Node = [[[[] for _ in range(3)] for _ in range(3)] for _ in range(2)]

Pre_Node[1][1][0] .append(0)
print(Pre_Node)