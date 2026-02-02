> ## MCP install
> 
> * [eino CREATE mcp-client,mcp-server](https://www.cloudwego.io/zh/docs/eino/ecosystem_integration/tool/tool_mcp/)
> * [eino CREATE mcp-tool And mcp-examples](https://github.com/cloudwego/eino-ext/blob/main/components/tool/mcp/examples/mcp.go)
> 
> ```go
> // mcpTool_Config
> go get github.com/cloudwego/eino-ext/components/tool/mcp@latest
> // MCP
> go get github.com/mark3labs/mcp-go
> ```
> ## MCP
> 
> ```go
> /*
> 1. mcp_server
> ->  // 1. CREATE mcp_server
> ->  // 2. CREATE And ADD mcpServer_TOOL
> ->  // 3. mcpServer_TOOL
> ->  // 4. mcpServer_TOOL_Handler
> ->  // 5. mcpServer_TOOL GET_API_DATA -- (如果有)
> 2. mcp_client
> ->  // 0. ctx
> ->  // 1. CREATE And INIT mcp_client
> ->  // 2. START mcp_client
> 3. main
> // GET mcp_tool
> ->  // 0. ctx
> ->  // 1. GET mcp_tool
> ->  // 2. USE mcp_tool
> */
> ```

> ### mcp_server
> 
> ```go
> // mcp_server\mcp_server.go
> package main
> import (
> 	"github.com/mark3labs/mcp-go/mcp"
> 	"github.com/mark3labs/mcp-go/server"
> )
> func main() {
> 	// home. NewMCPServer
> 	// LATEST_PROTOCOL_VERSION 使用最新协议版本
> 	mcpServer := server.NewMCPServer("weather", mcp.LATEST_PROTOCOL_VERSION)
> 	// 1. ADD mcpServer_TOOL-1
> 	tool := WeatherTool()
> 	mcpServer.AddTool(tool, WeatherToolHandler)
> 	// end. MCPServer Start
> 	err := server.NewSSEServer(mcpServer).Start("localhost:12345")
> }
> // 2. mcpServer_TOOL
> func WeatherTool() mcp.Tool {
> 	tool := mcp.NewTool("get_weather", // name
> 		mcp.WithDescription("描述"), // 设置工具描述
> 		mcp.WithString("data1", // 参数
> 			mcp.Required(), // Required() 表示参数必需（但有默认值）
> 			mcp.Enum("base", "all"), // Enum() 限制参数只能取"base"或"all"这两个值
> 			mcp.Description("返回数据类型，base为实况天气，all为预报天气"), // 设置参数描述 
> 			mcp.DefaultString("base"), // 设置默认值
> 		)
> 		// 添加第二个参数：返回数据类型,字符串
> 		// mcp.WithString("data2")
> 	)
> 	return tool
> }
> // 3. mcpServer_TOOL_Handler
> func WeatherToolHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
> 	// home. mcpTool_Handler request_GetArguments
> 	params := request.GetArguments()
> 	cityName, ok := params["city"].(string)
> 	daysStr, _ := params["days"].(string)
> 	// 1. GET_API_DATA/具体实现
> 	weatherResp, err := GetWeatherData(ctx, cityName, daysStr)
> 	// end. mcpTool_Handler return string
> 	weatherText := formatWeatherReport(cityName, weatherResp)
> 	return mcp.NewToolResultText(weatherText), nil
> }
> ```
> 
> #### mcpServer_TOOL-GET_API_DATA
> 
> ```go
> // mcp_server\apiTool_GetWeatherData.go> 
> // API例子
> // 请求方式 GET
> // URL := https://restapi.amap.com/v3/weather/weatherInfo?parameters
> 
> // parameters 代表的参数包括必填参数和可选参数。
> 
> // 请求参数
> // key 必填 缺省值(无)
> // city 必填 缺省值(无)
> // extensions 可选(base/all) 缺省值(无)
> // output 可选(JSON,XML) 缺省值(JSON)
> package main
> import (
> 	"context"
> 	"fmt"
> 	"io"
> 	"net/http"
> 	"net/url"
> )
> func GetWeatherData(ctx context.Context, cityName string, daysStr string) (*WeatherResponse, error) {
> 		// 1. 构建API请求URL
> 		baseURL := "https://restapi.amap.com/v3/weather/weatherInfo"
> 		queryParams := url.Values{}
> 		// 2. 设置参数
> 		queryParams.Set("key", "you api key")
> 		queryParams.Set("city", city)
> 		queryParams.Set("extensions", extensions)
> 		// 3. 设置返回格式为JSON
> 		queryParams.Set("output", "JSON")
> 		fullURL := fmt.Sprintf("%s?%s", baseURL, queryParams.Encode())
> 
> 		// 1. 发送HTTP请求
> 		// nil表示请求体为空（GET请求通常无请求体）
> 		req, err := http.NewRequestWithContext(ctx, "GET", fullURL, nil)
> 		// 2. 创建HTTP客户端实例
> 		client := &http.Client{}
> 		// 3. client.Do会发送请求并返回响应
> 		resp, err := client.Do(req)
> 		// 4. 使用 defer 确保响应体在函数返回前关闭
> 		defer resp.Body.Close()
> 		// 5. 读取响应
> 		body, err := io.ReadAll(resp.Body)
> 		// 6. 检查HTTP状态码
> 		if resp.StatusCode != http.StatusOK {
> 			return nil, fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
> 		}
> 		// 返回数据
> 		return &weatherResp, nil
> }
> ```

> ### mcp_client
> 
> ```go
> // ----------------------------------------
> // GET mcpServer_TOOL
> // ----------------------------------------
> // 	mcpTools, err := getMcpTools()
> // ----------------------------------------
> // mcp_client.go
> package main
> import (
> 	"context"
> 
> 	"github.com/cloudwego/eino/components/tool"
> 	mcpTool "github.com/cloudwego/eino-ext/components/tool/mcp"
> 	"github.com/mark3labs/mcp-go/client"
> 	"github.com/mark3labs/mcp-go/mcp"
> )
> 
> // 2. 连接到MCP服务器并获取工具
> func getMcpTools() ([]tool.BaseTool, error) {
> 	ctx := context.Background()
> 	// home. Create NewSSEMCPClient
> 	cli, err := client.NewSSEMCPClient("http://localhost:12345/sse")
> 
> 	// 1. Start_Client
> 	err = cli.Start(ctx)
> 
> 	// 2. client_Init
> 	initializeRequest := mcp.InitializeRequest{}
> 	initializeRequest.Params.ProtocolVersion = mcp.LATEST_PROTOCOL_VERSION // 使用最新协议版本
> 	initializeRequest.Params.ClientInfo = mcp.Implementation{
> 		Name:    "weather-tool", // 客户端名称
> 		Version: "0.0.1",        // 客户端版本
> 	}
> 	_, err = cli.Initialize(ctx, initializeRequest)
> 	
> 	// end. mcpTool_Config
> 	tools, err := mcpTool.GetTools(ctx, &mcpTool.Config{
> 		Cli: cli, // 传入已连接的MCP客户端
> 		// ToolNameList: []string{},
> 	})
> 	return tools, err
> }
> ```
> #### mcp_client main
> 
> ```go
> package main
> func main() {
> 	ctx := context.Background()
> 	// 1. GET mcp_tool
> 	mcpTools, err := GetMcpTools()
> 	if err != nil {
> 		panic(err)
> 	}
> 	// 2. USE mcp_tool
> 	chatAgent, err := adk.NewChatModelAgent(ctx, &adk.ChatModelAgentConfig{
> 		Name:        adk_AgentName,
> 		Description: adk_AgentDescription,
> 		Instruction: adk_AgentInstruction,
> 		Model:       chatModel, // chatModel
> 		ToolsConfig: adk.ToolsConfig{
> 			ToolsNodeConfig: compose.ToolsNodeConfig{
> 				Tools: mcpTools,
> 			},
> 		},
> 	})
> }
> ```
