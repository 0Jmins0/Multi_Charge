from readData import readmain
from test import evaluate
try:
    k = 0

    while True:
        a = input()
        # a = 10
        res = evaluate(a,k)
        k += 1
        print(res)
        pass
except SystemExit:
    print("Program stoppediji")