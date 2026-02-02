> ## eino-tool
> ```go
> // main.go
> /*
> type ToolInfo struct {
>     // 工具的唯一名称，用于清晰地表达其用途
>     Name string
>     // 用于告诉模型如何/何时/为什么使用这个工具
>     // 可以在描述中包含少量示例
>     Desc string
>     // 工具接受的参数定义
>     // 可以通过两种方式描述：
>     // 1. 使用 ParameterInfo：schema.NewParamsOneOfByParams(params)
>     // 2. 使用 OpenAPIV3：schema.NewParamsOneOfByOpenAPIV3(openAPIV3)
>     *ParamsOneOf
> }
> */
> 
> /*
> ->  // 0. ctx
> ->  // 1. Info(ctx context.Context) (*schema.ToolInfo, error)
> ->  // 2. InvokableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (string, error)
> ->  // 2. StreamableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (*schema.StreamReader[string], error)
> // 二选一
> --->  // end. 调用设置好的工具
> */
> ```

> ## struct AND interface
> ```go
> // 接口定义
> // Tool 组件提供了三个层次的接口：
> // 基础工具接口，提供工具信息
> type BaseTool interface {
>     Info(ctx context.Context) (*schema.ToolInfo, error)
> }
> 
> // 可调用的工具接口，支持同步调用
> type InvokableTool interface {
>     BaseTool
>     InvokableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (string, error)
> }
> 
> // 支持流式输出的工具接口
> type StreamableTool interface {
>     BaseTool
>     StreamableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (*schema.StreamReader[string], error)
> }
> /*
> Info 方法
> 功能：获取工具的描述信息
> 参数：
> ctx：上下文对象
> 返回值：
> *schema.ToolInfo：工具的描述信息
> error：获取信息过程中的错误
> InvokableRun 方法
> 功能：同步执行工具
> 参数：
> ctx：上下文对象，用于传递请求级别的信息，同时也用于传递 Callback Manager
> argumentsInJSON：JSON 格式的参数字符串
> opts：工具执行的选项
> 返回值：
> string：执行结果
> error：执行过程中的错误
> StreamableRun 方法
> 功能：以流式方式执行工具
> 参数：
> ctx：上下文对象，用于传递请求级别的信息，同时也用于传递 Callback Manager
> argumentsInJSON：JSON 格式的参数字符串
> opts：工具执行的选项
> 返回值：
> *schema.StreamReader[string]：流式执行结果
> error：执行过程中的错误
> */
> 
> type ToolInfo struct {
>     // 工具的唯一名称，用于清晰地表达其用途
>     Name string
>     // 用于告诉模型如何/何时/为什么使用这个工具
>     // 可以在描述中包含少量示例
>     Desc string
>     // 工具接受的参数定义
>     // 可以通过两种方式描述：
>     // 1. 使用 ParameterInfo：schema.NewParamsOneOfByParams(params)
>     // 2. 使用 OpenAPIV3：schema.NewParamsOneOfByOpenAPIV3(openAPIV3)
>     *ParamsOneOf
> }
> ```

### func_tool
```go
package main
import (
	"context"

	"github.com/cloudwego/eino-ext/components/model/ollama"
	"github.com/cloudwego/eino/adk"
	"github.com/cloudwego/eino/components/model"
	"github.com/cloudwego/eino/components/tool"
	"github.com/cloudwego/eino/compose"
	"github.com/cloudwego/eino/schema"
)
/*
type BaseTool interface {
    Info(ctx context.Context) (*schema.ToolInfo, error)
}

type InvokableTool interface {
    BaseTool
    InvokableRun(ctx context.Context, argumentsInJSON string, opts ...Option) (string, error)
}
*/

// home. 将功能封装为Tool
type RAGTool struct {}
// 1. NewRAGTool 创建RAG工具实例
func getFileExtensions(config *RAGToolConfig) []string {}
// 2. RAGToolConfig RAG工具配置
type RAGToolConfig struct {}
// 3. Info 返回工具信息
func (r *RAGTool) Info(ctx context.Context) (*schema.ToolInfo, error) {
	return &schema.ToolInfo{
        // 工具的唯一名称，用于清晰地表达其用途
        Name string
        // 用于告诉模型如何/何时/为什么使用这个工具
        // 可以在描述中包含少量示例
        Desc string
        // 可选，一般不用
        // 不是必须项就别硬加
        // 工具接受的参数定义
        // 可以通过两种方式描述：
        // 1. 使用 ParameterInfo：schema.NewParamsOneOfByParams(params)
        // 2. 使用 OpenAPIV3：schema.NewParamsOneOfByOpenAPIV3(openAPIV3)
        // *ParamsOneOf
    }, nil
}
// 4. InvokableTool interface 
// opts ...tool.Option == BaseTool?
func (r *RAGTool) InvokableRun(ctx context.Context, argumentsInJSON string, opts ...tool.Option) (string, error) {
    return string,nil
}
// end. 具体实现
func (r *RAGTool) xx() () {}
```

