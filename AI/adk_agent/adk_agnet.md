> ## ADK_agent 安装与配置环境
> 
> ```bash
> # 创建虚拟环境
> python -m venv .venv
> # Linux
> # source .venv/bin/activate
> # Windows
> # .venv\Scripts\activate.bat
> # .venv\Scripts\Activate.ps1
> # 环境安装
>  pip install google-adk
>  pip install litellm
> # 创建项目文件夹
>  mkdir adk_agent/
> # 创建 __init__.py
>  echo "from . import agent" > adk_agent/__init__.py
> # 配置文件 adk_agent/.env
> # 1. OLLAMA API配置
> # OLLAMA_API_BASE=http://localhost:11434
> # 2. Deepseek API配置
> # DEEPSEEK_API_KEY=API_KEY
> # agent.py
> # 关键：导入LiteLLM适配器
> # from google.adk.models.lite_llm import LiteLlm
>     # model=LiteLlm(model="deepseek/deepseek-chat"),  # 关键配置
>     # ollama/qwen3-vl:2b
>     # deepseek/deepseek-chat
>     # deepseek-reasoner # 思考模式
> ```

## 1. ADK_agent example
```py
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
# 关键：导入LiteLLM适配器
from google.adk.models.lite_llm import LiteLlm

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() in ["beijing", "北京"]:
        return {
            "status": "success",
            "report": (
                "北京今天天气晴朗，温度25摄氏度（77华氏度）。"
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"抱歉，我没有'{city}'的天气信息。",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() in ["beijing", "北京"]:
        tz_identifier = "Asia/Shanghai"
    else:
        return {
            "status": "error",
            "error_message": (
                f"抱歉，我没有{city}的时区信息。"
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'{city}的当前时间是 {now.strftime("%Y年%m月%d日 %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


# 核心配置：使用LiteLLM连接Ollama本地模型
root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(model="deepseek/deepseek-chat"),  # 关键配置
    # ollama/qwen3-vl:2b
    # deepseek/deepseek-chat
    # deepseek-reasoner # 思考模式
    description=(
        "一个可以回答城市时间和天气问题的智能助手"
    ),
    instruction=(
        "你是一个有用的智能助手，可以回答用户关于城市时间和天气的问题。请始终使用中文回复，语气要友好亲切。"
    ),
    tools=[get_weather, get_current_time],
)
```

> ## 2. 启动
> ```bash
> # 方式1：可视化Web界面（推荐）
> adk web
> # 左上角下拉菜单选择 "adk_agent"
> 
> # 方式2：命令行终端
> adk run adk_agent
> 
> # 方式3：API服务接口
> adk api_server
> # 报错信息(检查)
> # Error: Fail to load 'adk_agent' module. source code string cannot contain null bytes
> # 常见错误1
> #  编码错误 文件 __init__.py
> # 常见错误2
> # LiteLLM completion() model= qwen3-vl:2b; provider = ollama
> # model不兼容
> ```
> 
> ```bash
> # 快速创建命令
> adk create adk_agent_samples
> ```
