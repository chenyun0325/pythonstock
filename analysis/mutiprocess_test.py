import multiprocessing
import time

def func(msg1 =None,msg2=None):
    for i in range(10):
        print '%s----%s----%s'%(i,msg1,msg2)
        time.sleep(1)

def main():
    pool = multiprocessing.Pool(processes=4)
    cpu_count =multiprocessing.cpu_count()
    print cpu_count
    for i in range(11,20):
        res=pool.apply_async(func,(i,i,))
    pool.close()
    pool.join()
    if res.successful():
        print 'suc'


if __name__ == '__main__':
    main()