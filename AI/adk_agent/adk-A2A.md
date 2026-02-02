## A2A 安装与配置环境
<details>
<summary>A2A 安装与配置环境（点击展开）</summary>

```bash
# 安装a2a
pip install google-adk[a2a]
```
```bash
# A2A_create
# 快速创建命令
mkdir a2a_root
cd a2a_root
adk create remote_a2a
2
cd remote_a2a
mkdir hello_world
mv *.py hello_world
# move *.py hello_world
```

</details>

## 1. 远程A2A
<details>
<summary>结构与启动（点击展开）</summary>

```bash
# 结构
a2a_root/
├── remote_a2a/
│   └── hello_world/    
│       ├── __init__.py
│       └── agent.py    # 远程 agent
├── README.md
└── agent.py            # 根智能体
```
```bash
# 远程启动
# 确保当前工作目录是 adk-A2A/
# 使用 uvicorn 启动远程智能体
uvicorn a2a_root.remote_a2a.hello_world.agent:a2a_app --host localhost --port 8001
# 查看检查你的远程智能体是否正在运行
curl  http://localhost:8001/.well-known/agent-card.json
```

</details>

> ### 远程A2A实现
<details>
<summary>远程python代码（点击展开）</summary>
白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>

## 2. 消费与远程
<details>
<summary>结构与启动（点击展开）</summary>

```bash
a2a_basic/
├── remote_a2a/
│   └── check_prime_agent/ # 远程根智能体
│       ├── __init__.py
│       ├── agent.json
│       └── agent.py
├── README.md
├── root_agent_a2a/
│   └── root_agent/
│       ├── __init__.py
│       ├── agent.json
│       └── agent.py # 本地根智能体
```
```bash
# 远程启动
adk api_server --a2a --port 8001  a2a_basic/remote_a2a 
# 查看检查你的远程智能体是否正在运行
curl http://localhost:8001/a2a/check_prime_agent/.well-known/agent-card.json
```
```bash
# 本地web启动
adk web ./a2a_basic/root_agent_a2a
# 命令行启动
# adk run ./a2a_basic/root_agent_a2a
```

</details>

> ### 远程
<details>
<summary>远程python代码（点击展开）</summary>
白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>

> ### 消费
<details>
<summary>消费python代码（点击展开）</summary>
白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>
