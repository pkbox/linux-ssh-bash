# coding: utf-8


import os
import sys
import traceback
import pexpect

try:
    import pexpect
except ImportError:
    print("""
    You must install pexpect module
    """)
    os.system("pip3 install pexpect")
    sys.exit(1)

SHOW_SERVER = {
    "mac": ["10.66.29.56"],
    "bae": ["180.76.152.250"],
    "rootcloud": ["hadoop-master-dev-10.70.19.222"]
}
SERVER = {
    "10.66.29.56": ["22", "steven", "10.66.29.56", "1"],
    "180.76.152.250": ["22", "root", "180.76.152.250", "1234asdf!"],
    "hadoop-master-dev-10.70.19.222": ["22", "root", "10.70.19.222", "Cdh@20161123"],
}


def auto_connect(host):
    SSH = "ssh -p %s %s@%s " % (host[0], host[1], host[2])
    try:
        child = pexpect.spawn(SSH)
        index = child.expect(['password:', 'continue connecting (yes/no)?', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline(host[3])
            child.interact()
        elif index == 1:
            child.sendline('yes')
            child.expect(['password:'])
            child.sendline(host[3])
            child.interact()
        elif index == 2:
            print("子程序异常，退出!")
            child.close()
        elif index == 3:
            print("连接超时")
    except:
        traceback.print_exc()


show = "\n其从如下的连接中选择一个：\n"
i = 1
tmp = [""] * 1000

for sel in SHOW_SERVER:
    show = show + sel + "\n"
    for server in SHOW_SERVER[sel]:
        if server != "" and server != None:
            show = show + "  |--" + "[" + str(i) + "] " + server + "\n"
            tmp[i - 1] = server
            i += 1
print(show)
select = int(input("请输入连接编号："))
try:
    host = SERVER[tmp[select - 1]]
except:
    print("""
    argv error, use it link
    jssh v3, v3 must defined in addr_map
    """)
    sys.exit(1)
auto_connect(host)
