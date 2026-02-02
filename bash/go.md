> [navi](https://github.com/denisidoro/navi)

## go
> ```bash
> g -v
> g use 1.25
> g ls
> g ls-remote
> g ls-remote stable
> g clean
> g self update
> g self uninstall
> go clean -modcache && go clean -cache
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
> 
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
