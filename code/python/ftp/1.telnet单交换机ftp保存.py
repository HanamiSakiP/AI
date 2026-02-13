import telnetlib
#引入time模块
import time
#定义变量host（主机ip）、user（telnet用户）、password（telnet密码）
user="admin"
password="123456"
ftpuser="admin"
ftppassword="123456"
host="192.168.19.10"
print("已成功登录",host) 
tn=telnetlib.Telnet(host)    
tn.read_until(b"Username:")   
tn.write(user.encode('ascii') + b"\n")  
tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
tn.write(b"screen-length 0 temporary\n") 
f1=open("cmd.txt","r")
for line1 in f1.readlines() :	
	tn.write(line1.encode('ascii') + b"\n")
tn.write(b"return\n")
tn.write(b"save\n")
tn.write(b"Y\n")
tn.write(b"\n")
time.sleep(1)  
tn.write(b"ftp 192.168.19.1\n")
tn.write(ftpuser.encode('ascii') + b"\n")  
tn.write(ftppassword.encode('ascii') + b"\n")
tn.write(b"put vrpcfg.zip\n")
time.sleep(2)   
tn.write(b"quit\n")
tn.close()         
