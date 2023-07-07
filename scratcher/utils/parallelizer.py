from concurrent.futures import ThreadPoolExecutor

def parallel_runner(callback, worker_num, props=None): 
    with ThreadPoolExecutor(max_workers=worker_num) as executor:
      for i in range(worker_num):  
        if(props):       
          executor.submit(callback, *props[i])
        else:
          executor.submit(callback)