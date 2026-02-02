## MariaDB同理

> ### 1. 安装mysql、redis
> ```bash
> apt update
> apt install -y mariadb-server redis-server
> redis-server /etc/redis/redis.conf --daemonize no
> redis-cli ping
> service start mariadb
> mysql -u root -p
> ```
> ### 2. 配置mysql
> ```bash
> sudo mysql_secure_installation
> ```
> ### 3. 配置过程中
> ```bash
> 回车
> n
> y
> 新密码
> 确认新密码
> n
> y
> y
> Reload privilege tables now? [Y/n] y
> ```
