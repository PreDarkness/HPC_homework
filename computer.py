# 计算节点
from multiprocessing.connection import Client,Listener
from configparser import ConfigParser as cp
import sys,os


#读取序列号
node = sys.argv[1]
node = int(node)

#读取配置文件，用于建立第一个socket
conf = cp()
conf.read('conf_computer.ini')
# print(conf.sections())
port = conf.getint('server','port')
host = conf.get('server','host')
addr = (host,port+node)


# 读取配置文件，用于开启第二个socket，用于等待其他节点的结果，并规约
conf2 = cp()
conf2.read('conf_computer.ini')
# print(conf2.sections())
port2 = conf2.getint('compute', 'port')
host2 = conf2.get('compute', 'host')
addr2 = (host2, port2)

#建立与控制节点的连接
cpter = Client(addr)
total_node = cpter.recv()
role = cpter.recv()
# print('角色分配:'+role)
cpter.send(role)

def rec_data():
    #接收文件
    data = cpter.recv()
    with open('data' + role + '.csv', 'wb') as f:
        f.write(data)
    # print("--------------数据文件" + role + "已收到-----------")
    task = cpter.recv()
    with open('task.py', 'wb') as f:
        f.write(task)
    # print("--------------计算任务文件已收到--------------")

def compute():
    #计算
    res = os.popen('python task.py '+role+' '+str(total_node))
    res = res.read()
    return res
    # print(res)

def main():

    rec_data()

    res = compute()

    if role == '0':
        res_list = [int(res)]
        cpter0 = Listener(addr2)
        print("------节点0等待其他节点的结果-------")
        for i in range(int(total_node)-1):
            c0 = cpter0.accept()
            t = c0.recv()
            t = int(t)
            res_list.append(t)
        # print(res_list)
        #发送给控制节点
        cpter = Client(addr)
        print("------结果规约成功，发送至控制节点-----")
        cpter.send(max(res_list))

    else:
        cpter_other = Client(addr2)
        cpter_other.send(res)
        print("--------计算结束，发送给0-------")


if __name__ == '__main__':
    main()



