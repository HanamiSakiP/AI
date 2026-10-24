<div align="center">
<h1 align="center">
<a href="/luJTwX54bBjJ7R1f5lkd7gQ" title="关注塔菲喵">
<img src="assets/docs/images/M.jpg" width="200" alt="">
</a>
<br/>
devmgr
</h1>
</div>

## 简介

* start
```bash
mkdir -p ~/.local/share/devmgr/backups
git -C ~/.local/share/devmgr clone https://github.com/HanamiSakiP/AI.git
```
```bash
cp -r ~/.local/share/devmgr/AI/dev/backups ~/.local/share/devmgr/
mkdir -p ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/dev ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/dev-tool ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/tool ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/undev ~/.local/bin
install -m755 ~/.local/share/devmgr/AI/dev/doc ~/.local/bin
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
