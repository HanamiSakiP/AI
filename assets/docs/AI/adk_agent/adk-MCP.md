## MCP_pyReadme
<details>
<summary>go转py必学知识点（点击展开）</summary>


```py
# excel-mcp-server
# npm i @negokaz/excel-mcp-server
# go转py必学知识点
""" go-0. 导包
import os # 1. Python内置库
from dotenv import load_dotenv # 2. 第三方库
from mcp import types as mcp_types # 3. 别名导入
"""

"""go-1. 装饰器语法 AND 类实例化
    @符号是装饰器，用于修改函数行为
    类似Go的中间件，但语法更简洁
# 类实例化
Server("adk-tool-exposing-mcp-server")  # 创建实例，无需new关键字
LlmAgent(model='gemini-2.0-flash', ...) # 命名参数
"""

"""go-2. 函数定义 AND 列表和字典(map)
    func == def
    async def：定义异步函数（类似Go的goroutine）
    """文档字符串"""：函数文档，类似Go 注释 但更正式
name: str                    # 变量类型 提示
arguments: dict             # 字典类型
-> list[mcp_types.Content]  # 返回类型 Python可选，Go必须
# 列表和字典
return [mcp_tool_schema]  # 列表，Go用[]interface{}{...}
args=[PATH_TO...]        # 列表参数
{ "type": "text" }       # 字典字面量，Go用map[string]interface{}{}
"""

""" go-3. 异步编程
async def run_mcp_stdio_server():  # 定义异步函数
async with ... as ...:            # 异步上下文管理器
await app.run(...)                 # 等待异步操作
# 一般在main函数那
asyncio.run(...)                  # 运行异步主函数
"""

""" go-4. main
    Go的package main → Python的if __name__ == "__main__":作为入口
"""

""" go-5. 异常处理
    as e将异常赋值给变量
    finally同Go
try:
    # 可能出错的代码
except Exception as e:  # 捕获异常
    # 处理异常
finally:
    # 无论是否异常都执行
"""

""" go-0. iferr
var = "string"
    printf("err")
"""
```

</details>

<details>
<summary>结构（点击展开）</summary>

```bash
# 结构
adk_mcp/
├── adk_agent_samples/
│   └── mcp_client_agent/
│   │    ├── __init__.py
│   │    └── agent.py
│   └── .env
└── my_adk_mcp_server.py # 本地mcp_server
```

</details>

<details>
<summary>package_py mcp_server（点击展开）</summary>

```py
# ./my_adk_mcp_server.py
""" go-0. 导包
import os # 1. Python内置库
from dotenv import load_dotenv # 2. 第三方库
from mcp import types as mcp_types # 3. 别名导入
"""
# my_adk_mcp_server.py
import asyncio
import json
import os
from dotenv import load_dotenv

# 1. MCP 服务器导入
from mcp import types as mcp_types # 使用别名以避免冲突
# mcp_server AND 服务器能力
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio # 用于作为 stdio 服务器运行

# 2. ADK 工具导入
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.load_web_page import load_web_page # 示例 ADK 工具
# ADK <-> MCP 转换工具
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

```

</details>

> ### home. func mcp_server
<details>
<summary>func mcp_server（点击展开）</summary>
白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>

> ### end. iferr McpToolset
<details>
<summary>McpToolset（点击展开）</summary>
白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>

> ### mcp_server example
<details>
<summary>消费python代码（点击展开）</summary>
白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>
