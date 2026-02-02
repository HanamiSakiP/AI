## 1. 智能体组合的 ADK 原语
> ADK 提供了核心构建块——原语——使你能够在多智能体系统中构建和管理交互。
> * LLM 智能体： 由大型语言模型驱动的智能体。(参见 LLM 智能体)
> * 工作流智能体： 专门的智能体 (SequentialAgent、ParallelAgent、LoopAgent),旨在管理其子智能体的执行流程。(参见 工作流智能体)
> * 自定义智能体： 你自己的智能体，继承自 BaseAgent,具有专门的非 LLM 逻辑。(参见 自定义智能体)
> ```bash
> # LLM -> MAS -> MCP -> A2A -> A2UI
> # 组合模式
> # 1. 迭代优化模式 -> SequentialAgent评审/批评模式 
> # 2. 并行扇出/聚合模式 -> 评审/批评模式
> adk --version
> adk create 
> # 配置
> # adk create --type=config my_agent
> # cmd
> adk run 
> adk web
> adk api_server
> ```

> ### 1.1. 智能体层次结构 (父智能体、子智能体)
> ```py
> # 概念示例：定义层次结构
> from google.adk.agents import LlmAgent, BaseAgent
> # 定义单个智能体
> greeter = LlmAgent(name="Greeter", model="gemini-2.0-flash")
> task_doer = BaseAgent(name="TaskExecutor") # 自定义非-LLM 智能体
> 
> # 创建父智能体并通过 sub_agents 分配子智能体
> coordinator = LlmAgent(
>     name="Coordinator",
>     model="gemini-2.0-flash",
>     description="我负责协调问候和任务。",
>     sub_agents=[ # 在这里分配子智能体
>         greeter,
>         task_doer
>     ]
> )
> # 框架会自动设置：
> # assert greeter.parent_agent == coordinator
> # assert task_doer.parent_agent == coordinator
> ```
> * 建立层次结构：父智能体时将智能体实例列表传递给 sub_agents 参数来创建树结构。ADK 会在初始化期间自动在每个子智能体上设置 parent_agent 属性。
> * 单一父级规则：一个智能体实例只能作为子智能体添加一次。尝试分配第二个父级将导致 ValueError。
> * 重要性： 此层次结构定义了工作流智能体的作用域，并影响 LLM 驱动委派的潜在目标。你可以使用 agent.parent_agent 导航层次结构，或使用 agent.find_agent(name) 查找后代。

> ### 1.2. 作为编排器的工作流智能体
> ADK 包含从 BaseAgent 派生的专门智能体，它们自己不执行任务，而是编排其 sub_agents 的执行流程。

> #### 1.2.1 SequentialAgent
> * SequentialAgent: 按照列表顺序依次执行其 sub_agents。
>   * 上下文： 顺序传递相同的 InvocationContext,允许智能体通过共享状态轻松传递结果。
```py
# SequentialAgent
# 概念示例：顺序流水线
from google.adk.agents import SequentialAgent, LlmAgent
step1 = LlmAgent(name="Step1_Fetch", output_key="data") # 将输出保存到 state['data']
step2 = LlmAgent(name="Step2_Process", instruction="Process data from {data}.")

# 当 pipeline 运行时，Step2 可以访问 Step1 设置的 state['data']。
pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])
```

> #### 1.2.2 ParallelAgent
> * ParallelAgent: 并行执行其 sub_agents。来自子智能体的事件可能会交错出现。
>   * 上下文： 为每个子智能体修改 InvocationContext.branch(例如，ParentBranch.ChildName),提供一个不同的上下文路径，这在某些记忆实现中对隔离历史记录很有用。
>   * 状态： 尽管分支不同，所有并行子智能体都访问相同的共享 session.state,使它们能够读取初始状态并写入结果 (使用不同的键以避免竞争条件)。
```py
# ParallelAgent
# 概念示例：并行执行
from google.adk.agents import ParallelAgent, LlmAgent
fetch_weather = LlmAgent(name="WeatherFetcher", output_key="weather")
fetch_news = LlmAgent(name="NewsFetcher", output_key="news")

# 当 gatherer 运行时，WeatherFetcher 和 NewsFetcher 并发运行。
# 后续智能体可以读取 state['weather'] 和 state['news']。
gatherer = ParallelAgent(name="InfoGatherer", sub_agents=[fetch_weather, fetch_news])
```

