from test import evaluate
try:
    k = 0
    while True:
        a = input()
        res = evaluate(a,k)
        k += 1
        pass
except SystemExit:
    print("Program Stopped!")