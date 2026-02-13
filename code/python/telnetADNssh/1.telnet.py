import telnetlib
#引入time模块
import time
#定义变量host（主机ip）、user（telnet用户）、password（telnet密码）
host="192.168.19.10"
user="admin"
password="123456"


print("正在连接",host)      #telnet成功后提示登录成功

tn=telnetlib.Telnet(host)     #连接到主机
tn.read_until(b"Username:")   #当出现“Username：”时，停止下来
tn.write(user.encode('ascii') + b"\n")   #把用户名转化为ascii字符型
tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
tn.write(b"screen-length 0 temporary\n")    #在vty(telnet)远程连接下,所有命令完整显示
#配置环回口地址
tn.write(b"sys\n")
tn.write(b"interface LoopBack 0\n")
tn.write(b"ip address 11.11.11.11 255.255.255.255\n")
#保存并推出
tn.write(b"return\n")
tn.write(b"save\n")
tn.write(b"Y\n")

time.sleep(3)       #等待3秒


output = tn.read_very_eager().decode('ascii')
print(output)
tn.close()         #关闭连接