> #### 1.2.3 LoopAgent
> * LoopAgent: 在循环中顺序执行其 sub_agents。
>   * 终止： 如果达到可选的 max_iterations,或者任何子智能体返回一个在其事件操作中设置了 escalate=True 的 Event,循环就会停止。
>   * 上下文和状态： 在每次迭代中传递相同的 InvocationContext，允许状态变化 (例如，计数器、标志) 在循环中持久化。
```py
# LoopAgent
# 概念示例：带条件的循环
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
# 用于检查状态的自定义智能体
class CheckCondition(BaseAgent): 
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("status", "pending")
        is_done = (status == "completed")
        yield Event(author=self.name, actions=EventActions(escalate=is_done)) # 如果完成则上升
# 可能更新 state['status'] 的智能体
process_step = LlmAgent(name="ProcessingStep")

# 当 poller 运行时，它重复执行 process_step 然后 Checker
# 直到 Checker 上升(state['status'] == 'completed')或者达到 10 次迭代。
poller = LoopAgent(
    name="StatusPoller",
    max_iterations=10,
    sub_agents=[process_step, CheckCondition(name="Checker")]
)
```

> ### 1.3. 交互与通信机制
>  系统内的智能体通常需要相互交换数据或触发彼此的操作。ADK 通过以下方式实现这一点：

