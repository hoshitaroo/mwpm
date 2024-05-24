from itertools import combinations
import numpy as np
import networkx as nx
import time
from typing import List, Tuple
from tqdm import trange

from param import param
from toric_code import ToricCode

def decode(coord, param_):
    g = nx.Graph()
    for u, v in combinations(coord, 2):
        x_dist = min(np.abs(u[0]-v[0]), param_.code_distance - np.abs(u[0]-v[0]))
        y_dist = min(np.abs(u[1]-v[1]), param_.code_distance - np.abs(u[1]-v[1]))
        weight = -(x_dist*100 + y_dist*(1+100))
        g.add_edge(tuple(u),tuple(v),weight=weight)
    matching = nx.algorithms.max_weight_matching(g, maxcardinality=True)
    return matching
'''
↑マッチングの計算を行う
'''

'''
↓シミュレーションとその評価
'''
def evaluate(n_iter, param_):
    count = 0
    toric_code = ToricCode(param=param_)

    spent = 0
    count_no_error = 0
    #for _ in trange(n_iter):
    for _ in range(n_iter):
        #print('\n') #for debug
        errors = toric_code.generate_errors()
        is_no_error = np.all(errors == 0)
        if is_no_error:
            count_no_error += 1
            continue
        #print('errors') #for debug
        #print(errors) #for debug
        syndrome_x = toric_code.generate_syndrome_X(errors)
        #print('syndrome_x') #for debug
        #print(syndrome_x) #for debug
        syndrome_z = toric_code.generate_syndrome_Z(errors)
        #print('syndrome_z') #for debug
        #print(syndrome_z) #for debug
        coord_x = list(zip(*np.where(syndrome_x==1)))
        #print('coord_x') #for debug
        #print(coord_x) #for debug
        coord_z = list(zip(*np.where(syndrome_z==1)))
        #print('coord_z') #for debug
        #print(coord_z) #for debug
        before = time.perf_counter()
        matching_x = decode(coord_x, param_)
        #print ('matching_x') # for debug
        #print(matching_x) # for debug 
        matching_z = decode(coord_z, param_)
        #print ('matching_z') # for debug
        #print(matching_z) # for debug 
        spent += time.perf_counter() - before
        for u,v in matching_z:
            errors = toric_code.decode_x_error(errors,u,v)
        for u,v in matching_x:
            errors = toric_code.decode_z_error(errors,u,v)
        #print('corrected errors') # for debug
        #print(errors) # for debug
        if np.all(toric_code.generate_syndrome_X(errors)==0) and np.all(toric_code.generate_syndrome_Z(errors)==0): 
            if toric_code.not_has_non_trivial_x(errors) and toric_code.not_has_non_trivial_z(errors):
                count = count + 1
    #print(str(spent / (n_iter-count_no_error)) + str(" seconds"))
    time_average = spent / (n_iter-count_no_error)
    logical_error_rate = (n_iter - count - count_no_error) / (n_iter - count_no_error)
    #print(f"logical error rates: {n_iter - count - count_no_error}/{n_iter-count_no_error}", (n_iter - count - count_no_error) / (n_iter - count_no_error))
    return logical_error_rate, time_average

#実行
param_ = param(size=5, p=0.05)
#print("Toric code simulation // code distance is " + str(param_.code_distance))
logical_error_rate, time_average = evaluate(10000, param_)