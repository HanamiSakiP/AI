当 Docker 磁盘空间不足时，可以采取以下措施来释放空间：

### 1. 清理未使用的镜像、容器、卷和网络
使用 `docker system prune` 命令清理未使用的资源：

```bash
docker system prune
```

- **清理所有未使用的资源**（包括未使用的镜像、容器、卷和网络）：
  ```bash
  docker system prune -a
  ```

- **仅清理未使用的卷**：
  ```bash
  docker volume prune
  ```

- **仅清理未使用的网络**：
  ```bash
  docker network prune
  ```

### 2. 删除未使用的镜像
使用以下命令删除未使用的镜像：

```bash
docker image prune -a
```

### 3. 删除停止的容器
使用以下命令删除所有停止的容器：

```bash
docker container prune
```

### 4. 清理构建缓存
清理构建缓存以释放空间：

```bash
docker builder prune
```

- **清理所有构建缓存**：
  ```bash
  docker builder prune --all
  ```

### 5. 检查磁盘使用情况
查看 Docker 磁盘使用情况：

```bash
docker system df
```

### 6. 调整 Docker 存储驱动
如果使用 `overlay2` 存储驱动，可以通过调整存储选项优化磁盘使用：

1. 编辑 Docker 配置文件（通常为 `/etc/docker/daemon.json`）。
2. 添加或修改以下内容：
   ```json
   {
     "storage-opts": [
       "overlay2.override_kernel_check=true",
       "overlay2.size=20G"
     ]
   }
   ```
3. 重启 Docker 服务：
   ```bash
   sudo systemctl restart docker
   ```

### 7. 迁移 Docker 数据目录
如果系统盘空间不足，可以将 Docker 数据目录迁移到其他磁盘：

1. 停止 Docker 服务：
   ```bash
   sudo systemctl stop docker
   ```

2. 复制 Docker 数据目录到新位置：
   ```bash
   sudo rsync -aP /var/lib/docker /new/location/
   ```

3. 修改 Docker 配置文件（`/etc/docker/daemon.json`）：
   ```json
   {
     "data-root": "/new/location/docker"
   }
   ```

4. 重启 Docker 服务：
   ```bash
   sudo systemctl start docker
   ```

### 8. 删除大文件或日志
检查容器日志和大文件，必要时删除：

1. 查看容器日志大小：
   ```bash
   docker logs <container_id>
   ```

2. 清理日志：
   ```bash
   truncate -s 0 /var/lib/docker/containers/<container_id>/<container_id>-json.log
   ```

### 9. 限制日志大小
通过配置日志驱动和大小限制日志文件：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 10. 定期清理
设置定时任务定期清理 Docker 资源：

```bash
0 3 * * * /usr/bin/docker system prune -f
```

通过这些方法，可以有效释放 Docker 占用的磁盘空间。