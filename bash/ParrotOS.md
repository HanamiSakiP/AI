## 1. Parrot-OS 下载与配置
* [Parrot-OS官网](https://parrotsec.org/)

### 哈希值检查
<details>
<summary>如何检查哈希值（点击展开）</summary>

```bash
# 此处以 Parrot-security-7.0_amd64.iso 为例
# 进入ISO文件所在目录
cd /path/to/iso/
# 计算MD5哈希
md5sum Parrot-security-7.0_amd64.iso
# 计算SHA256哈希
sha256sum Parrot-security-7.0_amd64.iso
# 计算SHA512哈希
sha512sum Parrot-security-7.0_amd64.iso
# 自行对比
```

</details>


### 安装系统
<details>
<summary>1. 安装系统(Linux)（点击展开）</summary>

* 1. 首先需要一个 U 盘,进行烧录系统
* [balena官网下载](https://github.com/balena-io/etcher/releases)
```bash
# 1. 烧录 U 盘
# 选择.deb下载
# 以 balena-etcher_2.1.4_amd64.deb 为例
# 自行加sudo
dpkg -i balena-etcher_2.1.4_amd64.deb 
# 运行图形化
balena-etcher 
# 1.1 点击 Flash from file
# 选择ISO文件(镜像)
# Parrot-security-7.0_amd64.iso
# 1.2 Select target 选择U盘进行烧录
# 1.3 Flash! 选择U盘进行烧录
```
* 2. 重启 , 进入BIOS选择 USB 启动 (一般按F2,如不是,上官网查询)
* 3. 启动后按照提示安装即可

白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>
<details>
<summary>2. 安装系统(windows)（点击展开）</summary>

* 1. 首先需要一个 U 盘,进行烧录系统
* [balena官网下载](https://github.com/balena-io/etcher/releases)
    * 1.1 点击 Flash from file
    * 选择ISO文件(镜像)
    * Parrot-security-7.0_amd64.iso
    * 1.2 Select target 选择U盘进行烧录
    * 1.3 Flash! 选择U盘进行烧录

* 2. 重启 , 进入BIOS选择 USB 启动 (一般按F2,如不是,上官网查询)
* 3. 启动后按照提示安装即可

白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>

* 安装其他系统同理

### 个性化设置
```bash
# 1. 桌面背景
# 左上角点击   系统  -> 首选项 -> 外观  -->  外观  --->   背景
# 2. 锁屏背景
# 左上角点击   系统  -> 首选项 -> 外观  -->  屏幕保护程序  --->   锁屏背景图
# 自定义锁屏背景需要在 放在 锁屏背景路径下
sudo -i
# 锁屏背景路径
cd /usr/share/images/desktop-base/
cp path/bg.jpg  .
```

### 系统更新

<details>
<summary>系统更新（点击展开）</summary>

* 还没找到喵

白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>

## 2. Parrot-OS 显卡驱动安装

### 1. 前期准备
```bash
# 1.1. 检查显卡型号
lspci | grep -i vga
# 针对 NVIDIA/AMD 专用
lspci | grep -i nvidia
lspci | grep -i amd
# 1.2. 检查当前驱动
# 如果输出为空，说明使用默认开源驱动。
lsmod | grep -i nvidia  # NVIDIA
lsmod | grep -i amdgpu # AMD
# 1.3. 更新软件源： 编辑 /etc/apt/sources.list 文件
sudo nano /etc/apt/sources.list
```
* 确保你的源包含 main contrib non-free non-free-firmware，例如
```lsit
deb http://deb.parrotsec.org/parrot rolling main contrib non-free non-free-firmware
deb http://deb.parrotsec.org/parrot rolling-security main contrib non-free non-free-firmware
```
* 保存后，运行
```bash
# 1.4. 更新系统内核和依赖
sudo apt update && sudo apt full-upgrade -y
# 1.5. 通用依赖
# build-essential：编译工具。
# dkms：动态内核模块支持，确保驱动在内核更新后存活。
# linux-headers：匹配当前内核。
# firmware-misc-nonfree：非自由固件。
sudo apt install build-essential dkms linux-headers-$(uname -r) firmware-misc-nonfree
```
* 避坑提示：如果使用 Secure Boot（UEFI），需禁用或签名驱动模块。运行 mokutil --sb-state 检查 Secure Boot 状态。如果启用，安装时会提示错误，需进入 BIOS 禁用。
* 测试：在 Live USB 模式下运行 Parrot OS，测试驱动兼容性。
常见新手坑：
* 坑1：直接从 NVIDIA/AMD 官网下载 .run 文件安装。这会覆盖系统文件，导致无法恢复。解决方案：优先使用仓库安装。
* 坑2：忽略 Xorg 配置。安装后图形界面黑屏，通常因 Xorg 未识别驱动。
* 坑3：混合使用开源和专有驱动。解决方案：卸载开源驱动：sudo apt remove xserver-xorg-video-nouveau (NVIDIA) 或 sudo apt remove xserver-xorg-video-amdgpu (AMD)。

### 2. NVIDIA 显卡驱动安装实战操作
```bash
# 2.1 检测并选择驱动版本
sudo apt install nvidia-detect
sudo nvidia-detect
# 2.2 安装驱动
# 步骤1：卸载旧驱动（如果有）：
sudo apt purge nvidia* libnvidia*  # 清除所有 NVIDIA 相关
sudo apt autoremove
步骤2：安装推荐驱动
sudo apt install nvidia-driver
# 或指定版本（如 535）：
# sudo apt install nvidia-driver-535

# 步骤3：安装 CUDA 工具包（可选，用于 GPU 计算，如 Hashcat）：
sudo apt install nvidia-cuda-toolkit
# 验证
nvcc --version
# 步骤4：配置 Xorg（如果黑屏）： 编辑 /etc/X11/xorg.conf（备份原文件）：
sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf.bak
sudo nvidia-xconfig  # 自动生成配置
# 如果无 xorg.conf，运行：
sudo nvidia-xconfig --enable-all-gpus --connected-monitors
# 步骤5：重启并验证：
sudo reboot
# 重启后，运行
nvidia-smi  # 显示 GPU 状态、温度、驱动版本
```
示例输出：
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03   Driver Version: 535.129.03   CUDA Version: 12.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0 Off |                  N/A |
| N/A   45C    P8    N/A /  N/A |    100MiB /  4096MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

### 2.3 常见问题解决

问题1：安装后黑屏或无法进入图形界面。
* 原因：Nouveau 未禁用。
* 解决：编辑 /etc/modprobe.d/blacklist-nouveau.conf：
添加：
```
blacklist nouveau
options nouveau modeset=0
```
```bash
sudo update-initramfs -u
# 重启
# 问题2：DKMS 编译失败（内核不匹配）。
# 解决：确保 headers 安装正确：sudo apt install linux-headers-$(uname -r)。然后：
sudo dkms autoinstall
# 问题3：多显示器或分辨率问题。
# 使用 nvidia-settings GUI 工具调整：
# nvidia-settings
# 或编辑 /etc/X11/xorg.conf 添加 Monitor 部分。
# 性能优化：启用 Coolbits 以超频（风险高）： 在 xorg.conf 的 Device 部分添加：
# Option "Coolbits" "8"
# 重启后用 nvidia-settings 调整。
# 如果你的 NVIDIA 卡是 Optimus（笔记本混合显卡），需安装 nvidia-prime 并配置 PRIME 切换：
sudo apt install nvidia-prime
prime-select nvidia  # 切换到 NVIDIA
# 重启验证
prime-select query
```

## 3. Ollama安装与命令
```bash
curl -fsSL https://ollama.com/install.sh | sh
# 查看版本
ollama -v
# 查看已下载模型
ollama list
# 下载模型
ollama pull qwen3:0.6b
# 使用模型(无则会进行下载)
ollama run qwen3:0.6b
# 开启服务
ollama server
# 查询服务是否启动
curl 127.0.0.1:11434
# 成功返回 Ollama is running
```