#### func_tool adk_agent_main
```go
package main
import (
	"context"

	"github.com/cloudwego/eino-ext/components/model/ollama"
	"github.com/cloudwego/eino/adk"
	"github.com/cloudwego/eino/components/tool"
	"github.com/cloudwego/eino/compose"
	"github.com/cloudwego/eino/schema"
)
func main(){
    // 1. NewRAGTool
    ragTool, err := NewRAGTool(rdb, config)
    // adk_agent-1. 创建 NewChatModelAgent 绑定 ToolsNodeConfig
	chatModel, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
		BaseURL: "http://localhost:11434",
		Model:   "qwen3-vl:2b",
	})
    agent, err := adk.NewChatModelAgent(ctx, &adk.ChatModelAgentConfig{
        Name:        "SummaryAgent",
		Description: "Agent that summarizes A2A agent responses",
		Instruction: "你是一个专业的总结助手。你需要对输入的文本进行精炼、总结，提取关键信息，并以清晰、简洁的方式呈现。",
		Model:       chatModel,
		ToolsConfig: adk.ToolsConfig{
			ToolsNodeConfig: compose.ToolsNodeConfig{
				Tools: []tool.BaseTool{ragTool},
			},
		},
    })
    // adk_agent-2. 创建Runner
	runner := adk.NewRunner(ctx, adk.RunnerConfig{
		Agent:           agent,
		EnableStreaming: false,
	})
    // adk_agent-3. 输出
	// adk_agent-3. 输出
	iter := runner.Run(ctx, []adk.Message{
		schema.UserMessage("写个如何快速入睡教程"),
	})
	for {
		event, ok := iter.Next()
		if !ok {
			break
		}
		if event.Err != nil {
			log.Fatal(event.Err)
		}
		msg, err := event.Output.MessageOutput.GetMessage()
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("\nmessage:\n%v\n======", msg)
	}
}
```

### func_ToolsNode_main
```go
package main
import (
    "github.com/cloudwego/eino/components/tool"
    "github.com/cloudwego/eino/compose"
    "github.com/cloudwego/eino/schema"
)
func main(){
    /*
    // 1. 创建ToolsNode
    toolsNode := compose.NewToolsNode([]tool.Tool{
        searchTool,    // 搜索工具
        weatherTool,   // 天气查询工具
        calculatorTool, // 计算器工具
    })
    */

    // node_tool-0. 已创建 Info,InvokableRun (详情同上func_tool)
	// node_tool-1. 创建Tool 并绑定 ToolsNode 
    weatherTool := NewWeatherTool("高德 api key...")
    toolsNode, err := compose.NewToolNode(ctx, &compose.ToolsNodeConfig{
       Tools: []tool.BaseTool{weatherTool},
    })
/*
// run tools using `Invoke`
func (tn *ToolsNode) Invoke(ctx context.Context, input *schema.Message,
    opts ...ToolsNodeOption) ([]*schema.Message, error)
*/
    // node_tool-2. 绑定model
    weatherInfo, err := weatherTool.Info(ctx)
	toolCallingChatModel, err := model.WithTools([]*schema.ToolInfo{
		weatherInfo,
	})
    // node_tool-2.5. 绑定model且
    // 绑定prompt.FromMessages()后
    input, err := toolCallingChatModel.Generate(ctx, result)

    // node_tool-3. 编译运行(常规)
    // input := &schema.Message{}
    toolMessage, err := toolNode.Invoke(ctx, input)
}
```

