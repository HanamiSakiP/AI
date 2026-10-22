<div align="center">
<h1 align="center">
<a href="/luJTwX54bBjJ7R1f5lkd7gQ" title="关注塔菲喵">
<img src="assets/docs/images/M.jpg" width="200" alt="">
</a>
<br/>
CrazyThursdayVivo50
</h1>
</div>

## 简介

* start
```bash
mkdir -p ~/.local/share/devmgr/backups
cd ~/.local/share/devmgr
git clone https://github.com/HanamiSakiP/AI.git
```
```bash
cp -r ~/.local/share/devmgr/AI/dev/backups ~/.local/share/devmgr/
mkdir -p ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/dev ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/dev-tool ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/tool ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/undev ~/.local/bin
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
ls ~/.local/bin
dev restore # install
dev-tool
tool
source ~/.bashrc
ls ~/.local/share/devmgr/backups
```

<details>
<summary>test</summary>

docker
```bash
docker run -d --name test-debian debian:latest sleep infinity
docker exec -it test-debian mkdir -p /root/.local/share/devmgr/AI
docker cp ~/.local/share/devmgr/AI test-debian:/root/.local/share/devmgr/AI
docker exec -it test-debian /bin/bash
# 强制删除容器
# docker rm -f test-debian
```
podman
```bash
podman run -d --name test-debian debian:latest sleep infinity
podman exec -it test-debian mkdir -p /root/.local/share/devmgr/devmgr/AI
podman cp ~/.local/share/devmgr/AI test-debian:/root/.local/share/devmgr/AI
podman exec -it test-debian /bin/bash
# 强制删除容器
# podman rm -f test-debian
```
apt
```bash
apt update
apt install curl git -y # nano
```
```bash
# pyenv依赖
apt install -y build-essential \
libssl-dev \
zlib1g-dev \
libbz2-dev \
libreadline-dev \
libsqlite3-dev \
libffi-dev \
liblzma-dev \
pkg-config
```

</details>
