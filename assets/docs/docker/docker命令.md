以下是将 Docker 常用命令整理成的 Markdown 文档：

---

# Docker 常用命令手册

## 目录
- [容器生命周期管理](#容器生命周期管理)
- [镜像管理](#镜像管理)
- [查看容器信息](#查看容器信息)
- [日志与监控](#日志与监控)
- [网络管理](#网络管理)
- [数据卷管理](#数据卷管理)
- [系统清理](#系统清理)
- [其他实用命令](#其他实用命令)

---

## 容器生命周期管理

### 运行容器
```bash
docker run [OPTIONS] IMAGE [COMMAND]
```
- **常用选项**：
  - `-d`: 后台运行容器（守护模式）
  - `-p <主机端口>:<容器端口>`: 端口映射
  - `-v <主机目录>:<容器目录>`: 挂载数据卷
  - `--name <容器名>`: 指定容器名称
  - `-e <环境变量>`: 设置环境变量
  - `--rm`: 容器退出后自动删除

#### 示例
```bash
docker run -d -p 8080:80 --name my_nginx nginx
```

### 启动/停止/重启容器
```bash
docker start <容器ID或名称>
docker stop <容器ID或名称>
docker restart <容器ID或名称>
```

### 删除容器
```bash
docker rm <容器ID或名称>
```
- **强制删除运行中的容器**：
  ```bash
  docker rm -f <容器ID或名称>
  ```

### 进入运行中的容器
```bash
docker exec -it <容器ID或名称> /bin/bash
```
- `-i`: 保持交互模式
- `-t`: 分配伪终端

---

## 镜像管理

### 构建镜像
```bash
docker build -t <镜像名:标签> <Dockerfile路径>
```
#### 示例
```bash
docker build -t myapp:v1 .
```

### 拉取/推送镜像
```bash
docker pull <镜像名:标签>
docker push <镜像名:标签>
```

### 列出镜像
```bash
docker images
```

### 删除镜像(可批量)
```bash
docker rmi <镜像ID或名称>
```
- **强制删除**（若镜像被容器使用）：
  ```bash
  docker rmi -f <镜像ID或名称>
  ```

---

## 查看容器信息

### 查看运行中的容器
```bash
docker ps
```

### 查看所有容器（包括已停止的）
```bash
docker ps -a
```

### 查看容器详情
```bash
docker inspect <容器ID或名称>
```

### 查看容器资源占用
```bash
docker stats
```

---

## 日志与监控

### 查看容器日志
```bash
docker logs <容器ID或名称>
```
- **实时跟踪日志**：
  ```bash
  docker logs -f <容器ID或名称>
  ```

### 查看容器进程
```bash
docker top <容器ID或名称>
```

---

## 网络管理

### 列出所有网络
```bash
docker network ls
```

### 创建自定义网络
```bash
docker network create <网络名>
```

### 连接容器到网络
```bash
docker network connect <网络名> <容器ID或名称>
```

### 查看网络详情
```bash
docker network inspect <网络名>
```

---

## 数据卷管理

### 列出数据卷
```bash
docker volume ls
```

### 删除未使用的数据卷
```bash
docker volume prune
```

---

## 系统清理

### 清理无用资源
```bash
docker system prune
```
- **包含镜像和卷**：
  ```bash
  docker system prune -a --volumes
  ```

### 删除所有停止的容器
```bash
docker container prune
```

---

## 其他实用命令

### 查看 Docker 版本
```bash
docker --version
```

### 查看 Docker 信息
```bash
docker info
```

### 复制文件到容器
```bash
docker cp <本地文件路径> <容器ID或名称>:<容器路径>
```

### 从容器复制文件到主机
```bash
docker cp <容器ID或名称>:<容器路径> <本地文件路径>
```
### 保存本地镜像为指定文件
```bash
docker save -o <指定文件名称.tar> <镜像名称>
```
### 加载本地镜像
```bash
docker load -i <载入文件名称.tar>
```

---

## 附注
1. **数据持久化**：建议使用 `-v` 挂载数据卷避免数据丢失。
2. **权限问题**：在 Linux 系统中，若需避免 `sudo`，可将用户加入 `docker` 组。
3. **容器与镜像关系**：镜像是静态模板，容器是镜像的运行实例。
4. **版本兼容性**：Docker CLI 与守护程序版本需匹配，建议使用稳定版。

---

> 更多细节请参考 [Docker 官方文档](https://docs.docker.com/)。