> ## 下载fcitx5及中文拼音包
> ```bash
> apt install fcitx5 fcitx5-chinese-addons
> ```
>  ## 1. 主题下载安装
> * [关注塔菲喵](https://github.com/thep0y/fcitx5-themes-candlelight)
> ```bash
> git clone https://github.com/thep0y/fcitx5-themes.git
> cd fcitx5-themes
> cp spring ~/.local/share/fcitx5/themes -r
> vim ~/.config/fcitx5/conf/classicui.conf
> ```
>  ## 2. 主题配置（classicui.conf）
> ```bash
> # 垂直候选列表
> Vertical Candidate List=False
> # 按屏幕 DPI 使用
> PerScreenDPI=True
> # Font (设置成你喜欢的字体)
> Font="Smartisan Compact CNS 22"
> # 主题(这里要改成你想要使用的主题名，主题名就在下面)
> Theme=spring
> ```
>  ## 3. 快速输入
> * 配置 -> 附加组件 -> 快速输入 -> 配置 -> 添加/导入
>    * 键盘按 v   + 关键词触发
> ```bash
> # 我的词组配置
> ol	"ollama list"
> op	"ollama pull "
> dp	"docker ps"
> di	"docker images"
> ds	"docker start id"
> ds	"docker stop id"
> dcp	"docker compose ps"
> ad	"adk run\n"
> ad	"adk web "
> ad	"adk api_server --a2a --port 9999 "
> gi	"git add . && git commit -m \" AI\" && git push"
> ```

