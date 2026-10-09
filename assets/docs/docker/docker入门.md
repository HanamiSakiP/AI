> 自动安装
> 
> #### 卸载旧版本
> ```bash
> for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
> ```
> 
> #### 使用官方安装脚本
> ```bash> 
>  curl -fsSL https://get.docker.com -o get-docker.sh> 
>  sudo sh get-docker.sh
> ```
> 
> 手动安装
> #### 1. 更新软件包
> ```bash
> sudo apt update
> sudo apt upgrade
> ```
> 
> #### 2. 手动安装
> ```bash
> # 2. 安装依赖包
> sudo apt install apt-transport-https ca-certificates curl software-properties-common
> 
> # 3. 添加 Docker 官方 GPG 密钥
> sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
> sudo chmod a+r /etc/apt/keyrings/docker.asc
> 
> 4. 添加 Docker 仓库
> echo \
>   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
>   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
>   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
> 
> # 更新
> sudo apt-get update
> 
> # 5. 更新 APT 软件包缓存
> sudo apt update
> 
> # 确保现在 Docker 官方仓库安装 Docker 而不是 Debian 默认仓库：
> apt-cache policy docker-ce
> # 指向 https://download.docker.com/，确保是官方 Docker 仓库。
> 
> # 6. 安装 Docker
> 
> sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
> 
> # 7. 启动并验证 Docker
> 
> sudo systemctl start docker
> sudo systemctl enable docker
> 
> # 或是
> sudo service docker start
> sudo service docker start
> 
> 验证版本
> sudo docker --version
> ```
