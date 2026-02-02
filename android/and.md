施工中。。。
> * [lineageos](https://lineageos.org/)
> * [grapheneos](https://grapheneos.org/)
## grapheneos安装
> ### 前期准备
> 1. 关于本机  -> 快速点击版本号   -> 进入到开发者模式
> 2. 进入开发者模式,下拉找到OEM解锁和usb调试,都打开.
> 3.关机,同时按住电源和音量减弱按钮几秒钟,启动Bootloader界面.然后手机 usb 连接电脑.
> [![](../img/wr2.jpg)](https://www.google.com/chrome/ "推荐chrome浏览器")
> * 此为 chrome官网
> ### web安装
> * [grapheneos-web-install](https://grapheneos.org/install/web#prerequisites)
>   * 1. 解锁引导程序,网页点击 Unlock bootloader .然后在手机上按音量+或者-接受,再点电源键确认.手机屏幕显示 Bootloader is already unlocked.
>       * 2. 下载系统, 网页点击 Download release 。
>       * 3. 开始刷机, 下载完成后，网页点击 Flash release ，等待刷机结束。期间不要拔数据线！要选择接触良好的数据线。
>       * 4. 锁定 bootloader , 刷机结束后手机又回到引导界面，在 bootloader 界面，需要将其设置为锁定，网页端点击Lock bootloader，在手机上按音量+或者-接受，电源键确认。
>       * 5. 完成!  手机屏幕 -> 显示 Bootloader locked.
## 安卓开发
> * [flutter 官网](https://docs.flutter.dev/get-started/install)
> * [Android Studio 官网](https://developer.android.com/studio)
> ```bash
> # flutter安装
> # 1. 将文件解压到想要存储 Flutter SDK 的目录中
> tar -xf ~/Downloads/flutter_linux_3.35.3-stable.tar.xz -C ~/development/
> # 2. 将 Flutter 添加到您的PATH
> echo 'export PATH="$HOME/development/flutter/bin:$PATH"' >> ~/.bash_profile
> ```
> ```bash
> # 3. 启用签名许可证
> flutter doctor --android-licenses
> ```
> ```bash
> # 4. 该flutter doctor命令验证 Linux 的完整 Flutter 开发环境的所有组件
> flutter doctor
> ```
> ```bash
> # 5. Android Studio安装
> # 解压后
> sudo mv -xzf ~/Downloads/android-studio/ /opt/android-studio-stable
> # 启动
> /opt/android-studio-stable/bin/studio.sh
> ```


