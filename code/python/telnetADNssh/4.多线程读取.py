import threading
from queue import Queue
import telnetlib
import time
print (f"程序于{time.strftime('%X')}开始执行")

f=open("ip.txt","r")
def telnet_session(ip,outputq):
	host =ip.strip()
	user = "admin"
	password = "123456"
	print(host)
	tn=telnetlib.Telnet(host)
	tn.read_until(b"Username:")
	tn.write(user.encode('ascii') + b"\n")
	tn.read_until(b"Password:")
	tn.write(password.encode('ascii') + b"\n")
	tn.write(b"screen-length 0 temporary\n")
	f1=open("cmd.txt","r")                               #使用读的方式打开cmd1.txt文件            
	for line1 in f1.readlines() :	                      #把命令一行一行读给line1
		tn.write(line1.encode('ascii') + b"\n")           #执行line1(每一行的命令)
	time.sleep(3)
	output = tn.read_very_eager().decode('ascii')
	print(output)
	tn.close()
threads=[]
for ip in f.readlines():
      t=threading.Thread(target=telnet_session,args=(ip,Queue()))
      t.start()
      threads.append(t)
for i in threads:
      i.join()
print (f"程序于{time.strftime('%X')}结束执行")
