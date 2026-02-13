import telnetlib
import time

user="admin"
password="123456"
f=open("ip.txt","r")
for line in f.readlines() :
	host =line.strip()
	print(host)
	tn=telnetlib.Telnet(host)
	tn.read_until(b"Username:")
	tn.write(user.encode('ascii') + b"\n")
	tn.read_until(b"Password:")
	tn.write(password.encode('ascii') + b"\n")
	tn.write(b"screen-length 0 temporary\n")
	f1=open("cmd1.txt","r")                               #使用读的方式打开cmd1.txt文件            
	for line1 in f1.readlines() :	                      #把命令一行一行读给line1
		tn.write(line1.encode('ascii') + b"\n")           #执行line1(每一行的命令)
	time.sleep(3)
	output = tn.read_very_eager().decode('ascii')
	print(output)
	tn.close()
