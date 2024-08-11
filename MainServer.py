import os
import sys
import time

from server import Server as mainServer
from timeserver import Server as timeServer

import threading

try:
    mthread = threading.Thread(target=mainServer)
    tthread = threading.Thread(target=timeServer)

    mthread.daemon = True
    tthread.daemon = True

    mthread.start()
    tthread.start()
except Exception as e:
    print(e)
    print("服务器未能启动")
    sys.exit(str(e))

print("服务器已启动 输入 help 以查看帮助")

time.sleep(0.5)
while True:
    c = input(">")
    c = c.lower()
    if c == "h" or c == "help":
        print("""帮助:
h&help - 命令解释
s&status - 查看服务器状态
exit&shutdown - 关闭服务器""")
    if c == "s" or c == "status":
        print("正在制作中")
        pass
        #os.system('start "ping http://127.0.0.1:11451&pause"')
    if c == "exit" or c == "shutdown":
        sys.exit(0)