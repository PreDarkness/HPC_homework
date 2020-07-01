# 控制节点

#控制节点发送任务程序和切片后的数据给各自处理的节点
#节点0返回规约后的结果
from multiprocessing.connection import Listener

from multiprocessing import Pool
import time,os,sys
from configparser import ConfigParser as cp



#读取配置文件
conf = cp()
conf.read('conf_controller.ini')
conf.sections()



#获取配置文件
port = conf.getint('server', 'port')
host = conf.get('server', 'host')



def control(i,n):
    addr = (host, port+i)
    # 开启监听器
    ctler = Listener(addr)
    print("-----等待一个新客户端到来-----：",addr)
    ctl = ctler.accept()
    ctl.send(n)
    ctl.send(str(i))
    print("节点 "+ctl.recv()+" 确认接入，时间："+time.ctime())


    #发送文件
    with open('data.csv', 'r') as f:
        data = f.read()
        data = data.split(',')
        l = len(data)
        s = int(l / n * i)
        e = int(l / n * (i + 1))
        data = bytes(','.join(data[s:e]), encoding='utf-8')
        ctl.send(data)
    with open('task.py','rb') as f:
        data = f.read()
        ctl.send(data)

def main():
    start_time = time.time()
    # 开启进程池
    po = Pool(10)
    # 同时监听多个节点
    # print("输入所需节点数（0-4）:")

    n = sys.argv[1]
    n = int(n)

    for i in range(0, n):
        temp = po.apply_async(control, (i, n))
        print("开始监听", i)
    # 关闭进程池，join必须放在close后面，等待全部子进程结束
    po.close()
    po.join()

    addr = (host, port)
    # 开启监听器
    ctler = Listener(addr)
    ctl = ctler.accept()
    res = ctl.recv()
    print(res)
    # 计算运行时间
    end_time = time.time()
    time1 = end_time - start_time
    print("分布式计算时间:", time1)
    # 直接计算
    start_time = time.time()
    res = os.popen('python task.py -1 1')
    res = res.read()
    end_time = time.time()
    time2 = end_time - start_time
    print("直接计算时间:", time2)
    print('加速比：',time1 / time2)
    print("----任务完成----")

if __name__ == '__main__':
    main()