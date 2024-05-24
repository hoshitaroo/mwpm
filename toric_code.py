'''
Toric code シミュレーション用
param.py で符号距離とエラーレートを設定
'''
import numpy as np
from enum import IntEnum, auto, unique
import random

class Pauli(IntEnum):
    I = auto()
    X = auto()
    Y = auto()
    Z = auto()

    def __mul__(self, b):
        if self == b:
            return Pauli.I
        if self is Pauli.I:
            return b
        if b is Pauli.I:
            return self
        return ({Pauli.X, Pauli.Y, Pauli.Z} - {self, b}).pop()


class ToricCode:

    #Toric codeの初期化
    def __init__(self,param) -> None:
        self.size = param.code_distance
        self.errors_rate = param.errors_rate

    #エラーの発生
    def generate_errors(self) -> np.array:
        errors_list = random.choices([0, 1, 2, 3], # I, X, Y, Z
                                     [1-self.errors_rate[0]-self.errors_rate[1]-self.errors_rate[2],self.errors_rate[0],self.errors_rate[1],self.errors_rate[2]],
                                     k = 2*self.size*self.size)
        errors = np.array(errors_list)
        errors = errors.reshape(2*self.size, self.size)
        return errors
    
    # X作用素によるパリティチェックとシンドローム生成(点上スタビライザー)
    def generate_syndrome_X(self,errors) -> np.array:

        syndrome = np.zeros((self.size, self.size), dtype=int)
        i = 0
        j = 0
        
        while 1:
            while 1:
                count = 0
                #左のqubitのcheck
                if j==0:
                    if errors[2*i][self.size-1] == 3 or errors[2*i][self.size-1] == 2:
                        count = count+1
                else:
                    if errors[2*i][j-1] == 3 or errors[2*i][j-1] == 2:
                        count = count+1
                #上のqubitのcheck
                if i==0:
                    if errors[2*self.size-1][j] == 3 or errors[2*self.size-1][j] == 2:
                        count = count+1
                else:
                    if errors[2*i-1][j] == 3 or errors[2*i-1][j] == 2:
                        count = count+1
                #右のqubitのcheck
                if errors[2*i][j] == 3 or errors[2*i][j] == 2:
                    count = count+1
                #下のqubitのcheck
                if errors[2*i+1][j] == 3 or errors[2*i+1][j] == 2:
                    count =count+1
                #パリティチェック
                if count%2 == 0:
                    syndrome[i][j] = 0
                else:
                    syndrome[i][j] = 1
                
                # j 終了判定
                if j==self.size-1:
                    j = 0
                    break
                else:
                    j = j+1
            # i 終了判定
            if i==self.size-1:
                break
            else:
                i = i+1
        
        return syndrome
    
    # Z作用素によるパリティチェックとシンドローム生成(面上スタビライザー)
    def generate_syndrome_Z(self,errors) -> np.array:

        syndrome = np.zeros((self.size, self.size), dtype =int)
        i = 0
        j = 0
        
        while 1:
            while 1:
                count = 0
                #右のqubitのcheck
                if j==self.size-1:
                    if errors[2*i+1][0] == 1 or errors[2*i+1][0] == 2:
                        count = count+1
                else:
                    if errors[2*i+1][j+1] == 1 or errors[2*i+1][j+1] == 2:
                        count = count+1
                #下のqubitのcheck
                if i==self.size-1:
                    if errors[0][j] == 1 or errors[0][j] == 2:
                        count = count+1
                else:
                    if errors[2*i+2][j] == 1 or errors[2*i+2][j] == 2:
                        count = count+1
                #左のqubitのcheck
                if errors[2*i+1][j] == 1 or errors[2*i+1][j] == 2:
                    count = count+1
                #上のqubitのcheck
                if errors[2*i][j] == 1 or errors[2*i][j] == 2:
                    count =count+1
                #パリティチェック
                if count%2 == 0:
                    syndrome[i][j] = 0
                else:
                    syndrome[i][j] = 1
                
                # j 終了判定
                if j==self.size-1:
                    j = 0
                    break
                else:
                    j = j+1
            # i 終了判定
            if i==self.size-1:
                break
            else:
                i = i+1
        
        return syndrome
    
    def not_has_non_trivial_x(self,errors) -> bool:
        '''
        shape of errors is (2*size,size)
        '''
        errors_tmp = np.zeros((2,self.size,self.size), dtype = int)
        
        i=0
        j=0
        m=0
        n=0
        #横
        while i < 2*self.size:
            while j < self.size:
                errors_tmp[0,m,n] = errors[i,j]
                j = j+1
                n = n+1
            n = 0
            j = 0
            i = i+2
            m = m+1
        
        i=1
        j=0
        m=0
        n=0
        #縦
        while i < 2*self.size:
            while j < self.size:
                errors_tmp[1,m,n] = errors[i,j]
                j = j+1
                n = n+1
            n = 0
            j = 0
            i = i+2
            m = m+1
        
        count = [0,0]
        for i in range(self.size):
            for j in range(self.size):
                if errors_tmp[0,i,j]==1 or errors_tmp[0,i,j]==2:
                    count[0] = count[0]+1
        
        for i in range(self.size):
            for j in range(self.size):
                if errors_tmp[1,i,j]==1 or errors_tmp[1,i,j]==2:
                    count[1] = count[1]+1
        return (count[0]%2==0 and count[1]%2==0)

    def not_has_non_trivial_z(self,errors) -> bool:
        '''
        shape of errors is (2*size,size)
        '''
        errors_tmp = np.zeros((2,self.size,self.size), dtype = int)
        
        i=0
        j=0
        m=0
        n=0
        #横
        while i < 2*self.size:
            while j < self.size:
                errors_tmp[0,m,n] = errors[i,j]
                j = j+1
                n = n+1
            n = 0
            j = 0
            i = i+2
            m = m+1
        
        i=1
        j=0
        m=0
        n=0
        #縦
        while i < 2*self.size:
            while j < self.size:
                errors_tmp[1,m,n] = errors[i,j]
                j = j+1
                n = n+1
            n = 0
            j = 0
            i = i+2
            m = m+1
        count = [0,0]
        for i in range(self.size):
            for j in range(self.size):
                if errors_tmp[0,i,j]==3 or errors_tmp[0,i,j]==2:
                    count[0] = count[0]+1
        
        for i in range(self.size):
            for j in range(self.size):
                if errors_tmp[1,i,j]==3 or errors_tmp[1,i,j]==2:
                    count[1] = count[1]+1
        return (count[0]%2==0 and count[1]%2==0)

    def decode_x_error(self,errors,u,v):
        
        u = list(u)
        v = list(v)
        #u,v in matching_z

        #行成分から訂正を行う
        while u[1] != v[1]:  # small [u / v] large
            if u[1] > v[1]:
                u, v = v, u #uの方が左にあることが確定
            x = u[0]*2 + 1
            if v[1] - u[1] > self.size // 2: #境界を跨ぐパターン
                y = u[1]%self.size #左のqubit
                if errors[x, y]%2==0:
                    errors[x, y] += 1
                else:
                    errors[x, y] -= 1
                u[1] -= 1
                u[1] %= self.size
            else: #境界を跨がないパターン
                y = (u[1] + 1) % self.size
                if errors[x, y]%2==0:
                    errors[x, y] += 1
                else:
                    errors[x, y] -= 1
                u[1] += 1
                u[1] %= self.size

        #次に列成分の訂正を行う
        while u[0] != v[0]:  # small [u   v] large
            if u[0] > v[0]:
                u, v = v, u #uの方が上にあることが確定
            y = u[1]
            if v[0] - u[0] > self.size // 2:  #境界を跨ぐパターン
                x = 2*u[0]
                if errors[x, y]%2==0:
                    errors[x, y] += 1
                else:
                    errors[x, y] -= 1
                u[0] -= 1
                u[0] %= self.size
            else: # 境界を跨がないパターン
                x = (2*u[0]+2) % (2*self.size)
                
                if errors[x, y]%2==0:
                    errors[x, y] += 1
                else:
                    errors[x, y] -= 1
                
                u[0] += 1
                u[0] %= self.size
        return errors
    
    def decode_z_error(self,errors,u,v):
        
        u = list(u)
        v = list(v)
        #u,v in matching_x

        #行成分の訂正
        while u[1] != v[1]:  # small [u / v] large
            if u[1] > v[1]:
                u, v = v, u #uが左にあることが確定
            x = 2*u[0]
            if v[1] - u[1] > self.size // 2: #境界を跨ぐパターン
                y = (u[1] - 1) % self.size
                errors[x, y] = 3 - errors[x, y]
                u[1] -= 1
                u[1] %= self.size
            else: #境界を跨がないパターン
                y = u[1] % self.size
                errors[x, y] = 3 - errors[x, y]
                u[1] += 1
                u[1] %= self.size

        #列成分の訂正
        while u[0] != v[0]:  # small [u   v] large
            if u[0] > v[0]:
                u, v = v, u #uが上にあることが確定
            y = u[1]
            if v[0] - u[0] > self.size // 2: #境界を跨ぐパターン
                x = (2*u[0] - 1) % (self.size*2)
                errors[x, y] = 3 - errors[x, y]
                u[0] -= 1
                u[0] %= self.size
            else: #境界を跨がないパターン
                x = (2*u[0] + 1) % (self.size*2)
                errors[x, y] = 3 - errors[x, y]
                u[0] += 1
                u[0] %= self.size
        return errors

#test
'''
toric_code = ToricCode()
errors = toric_code.generate_errors()
print("errors")
print(errors)
syndrome_x = toric_code.generate_syndrome_X(errors)
print("syndrome_x")
print(syndrome_x)
syndrome_z = toric_code.generate_syndrome_Z(errors)
print("syndrome_z")
print(syndrome_z)
'''

'''
print(Pauli.I)
print(Pauli.X)
print(Pauli.Y)
print(Pauli.Z)
'''