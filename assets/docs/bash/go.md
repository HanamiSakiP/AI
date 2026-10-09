> [navi](https://github.com/denisidoro/navi)

## go
> ```bash
> g -v
> g use 1.25
> g ls
> g ls-remote
> g ls-remote stable
> # 清空g缓存
> g clean
> # 升级g版本
> g self update
> # g删除指定go版本
> g self uninstall 版本
> # 清空go缓存
> go clean -modcache && go clean -cache
> # 查看go下载(go install)
> ls $GOPATH/bin
> # go run main.go
> go run .
> ```
> ### go-cn(windows)
> ```shell
> go env -w GOPROXY=镜像网站,direct
> go env -w GO111MODULE=on
> ```
> ### go-cn(Linux)
> ```bash
> # ~/.bashrc
> export GOPROXY=镜像网站,direct
> export GO111MODULE=on  # 确保开启 Go Modules
> source ~/.bashrc
> ```
> ### go_tool
> ```bash
> go install github.com/restic/restic/cmd/restic@latest
> go install filippo.io/age/cmd/...@latest
> go install github.com/junegunn/fzf@latest
> go install github.com/rclone/rclone@latest
> go install github.com/maaslalani/nap@main
> go install github.com/charmbracelet/glow@latest
> go install github.com/boyter/scc/v3@latest
> go install github.com/zu1k/nali@latest
> go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
> go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
> go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
> go install github.com/gopasspw/gopass@latest
> go install github.com/LeperGnome/bt/cmd/bt@v1.2.0
> go install github.com/aurc/loggo@latest
> go install github.com/knqyf263/sou@latest
> go install github.com/dhth/omm@latest
> go install github.com/neilotoole/sq@latest
> go install github.com/rs/curlie@latest
> go install github.com/xo/usql@latest
> go install github.com/projectdiscovery/katana/cmd/katana@latest
> 
> # test
> go install github.com/brittonhayes/pillager@latest
> go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
> env CGO_ENABLED=0 go install -ldflags="-s -w" github.com/gokcehan/lf@latest
> ```

<details>
<summary></summary>

```bash
# 密钥生成
age-keygen -o key.txt
# 密钥解密
age -d -i key.txt -o 还原后的文件  加密的文件
# 密钥加密
age -p -i key.txt -o 加密后的文件  加密前的文件

# 加密
age -p -o secret.age secret.txt
# 解密
age -d  -o secret.txt secret.age
```

```bash
# rclone配置
rclone config
# n , 名字 , 服务
# 回车,回车,n,y,浏览器登陆,y
# 查看已配置的rclone
rclone listremotes
# 查看rclone内容(目录)
rclone lsd k:

# 快照查看
restic -r rclone:k:apk snapshots
# 查看快照内容(全部)
restic -r rclone:k:apk ls ID
# 查看快照某个内容
restic -r rclone:k:apk ls ID --path apk/debian
# 恢复快照中某个文件夹到本地(.表示当前目录)
restic -r rclone:k:apk restore latest --target apk --include .
```

```bash
# restic 仓库初始化
restic init -r o/apk
# restic 仓库备份( test 文件夹)
restic -r o/apk backup test
# 模拟增量同步 --progress（显示进度）
rclone sync o/apk k:apk --progress --dry-run
# 增量同步( o/apk 为本地目录)
rclone sync o/apk k:apk --progress
# restic 恢复快照中 test 文件夹到本地(.表示当前目录) (latest表示最新的快照ID)
restic -r o/apk restore latest --target test --include .

# 删除快照
restic forget ID
```

</details>

## pip
> ### pip_com
> ```bash
> pip list
> pip show pip
> pip install -i 镜像网站  httpie
> ```
> ### pip_tool
> ```bash
> pip install httpie
> pip install pathos
> pip install toolong
> 
> pipx run nvitop
> # uvx nvitop
> 
> python -m pip install aider-install
> aider-install
> ```
