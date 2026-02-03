## lang版本控制
> * [go](https://github.com/voidint/g)
> * [node](https://github.com/nvm-sh/nvm)
> * [python](https://github.com/pyenv/pyenv)
> ### 1. lang-install
> ```bash
> curl -fsSL https://pyenv.run | bash
> curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
> curl -sSL https://raw.githubusercontent.com/voidint/g/master/install.sh | bash
> ```
> ### 2. lang-config环境
> ```bash
> # ~/.bashrc
> # pyenv
> echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
> echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
> echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
> cat << 'EOF' >> ~/.bashrc
> # Check if the alias 'g' exists before trying to unalias it
> if [[ -n $(alias g 2>/dev/null) ]]; then
>     unalias g
> fi
> # nvm
> export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
> [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
> EOF
> source "$HOME/.g/env"
> exec "$SHELL"
> ```
> ### 3. lang-tool常用命令
> ```bash
> pyenv install 3.10.4
> pyenv global 3.10.4
> pyenv shell 3.10.4
> # 1. 下载指定版本
> g install 1.25.1
> nvm install v18.20.8
> # 2. 设置版本
> g use 1.25.1
> nvm use v18.20.8
> # 设置当前目录
> pyenv local 3.10.4
> # 3. 查看已下载
> g ls
> mvm ls
> pyenv version
> # 4. 查询下载列表
> g ls-remote
> nvm list-remote
> pyenv install --list
> ```

## git AND tmux

> ### git AND tmux install
> ```bash
> apt update
> apt install -y tmux git nano curl
> ```

> ### tmux
> ```bash
> # 创建会话和后台输出命令
> tmux new-session -d -s mcp_server
> tmux send-keys -t mcp_server "go run /path/mcp_server/." Enter
> tmux new-session -d -s a2a_server
> tmux send-keys -t mcp_server "go run /path/a2a_server/." Enter
> tmux new-session -d -s a2a_client
> tmux send-keys -t mcp_server "go run /path/a2a_client/." Enter
> # 查询会话
> tmux ls
> ```
> ```bash
> # 删除会话
> tmux kill-session -t mcp_server
> tmux kill-session -t a2a_server
> tmux kill-session -t a2a_client
> ```

> ### git
> ```bash
> # 下载项目
> git clone 地址  指定目录(没有设置则默认当前目录)
> # 查看已配置的远程仓库,名称 + 对应 URL
> git remote -v
> # 查看单个远程仓库的详细信息
> git remote show origin  # 替换 origin 为你的远程仓库简称
> ```
> git SSH_Config
> ```bash
> # 生成 SSH 密钥并使用
> ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"
> # 查看生成的密钥（复制到GitHub上）
> cat ~/.ssh/id_rsa.pub
> ```
> git USE
> ```bash
> # 在当前目录初始化git
> git init
> # 添加远程仓库
> git remote add origin git@github.com:username/repository.git
> # 添加所有文件
> git add .
> # 推送本地仓库，并描述
> git commit -m "Initial commit with all files"
> # 推送远程仓库
> git push -u origin master
> ```
>  git 后续使用
> ```bash
> # 查看当前状态
> git status
> # 添加更改
> # 添加所有更改到暂存区
> git add .
> # 添加特定文件
> # git add 文件名
> # 提交更改
> git commit -m "描述你的更改"
> # 推送更改到远程仓库(默认为初次配置的远程仓库)
> git push
> # 查看提交历史
> git log
> # 清空暂存区
> # git reset
> ```

>  git 后续使用2
> ```bash
> # 添加子模块
> git submodule add https://github.com/iphysresearch/GWToolkit.git GWToolkit
> # 初始化更新子模块
> git submodule update --init --recursive
> # 查看当前状态
> git status
> ```
> * 此时已生成了.gitmodules 显示如下
> ```text
> $ git status
> 位于分支 main
> 您的分支与上游分支 'origin/main' 一致。
> 要提交的变更：
>   （使用 "git restore --staged <文件>..." 以取消暂存）
> 	新文件：   .gitmodules
> 	新文件：   GWToolkit
> ```
> ```bash
> # 查看子模块
> git submodule
> # 更新项目内子模块到最新版本
> git submodule update
> # 更新子模块为远程项目的最新版本
> git submodule update --remote
> # 1. 删除子模块文件夹
> git rm --cached GWToolkit
> rm -rf GWToolkit
> 
> 2. 删除 .gitmodules 文件中相关子模块的信息，类似于：
> ```text
> [submodule "GWToolkit"]
>         path = GWToolkit
>         url = https://github.com/iphysresearch/GWToolkit.git
> ```
> 
> 3. 删除 .git/config 中相关子模块信息，类似于：
> ```text
> [submodule "GWToolkit"]
>         url = https://github.com/iphysresearch/GWToolkit.git
>         active = true
> ```
>  
> 4. 删除 .git 文件夹中的相关子模块文件
> ```bash
> rm -rf .git/modules/GWToolkit
> ```text
> ```

浏览器夜间插件
[dark-background-light-text](https://addons.mozilla.org/firefox/addon/dark-background-light-text/)
> ```text
> #ffffff
> #241f31
> #deddda
> #9a9996
> #ff0000
> #8080ff
> ```


https://docs.nvidia.com/cuda/cuda-installation-guide-linux/

> ## 修复vlc打不开
> ### 重置配置和插件缓存（持久修复）
> ```bash
> vlc --reset-config
> vlc --reset-plugins-cache
> ```
