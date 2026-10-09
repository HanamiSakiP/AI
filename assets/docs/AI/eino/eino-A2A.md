> ## A2A install
> ```bash
> // eino
> go get github.com/cloudwego/eino
> // A2A
> go get github.com/cloudwego/eino-ext/a2a
> // SSE
> go get github.com/cloudwego/hertz
> ```
> ## A2A
> ```go
> /*
> 1. A2A_server
> ->  // 0. ctx
> ->  // 1. Create A2A_server
> ->  // 2. Create adk_Agent And Register A2A_Server
> 2. A2A_Client
> ->  // 0. ctx
> ->  // 1. A2A_Client
> */
> ```

> ### A2A_Server
> ```go
> package main
> import (
> 	"context"
> 
> 	"github.com/cloudwego/eino-ext/a2a/extension/eino"
> 	"github.com/cloudwego/eino-ext/a2a/transport/jsonrpc"
> 	"github.com/cloudwego/eino-ext/components/model/ollama"
> 	"github.com/cloudwego/eino/adk"
> 	"github.com/cloudwego/eino/compose"
> 	hertzServer "github.com/cloudwego/hertz/pkg/app/server"
> )
> const (
> 	chatModelBaseURL     = "http://localhost:11434"
> 	ollamaChatModelName  = "qwen3-vl:2b"
> 	adk_AgentName        = "WeatherTool-recommender"
> 	adk_AgentDescription = "A WeatherTool recommender agent"
> 	adk_AgentInstruction = "请根据提供的天气查询工具，查询天气情况."
> )
> func main() {
> 	ctx := context.Background()
> 	// home. Create A2A_server
> 	h := hertzServer.Default()
> 	r, err := jsonrpc.NewRegistrar(ctx, &jsonrpc.ServerConfig{
> 		Router:      h,
> 		HandlerPath: "/a2a",
> 	})
> 	if err != nil {
> 		panic(err)
> 	}
> 
> 	// 1. NewChatModel
> 	chatModel, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
> 		BaseURL: chatModelBaseURL,
> 		Model:   ollamaChatModelName,
> 	})
> 	// 2. Get McpTools
> 	mcpTools, err := GetMcpTools()
> 	if err != nil {
> 		panic(err)
> 	}
> 	// 3. adk_Agent
> 	chatAgent, err := adk.NewChatModelAgent(ctx, &adk.ChatModelAgentConfig{
> 		Name:        adk_AgentName,
> 		Description: adk_AgentDescription,
> 		Instruction: adk_AgentInstruction,
> 		Model:       chatModel,
> 		ToolsConfig: adk.ToolsConfig{
> 			ToolsNodeConfig: compose.ToolsNodeConfig{
> 				Tools: mcpTools,
> 			},
> 		},
> 	})
> 	if err != nil {
> 		panic(err)
> 	}
> 	// end. Register A2A Server
> 	err = eino.RegisterServerHandlers(ctx, chatAgent, &eino.ServerConfig{
> 		Registrar: r,
> 	})
> 	if err != nil {
> 		panic(err)
> 	}
> 	err = h.Run()
> 	if err != nil {
> 		panic(err)
> 	}
> }
> ```

> ### A2A_Client
> ```go
> package main
> import (
> 	"bufio"
> 	"context"
> 	"fmt"
> 	"os"
> 	"strings"
> 
> 	"github.com/cloudwego/eino-ext/a2a/client"
> 	"github.com/cloudwego/eino-ext/a2a/extension/eino"
> 	"github.com/cloudwego/eino-ext/a2a/transport/jsonrpc"
> 	"github.com/cloudwego/eino/adk"
> 	"github.com/cloudwego/eino/schema"
> )
> func main() {
> 	// home. Create A2A_client
> 	t, err := jsonrpc.NewTransport(ctx, &jsonrpc.ClientConfig{
> 		BaseURL:     "http://127.0.0.1:8888",
> 		HandlerPath: "/a2a",
> 	})
> 	if err != nil {
> 		panic(err)
> 	}
> 	// 1. NewA2AClient
> 	aClient, err := client.NewA2AClient(ctx, &client.Config{
> 		Transport: t,
> 	})
> 	// 2. Create adk_Agent
> 	streaming := true
> 	a, err := eino.NewAgent(ctx, eino.AgentConfig{
> 		Client:    aClient,
> 		Streaming: &streaming,
> 	})
> 	// 3. adk_Agent NewRunner
> 	runner := adk.NewRunner(ctx, adk.RunnerConfig{
> 		Agent:           a,
> 		EnableStreaming: true,
> 	})
> 	// end. adk_Agent Run
> 	run := runner.Run(ctx, []adk.Message{
> 		schema.UserMessage("recommend a fiction book to me"),
> 	})
> }
> ```
> 
> #### adk_Agent Run
> ```go
> 	// end. adk_Agent Run
> 	for {
> 		next, b := run.Next()
> 		if !b {
> 			break
> 		}
> 		printEvent(next)
> 	}
> func printEvent(event *adk.AgentEvent) {
> 	fmt.Printf("name: %s\npath: %s \n", event.AgentName, event.RunPath)
> 	fmt.Printf("output: %v\n", event.Output.MessageOutput.Message.Content)
> }
> ```
