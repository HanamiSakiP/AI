## MariaDB同理

> ### 1. 安装mysql、redis
> ```bash
> apt update
> apt install -y mariadb-server redis-server
> redis-server /etc/redis/redis.conf --daemonize no
> redis-cli ping
> service mariadb start
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

## mysql 命令
```bash
# 1. 查询数据库
show databases;
# 创建数据库
create database op;
# 2. 使用数据库
use op;

# 创建表
create table op(name varchar(6));
# 查询表结构
desc op;
# 删除表
drop table op;

# 3. 查询数据库 表
show tables;
# 删除数据库
drop database op;
```

## redis 命令
```bash
# 测试
redis-cli ping
redis-cli get keys
```