> #### 1.3.1. 共享会话状态 (session.state)
>  对于在同一调用内操作的智能体 (因此通过 InvocationContext 共享同一个 Session 对象) 来说，这是最基本的被动通信方式。
> * 机制： 一个智能体 (或其工具/回调) 写入一个值 (context.state['data_key'] = processed_data),后续智能体读取它 (data = context.state.get('data_key'))。状态变化通过 CallbackContext 进行跟踪。
> * 便利性： LlmAgent 上的 output_key 属性会自动将智能体的最终响应文本 (或结构化输出) 保存到指定的状态键。
> * 性质： 异步、被动通信。非常适合由 SequentialAgent 编排的流水线或在 LoopAgent 迭代中传递数据。
> * 参见： [状态管理](https://adk.wiki/sessions/state/)
```py
# 概念示例：使用 output_key 和读取状态
from google.adk.agents import LlmAgent, SequentialAgent
agent_A = LlmAgent(name="AgentA", instruction="Find the capital of France.", output_key="capital_city")
agent_B = LlmAgent(name="AgentB", instruction="Tell me about the city stored in {capital_city}.")

# AgentA `运行，`将 "Paris" 保存到 state['capital_city']。
# AgentB 运行，其指令处理器读取 state['capital_city'] 以获取 "Paris"。
pipeline = SequentialAgent(name="CityInfo", sub_agents=[agent_A, agent_B])
```

> #### 1.3.2. LLM 驱动委派 (智能体转移)
>  利用 LlmAgent 的理解能力动态地将任务路由到层次结构内的其他适合智能体。
> * 机制： 智能体的 LLM 生成一个特定的函数调用：transfer_to_agent(agent_name='target_agent_name')。
> * 处理： AutoFlow(当存在子智能体或未禁止转移时默认使用) 拦截此调用。它使用 root_agent.find_agent() 识别目标智能体，并更新 InvocationContext 以切换执行焦点。
> * 需求： 调用的 LlmAgent 需要清晰的 instructions 来说明何时转移，潜在目标智能体需要不同的 description 以便 LLM 做出明智的决策。可以在 LlmAgent 上配置转移范围 (父级、子智能体、同级)。
> * 性质： 基于 LLM 解释的动态、灵活路由。
```py
# 概念设置：LLM 转移
from google.adk.agents import LlmAgent
booking_agent = LlmAgent(name="Booker", description="Handles flight and hotel bookings.")
info_agent = LlmAgent(name="Info", description="Provides general information and answers questions.")

# 如果 coordinator 收到 "Book a flight"，其 LLM 应生成：
# FunctionCall(name='transfer_to_agent', args={'agent_name': 'Booker'})
# 然后 ADK 框架将执行路由到 booking_agent。
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="你是助手。将预订任务委托给 Booker，将信息请求委托给 Info。",
    description="主要协调器。",
    # AutoFlow 通常在这里被隐式使用
    sub_agents=[booking_agent, info_agent]
)
```

> #### 1.3.3. 显式调用 (AgentTool)
> 允许 LlmAgent 将另一个 BaseAgent 实例视为可调用的函数或工具。
> * 机制： 将目标智能体实例包装在 AgentTool 中，并将其包含在父 LlmAgent 的 tools 列表中。AgentTool 为 LLM 生成相应的函数声明。
> * 处理： 当父 LLM 生成针对 AgentTool 的函数调用时，框架执行 AgentTool.run_async。此方法运行目标智能体，捕获其最终响应，将任何状态/工件变化转发回父上下文，并将响应作为工具的结果返回。
> * 性质： 同步 (在父流程内)、显式、受控的调用，就像任何其他工具一样。
>  (注意： 需要显式导入和使用 AgentTool)。
```py
# 概念设置：智能体作为工具
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import agent_tool
from pydantic import BaseModel
# 定义目标智能体（可以是 LlmAgent 或自定义 BaseAgent）
class ImageGeneratorAgent(BaseAgent): # 示例自定义智能体
    name: str = "ImageGen"
    description: str = "基于 Prompt 生成图像。"
    # ... 内部逻辑 ...
    async def _run_async_impl(self, ctx): # 简化的运行逻辑
        prompt = ctx.session.state.get("image_prompt", "默认 prompt")
        # ... 生成图像字节 ...
        image_bytes = b"..."
        yield Event(author=self.name, content=types.Content(parts=[types.Part.from_bytes(image_bytes, "image/png")]))
# 包装智能体
image_agent = ImageGeneratorAgent()
image_tool = agent_tool.AgentTool(agent=image_agent) # 包装智能体

# 父智能体使用 AgentTool
artist_agent = LlmAgent(
    name="Artist",
    model="gemini-2.0-flash",
    instruction="创建一个 Prompt 并使用 ImageGen 工具生成图像。",
    tools=[image_tool] # 包含 AgentTool
)

# Artist LLM 生成 prompt，然后调用：
# FunctionCall(name='ImageGen', args={'image_prompt': 'a cat wearing a hat'})
# 框架调用 image_tool.run_async(...)，运行 ImageGeneratorAgent。
# 生成的图片 Part 作为工具结果返回给 Artist agent。
```

> ## 2. example 常见多智能体模式

> ### 协调器/调度器模式
> * 结构： 一个中心 LlmAgent(协调器) 管理几个专门的 sub_agents。
> * 目标： 将传入请求路由到适当的专家智能体。
> * 使用的 ADK 原语：
>     * 层次结构： 协调器在 sub_agents 中列出专家。
>     * 交互： 主要使用 LLM 驱动委派(需要在子智能体上有清晰的 description 并在协调器上有适当的 instruction) 或 显式调用 (AgentTool)(协调器在其 tools 中包含用 AgentTool 包装的专家)。
```py
# 概念代码:使用 LLM 转移的协调器
from google.adk.agents import LlmAgent
billing_agent = LlmAgent(name="Billing", description="Handles billing inquiries.")
support_agent = LlmAgent(name="Support", description="Handles technical support requests.")

# 用户问 "My payment failed" -> 协调器的 LLM 应调用 transfer_to_agent(agent_name='Billing')
# 用户问 "I can't log in" -> 协调器的 LLM 应调用 transfer_to_agent(agent_name='Support')
coordinator = LlmAgent(
    name="HelpDeskCoordinator",
    model="gemini-2.0-flash",
    instruction="路由用户请求：付款问题使用 Billing 智能体，技术支持问题使用 Support 智能体。",
    description="主要帮助台路由器。",
    # 在 AutoFlow 中，allow_transfer=True 对于 sub_agents 通常是隐式的
    sub_agents=[billing_agent, support_agent]
)
```

> ### 顺序流水线模式
> * 结构： 一个 SequentialAgent 包含按固定顺序执行的 sub_agents。
> * 目标： 实现多步骤过程，其中一个步骤的输出输入到下一个步骤。
> * 使用的 ADK 原语：
>   * 工作流： SequentialAgent 定义顺序。
>   * 通信： 主要使用 共享会话状态。较早的智能体写入结果 (通常通过 output_key),较晚的智能体从 context.state 读取这些结果。
```py
# 概念代码:顺序数据流水线
from google.adk.agents import SequentialAgent, LlmAgent
validator = LlmAgent(name="ValidateInput", instruction="Validate the input.", output_key="validation_status")
processor = LlmAgent(name="ProcessData", instruction="Process data if {validation_status} is 'valid'.", output_key="result")
reporter = LlmAgent(name="ReportResult", instruction="Report the result from {result}.")

# validator 运行 -> 保存到 state['validation_status']
# processor 运行 -> 读取 state['validation_status'],保存到 state['result']
# reporter 运行 -> 读取 state['result']
data_pipeline = SequentialAgent(
    name="DataPipeline",
    sub_agents=[validator, processor, reporter]
)
```
```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)
// Conceptual Code: Sequential Data Pipeline
validator, _ := llmagent.New(llmagent.Config{Name: "ValidateInput", Instruction: "Validate the input.", OutputKey: "validation_status", Model: m})
processor, _ := llmagent.New(llmagent.Config{Name: "ProcessData", Instruction: "Process data if {validation_status} is 'valid'.", OutputKey: "result", Model: m})
reporter, _ := llmagent.New(llmagent.Config{Name: "ReportResult", Instruction: "Report the result from {result}.", Model: m})

// validator runs -> saves to state["validation_status"]
// processor runs -> reads state["validation_status"], saves to state["result"]
// reporter runs -> reads state["result"]
dataPipeline, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "DataPipeline", SubAgents: []agent.Agent{validator, processor, reporter}},
})
```

> ### 2.1 SequentialAgent 评审/批评模式 (生成器 - 批评者)
> * 结构： 通常涉及 SequentialAgent 中的两个智能体：一个生成器和一个批评者/评审者。
> * 目标： 通过让专门的智能体评审生成的输出来提高其质量或有效性。
> * 使用的 ADK 原语：
>   * 工作流： SequentialAgent 确保生成在评审之前发生。
>   * 通信： 共享会话状态(生成器使用 output_key 保存输出;评审者读取该状态键)。评审者可能将其反馈保存到另一个状态键以供后续步骤使用。
```py
# 概念示例：Generator-Critic
from google.adk.agents import SequentialAgent, LlmAgent
generator = LlmAgent(
    name="DraftWriter",
    instruction="Write a short paragraph about subject X.",
    output_key="draft_text"
)
reviewer = LlmAgent(
    name="FactChecker",
    instruction="Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    output_key="review_status"
)
# Optional: Further steps based on review_status
review_pipeline = SequentialAgent(
    name="WriteAndReview",
    sub_agents=[generator, reviewer]
)
# generator runs -> saves draft to state['draft_text']
# reviewer runs -> reads state['draft_text'], saves status to state['review_status']
```
```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)
// Conceptual Code: Generator-Critic
generator, _ := llmagent.New(llmagent.Config{
    Name:        "DraftWriter",
    Instruction: "Write a short paragraph about subject X.",
    OutputKey:   "draft_text",
    Model:       m,
})
reviewer, _ := llmagent.New(llmagent.Config{
    Name:        "FactChecker",
    Instruction: "Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    OutputKey:   "review_status",
    Model:       m,
})

reviewPipeline, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "WriteAndReview", SubAgents: []agent.Agent{generator, reviewer}},
})
// generator runs -> saves draft to state["draft_text"]
// reviewer runs -> reads state["draft_text"], saves status to state["review_status"]
```

> ### 2.2 LoopAgent 迭代优化模式
> * 结构： 使用一个 LoopAgent,其中包含一个或多个在多次迭代中处理任务的智能体。
> * 目标： 逐步改进存储在会话状态中的结果 (例如，代码、文本、计划),直到达到质量阈值或达到最大迭代次数。
> * 使用的 ADK 原语：
>   * 工作流： LoopAgent 管理重复。
>   * 通信： 共享会话状态对于智能体读取上一次迭代的输出并保存优化版本至关重要。
>   * 终止： 循环通常基于 max_iterations 或专用检查智能体在结果令人满意时在事件操作中设置 escalate=True 来结束。
```py
# 概念示例：Iterative Code Refinement
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
# Agent to generate/refine code based on state['current_code'] and state['requirements']
code_refiner = LlmAgent(
    name="CodeRefiner",
    instruction="Read state['current_code'] (if exists) and state['requirements']. Generate/refine Python code to meet requirements. Save to state['current_code'].",
    output_key="current_code" # 每次覆盖 state 中的代码
)
# Agent to check if the code meets quality standards
quality_checker = LlmAgent(
    name="QualityChecker",
    instruction="Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    output_key="quality_status"
)
# Custom agent to check the status and escalate if 'pass'
class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("quality_status", "fail")
        should_stop = (status == "pass")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))
        
# Loop runs: Refiner -> Checker -> StopChecker
# State['current_code'] is updated each iteration.
# Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
refinement_loop = LoopAgent(
    name="CodeRefinementLoop",
    max_iterations=5,
    sub_agents=[code_refiner, quality_checker, CheckStatusAndEscalate(name="StopChecker")]
)
```
```go
import (
    "iter"
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/loopagent"
    "google.golang.org/adk/session"
)
// Conceptual Code: Iterative Code Refinement
codeRefiner, _ := llmagent.New(llmagent.Config{
    Name:        "CodeRefiner",
    Instruction: "Read state['current_code'] (if exists) and state['requirements']. Generate/refine Python code to meet requirements. Save to state['current_code'].",
    OutputKey:   "current_code",
    Model:       m,
})
qualityChecker, _ := llmagent.New(llmagent.Config{
    Name:        "QualityChecker",
    Instruction: "Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    OutputKey:   "quality_status",
    Model:       m,
})

checkStatusAndEscalate, _ := agent.New(agent.Config{
    Name: "StopChecker",
    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
        return func(yield func(*session.Event, error) bool) {
            status, _ := ctx.Session().State().Get("quality_status")
            shouldStop := status == "pass"
            yield(&session.Event{Author: "StopChecker", Actions: session.EventActions{Escalate: shouldStop}}, nil)
        }
    },
})

// Loop runs: Refiner -> Checker -> StopChecker
// State["current_code"] is updated each iteration.
// Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
refinementLoop, _ := loopagent.New(loopagent.Config{
    MaxIterations: 5,
    AgentConfig:   agent.Config{Name: "CodeRefinementLoop", SubAgents: []agent.Agent{codeRefiner, qualityChecker, checkStatusAndEscalate}},
})
```

> ### 2.3 ParallelAgent to SequentialAgent 并行扇出/聚合模式
> * 结构： 一个 ParallelAgent 并发运行多个 sub_agents,通常后面跟着一个后续智能体 (在 SequentialAgent 中) 来聚合结果。
> * 目标： 同时执行独立任务以减少延迟，然后组合它们的输出。
> * 使用的 ADK 原语：
>   * 工作流： ParallelAgent 用于并发执行 (扇出)。通常嵌套在 SequentialAgent 中以处理后续的聚合步骤 (聚合)。
>   * 通信： 子智能体将结果写入 共享会话状态中的不同键。后续的“聚合”智能体读取多个状态键。
```py
# 概念代码：并行信息收集
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
fetch_api1 = LlmAgent(name="API1Fetcher", instruction="Fetch data from API 1.", output_key="api1_data")
fetch_api2 = LlmAgent(name="API2Fetcher", instruction="Fetch data from API 2.", output_key="api2_data")
gather_concurrently = ParallelAgent(
    name="ConcurrentFetch",
    sub_agents=[fetch_api1, fetch_api2]
)
synthesizer = LlmAgent(
    name="Synthesizer",
    instruction="Combine results from {api1_data} and {api2_data}."
)

# fetch_api1 和 fetch_api2 并发运行，保存到 state。
# synthesizer 随后运行，读取 state['api1_data'] 和 state['api2_data']。
overall_workflow = SequentialAgent(
    name="FetchAndSynthesize",
    sub_agents=[gather_concurrently, synthesizer] # 运行并行获取,然后合成
)
```
```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/parallelagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)
// Conceptual Code: Parallel Information Gathering
fetchAPI1, _ := llmagent.New(llmagent.Config{Name: "API1Fetcher", Instruction: "Fetch data from API 1.", OutputKey: "api1_data", Model: m})
fetchAPI2, _ := llmagent.New(llmagent.Config{Name: "API2Fetcher", Instruction: "Fetch data from API 2.", OutputKey: "api2_data", Model: m})
gatherConcurrently, _ := parallelagent.New(parallelagent.Config{
    AgentConfig: agent.Config{Name: "ConcurrentFetch", SubAgents: []agent.Agent{fetchAPI1, fetchAPI2}},
})
synthesizer, _ := llmagent.New(llmagent.Config{Name: "Synthesizer", Instruction: "Combine results from {api1_data} and {api2_data}.", Model: m})

// fetch_api1 and fetch_api2 run concurrently, saving to state.
// synthesizer runs afterwards, reading state["api1_data"] and state["api2_data"].
overallWorkflow, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "FetchAndSynthesize", SubAgents: []agent.Agent{gatherConcurrently, synthesizer}},
})
```

> ### 2.3 人机协作模式
> * 结构： 在智能体工作流中集成人类干预点。
> * 目标： 允许人类监督、审批、纠正或执行 AI 无法完成的任务。
> 使用的 ADK 原语 (概念):
> * 交互： 可以使用自定义工具实现，该工具暂停执行并向外部系统 (例如，UI、工单系统) 发送请求，等待人类输入。然后工具将人类的响应返回给智能体。
> * 工作流： 可以使用 LLM 驱动委派(transfer_to_agent) 针对概念上的“人类智能体”来触发外部工作流，或在 LlmAgent 内使用自定义工具。
> * 状态/回调： 状态可以保存人类的任务详情;回调可以管理交互流程。
> * 注意： ADK 没有内置的“人类智能体”类型，因此这需要自定义集成。
```py
# 概念示例：使用工具进行人工审批
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool
# --- Assume external_approval_tool exists ---
# This tool would:
# 1. Take details (e.g., request_id, amount, reason).
# 2. Send these details to a human review system (e.g., via API).
# 3. Poll or wait for the human response (approved/rejected).
# 4. Return the human's decision.
# async def external_approval_tool(amount: float, reason: str) -> str: ...
approval_tool = FunctionTool(func=external_approval_tool)

# Agent that prepares the request
prepare_request = LlmAgent(
    name="PrepareApproval",
    instruction="Prepare the approval request details based on user input. Store amount and reason in state.",
    # ... 可能设置 state['approval_amount'] 和 state['approval_reason'] ...
)
# Agent that calls the human approval tool
request_approval = LlmAgent(
    name="RequestHumanApproval",
    instruction="Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].",
    tools=[approval_tool],
    output_key="human_decision"
)
# Agent that proceeds based on human decision
process_decision = LlmAgent(
    name="ProcessDecision",
    instruction="Check {human_decision}. If 'approved', proceed. If 'rejected', inform user."
)

approval_workflow = SequentialAgent(
    name="HumanApprovalWorkflow",
    sub_agents=[prepare_request, request_approval, process_decision]
)
```
