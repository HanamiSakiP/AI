以下是将 Docker Compose 常用命令整理成的 Markdown 文档：

---

# Docker Compose 常用命令手册

## 目录
- [启动服务](#启动服务)
- [停止服务](#停止服务)
- [查看服务状态](#查看服务状态)
- [查看日志](#查看日志)
- [构建或重新构建服务](#构建或重新构建服务)
- [启动/停止/重启服务](#启动停止重启服务)
- [删除容器](#删除容器)
- [执行命令](#执行命令)
- [配置检查](#配置检查)
- [镜像与网络管理](#镜像与网络管理)
- [其他常用操作](#其他常用操作)

---

## 启动服务

### 启动所有服务
```bash
docker-compose up
```
- **后台运行**：添加 `-d` 参数
  ```bash
  docker-compose up -d
  ```

### 强制重新创建容器
```bash
docker-compose up --force-recreate
```

### 仅重新创建变化的容器
```bash
docker-compose up --no-recreate
```

---

## 停止服务

### 停止并移除资源
```bash
docker-compose down
```
- **删除挂载卷**：添加 `--volumes`
  ```bash
  docker-compose down --volumes
  ```

---

## 查看服务状态

### 查看运行中的服务
```bash
docker-compose ps
```

---

## 查看日志

### 查看所有服务日志
```bash
docker-compose logs
```

### 查看指定服务日志
```bash
docker-compose logs <service_name>
```

### 实时跟踪日志
```bash
docker-compose logs -f <service_name>
```

---

## 构建或重新构建服务

### 构建镜像
```bash
docker-compose build
```

### 忽略缓存构建
```bash
docker-compose build --no-cache
```

---

## 启动/停止/重启服务

### 启动已停止的服务
```bash
docker-compose start
```

### 停止运行中的服务
```bash
docker-compose stop
```

### 重启服务
```bash
docker-compose restart
```

---

## 删除容器

### 删除已停止的容器
```bash
docker-compose rm
```

### 强制删除容器
```bash
docker-compose rm -f
```

---

## 执行命令

### 在容器中执行命令
```bash
docker-compose exec <service_name> <command>
```

#### 示例：进入容器的 Shell
```bash
docker-compose exec <service_name> /bin/bash
```

---

## 配置检查

### 查看服务配置和依赖
```bash
docker-compose config
```

---

## 镜像与网络管理

### 拉取服务镜像
```bash
docker-compose pull
```

### 查看服务镜像列表
```bash
docker-compose images
```

### 查看服务网络
```bash
docker-compose network ls
```

### 查看服务数据卷
```bash
docker-compose volume ls
```

---

## 其他常用操作

### 暂停/恢复服务
```bash
docker-compose pause <service_name>
docker-compose unpause <service_name>
```

### 扩展服务实例数量
```bash
docker-compose scale <service_name>=<num_instances>
```

### 查看端口映射
```bash
docker-compose port <service_name> <port>
```

---

## 附注
1. **文件指定**：若使用非默认的 Compose 文件（如 `docker-compose.prod.yml`），可通过 `-f` 指定：
   ```bash
   docker-compose -f docker-compose.prod.yml up
   ```
2. **版本兼容性**：Docker Compose V2 使用 `docker compose`（无连字符），部分命令可能略有差异。
3. **环境变量**：可通过 `.env` 文件或命令行注入变量。

---

> 更多细节请参考 [Docker Compose 官方文档](https://docs.docker.com/compose/)。