import telnetlib
import time

user="admin"
password="123456"
f=open("ip.txt","r")                                  #使用读的方法打开ip.txt文件
for line in f.readlines() :                           #一行一行读取ip.txt文件，并把内容给line变量
	host =line.strip()                                #去掉每行的头部和尾部空格等内容，并给host变量
	print(host)                                       #打印host的值（ip地址）
	tn=telnetlib.Telnet(host)                         #连接host
	tn.read_until(b"Username:")
	tn.write(user.encode('ascii') + b"\n")
	tn.read_until(b"Password:")
	tn.write(password.encode('ascii') + b"\n")
	tn.write(b"screen-length 0 temporary\n")
	tn.write(b"sys\n")
	tn.write(b"interface LoopBack 0\n")
	tn.write(b"ip address 11.11.11.11 255.255.255.255\n")
	tn.write(b"return\n")
	tn.write(b"save\n")
	tn.write(b"Y\n")
	time.sleep(3)
	output = tn.read_very_eager().decode('ascii')
	print(output)
	tn.close()
