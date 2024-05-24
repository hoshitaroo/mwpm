import numpy as np

a = [round(x, 3) for x in list(np.arange(0.01, 0.20 + 0.005, 0.005))]

print(a)
i=0
while True:
    if a[i] == 0.05:
        print(i)
        break
