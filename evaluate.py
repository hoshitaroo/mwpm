'''
MWPMの精度、計算時間について実行結果を図にするためのプログラム
'''
from toric_code import ToricCode
from param import param
from decoder_by_MWPM import evaluate #復号手法によって変更可能

import numpy as np
import matplotlib.pyplot as plt

size_list = [5,7,9]

def make_list(size, n_iter=10000, p_interval=0.005):
    logical_error_rate_list = []
    time_average_list = []
    p_list = [round(x, 3) for x in list(np.arange(0.01, 0.20 + 0.005, 0.005))]
    for p in p_list:
        param_ = param(size=size, p=p)
        print('size='+str(param_.code_distance)+'   p='+str(p))
        logical_error_rate, time_average = evaluate(n_iter=n_iter, param_=param_)
        logical_error_rate_list.append(logical_error_rate)
        time_average_list.append(time_average)
        p += p_interval
    return logical_error_rate_list, time_average_list

l_lists = []
t_lists = []
for size in size_list:
    logical_error_list, time_average_list = make_list(size=size)
    l_lists.append(logical_error_list)
    t_lists.append(time_average_list)

plt.figure()
plt.title('error_rate and logical_error_rate')
plt.xlabel('Pauli error rate')
plt.ylabel('logical error rate')
size = 5
i = 0
while size <= 9:
    x = [round(x, 3) for x in list(np.arange(0.01, 0.20 + 0.005, 0.005))]
    y = l_lists[i]
    plt.plot(x, y, label='size='+str(size))
    i += 1
    size += 2
plt.legend()
plt.savefig('p_to_logical.png')

plt.figure()
plt.title('code7 error_rate and time')
plt.xlabel('Pauli error rate')
plt.ylabel('time')
size = 7
x = [round(x, 3) for x in list(np.arange(0.01, 0.20 + 0.005, 0.005))]
y = t_lists[1]
plt.plot(x, y, label='size=7')
plt.legend()
plt.savefig('p_to_time_code7.png')

plt.figure()
plt.title('p=0.05 time and code_distance')
plt.xlabel('code distance')
plt.ylabel('time')
x = size_list
y = []
i=0
while i < len(size_list):
    time_list = t_lists[i]
    y.append(time_list[8])      #p=0.05
    i += 1
plt.plot(x, y, label='p=0.05')
plt.legend()
plt.savefig('time_to_size.png')
print('complete')