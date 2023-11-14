from test import evaluate
try:
    k = 0
    while True:
        # a = input()
        a = 14
        res = evaluate(a,k)
        k += 1
        print(res)
        pass
except SystemExit:
    print("Program Stopped!")