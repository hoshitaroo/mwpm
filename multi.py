from multiprocessing import Pool
import time 

def parallel_function(argument):
    # ここに並列で実行する処理を書く
    time.sleep(argument)
    print(argument)
    return(10*argument)

if __name__ == '__main__':
    pool = Pool(processes=3) # 同時に実行する処理の個数（コア数）を指定
    arguments = [10,15,5,1]  # 処理するデータや引数のリスト
    results = pool.map(parallel_function, arguments)
    print(results)
    pool.close()
    pool.join()
