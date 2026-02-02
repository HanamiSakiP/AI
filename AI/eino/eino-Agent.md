> ## flow_integration ReAct-Agent
> ```go
> /*
> // main
> ->  // 0. ctx
> ->  // 1. create ChatModel
> ->  // 2. 创建工具
> ->  // 3. 创建ReAct Agent
> ->  // 4. 使用Agent处理用户请求
> ->  // 5. 输出内容
> */
> ```
> ## flow_integration Multi-Agent
> ```go
> // main
> /*
> ->  // 0. ctx
> ->  // 1. 创建Host和专家Agents
> ->  // 2. 创建Multi-Agent系统
> // 创建Host Agent
> // 创建写日记专家
> // 创建读日记专家
> */
> ```


> ## flow_integration ReAct-Agent example
> ```go
> /*
> --->  // 1. 创建模型
> */
> 	model, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
> 		BaseURL: "http://localhost:11434",
> 		Model:   "modelscope.cn/Qwen/Qwen3-32B-GGUF:latest",
> 	})
> /*
> --->  // 2. 创建工具
> */
> 	userInfoTool := utils.NewTool(
> 		&schema.ToolInfo{
> 			Name: "user_info",
> 			Desc: "根据用户的姓名和邮箱，查询用户的公司、职位、薪酬信息，薪酬是月薪，单位人民币",
> 			ParamsOneOf: schema.NewParamsOneOfByParams(map[string]*schema.ParameterInfo{
> 				"name": {
> 					Type: "string",
> 					Desc: "用户的姓名",
> 				},
> 				"email": {
> 					Type: "string",
> 					Desc: "用户的邮箱",
> 				},
> 			}),
> 		},
> 		func(ctx context.Context, input *userInfoRequest) (output *userInfoResponse, err error) {
> 			// 模拟从数据库或其他服务获取用户信息
> 			return &userInfoResponse{
> 				Name:     input.Name,
> 				Email:    input.Email,
> 				Company:  "字节跳动",
> 				Position: "高级工程师",
> 				Salary:   "60000",
> 			}, nil
> 		})
> /*
> --->  // 3. 创建ReAct Agent
> */
> 	agent, err := react.NewAgent(ctx, &react.AgentConfig{
> 		ToolCallingModel: model,
> 		ToolsConfig: compose.ToolsNodeConfig{
> 			Tools: []tool.BaseTool{userInfoTool},
> 		},
> 		MessageModifier: func(ctx context.Context, input []*schema.Message) []*schema.Message {
> 			res := make([]*schema.Message, 0, len(input)+1)
> 			res = append(res, schema.SystemMessage(`你是一名元神高手`))
> 			res = append(res, input...)
> 			return res
> 		},
> 	})
> /*
> --->  // 4. 使用Agent处理用户请求
> */
> 	result, err := agent.Generate(ctx, []*schema.Message{
> 		schema.UserMessage("我叫 zhangsan, 邮箱是 zhangsan@bytedance.com, 帮我推荐一处房产，用中文回答问题"),
> 	})
> 	fmt.Println("Agent回答:", result.Content)
> 
> // 定义工具的输入输出结构
> type userInfoRequest struct {
> 	Name  string `json:"name"`
> 	Email string `json:"email"`
> }
> 
> type userInfoResponse struct {
> 	Name     string `json:"name"`
> 	Email    string `json:"email"`
> 	Company  string `json:"company"`
> 	Position string `json:"position"`
> 	Salary   string `json:"salary"`
> }
> ```
> 
> ## flow_integration Multi-Agent example
> ```go
> // main.go
> /*
> --->	// 1. 创建Host和专家Agents
> */
> 	h, err := newHost(ctx)
> 	writer, err := newWriteJournalSpecialist(ctx)
> 	reader, err := newReadJournalSpecialist(ctx)
> /*
> ---> 	// 2. 创建Multi-Agent系统
> */
> 	hostMA, err := host.NewMultiAgent(ctx, &host.MultiAgentConfig{
> 		Host: *h,
> 		Specialists: []*host.Specialist{
> 			writer,
> 			reader,
> 		},
> 	})
> 
> // 创建Host Agent
> func newHost(ctx context.Context) (*host.Host, error) {
> 	chatModel, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
> 		BaseURL: ollamaBaseURL,
> 		Model:   ollamaModelName,
> 	})
> 	return &host.Host{
> 		ToolCallingModel: chatModel,
> 		SystemPrompt:     "你是一个日记助手，可以帮助用户写日记、读日记。调用提供的",
> 	}, nil
> }
> // 创建写日记专家
> func newWriteJournalSpecialist(ctx context.Context) (*host.Specialist, error) {
> 	chatModel, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
> 		BaseURL: ollamaBaseURL,
> 		Model:   ollamaModelName,
> 	})
> 	return &host.Specialist{
> 		ChatModel:    chatModel,
> 		SystemPrompt: "请将用户输入的内容写入日记。请勿返回任何内容。",
> 		// Specialist特有
> 		AgentMeta: host.AgentMeta{
> 			Name:        "write_journal",
> 			IntendedUse: "将用户输入的内容写入日记",
> 		},
> 		Invokable: func(ctx context.Context, input []*schema.Message, opts ...agent.AgentOption) (*schema.Message, error) {
> 			// 不同
> 			return &schema.Message{
> 				Role:    schema.Assistant,
> 				Content: "日记已保存",
> 			}, nil
> 		},
> 		// 不同 返回输出
> 		Streamable: func(ctx context.Context, input []*schema.Message, opts ...agent.AgentOption) (*schema.StreamReader[*schema.Message],  error) {
> 			// 返回输出具体实现
> 			return &schema.StreamReader[*schema.Message]{}, nil
> 		},
> 	}, nil
> }
> 
> // 创建读日记专家
> func newReadJournalSpecialist(ctx context.Context) (*host.Specialist, error) {
> 	// 同上
> 	return &host.Specialist{
> 		// 同上
> 		// 返回输出
> 		Streamable: func(ctx context.Context, input []*schema.Message, opts ...agent.AgentOption) (*schema.StreamReader[*schema.Message], error) {
> 			// 略有不同 固定格式
> 			journal, err := readJournal()
> 			if err != nil {
> 				return nil, err
> 			}
> 			reader, writer := schema.Pipe[*schema.Message](0)
> 			go func() {
> 				scanner := bufio.NewScanner(journal)
> 				scanner.Split(bufio.ScanLines)
> 
> 				for scanner.Scan() {
> 					line := scanner.Text()
> 					message := &schema.Message{
> 						Role:    schema.Assistant,
> 						Content: line + "\n",
> 					}
> 					writer.Send(message, nil)
> 				}
> 
> 				if err := scanner.Err(); err != nil {
> 					writer.Send(nil, err)
> 				}
> 
> 				writer.Close()
> 			}()
> 
> 			return reader, nil
> 		},
> 	}, nil
> }
> ```

> ## adk_Agent
> ```go
> 	// 1. NewChatModel
> 	chatModel, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
> 		BaseURL: chatModelBaseURL,
> 		Model:   ollamaChatModelName,
> 	})
> 	// adk NewChatModelAgent
> 	chatAgent, err := adk.NewChatModelAgent(ctx, &adk.ChatModelAgentConfig{
> 		Name:        adk_AgentName,
> 		Description: adk_AgentDescription,
> 		Instruction: adk_AgentInstruction,
> 		Model:       chatModel,
> 		ToolsConfig: adk.ToolsConfig{
> 			ToolsNodeConfig: compose.ToolsNodeConfig{
> 				Tools: mcpTools(),
> 			},
> 		},
> 	})
> ```
> 
> ## adk_Agent-Supervisor
> ```go
> func main() {
> 	// 1. NewChatModel
> 	chatModel, err := ollama.NewChatModel(ctx, &ollama.ChatModelConfig{
> 		BaseURL: chatModelBaseURL,
> 		Model:   ollamaChatModelName,
> 	})
> 	// 2. 创建子 Agent 和 Supervisor
> 	weatherchAgent := NewWeatherchAgent(chatModel)
> 	reportSupervisor := NewReportSupervisor(chatModel)
> 	// 3. 组合 Supervisor 与子 Agent
> 	supervisorAgent, _ := supervisor.New(ctx, &supervisor.Config{
> 		Supervisor: reportSupervisor,
> 		SubAgents:  []adk.Agent{weatherchAgent},
> 	})
> }
> // 调研 Agent：生成研究计划
> func NewWeatherchAgent(model model.ToolCallingChatModel) adk.Agent {
> 	// Get McpTools
> 	mcpTools, err := GetMcpTools()
> 	if err != nil {
> 		panic(err)
> 	}
> 	agent, _ := adk.NewChatModelAgent(context.Background(), &adk.ChatModelAgentConfig{
> 		Name:        adk_AgentName,
> 		Description: adk_AgentDescription,
> 		Instruction: adk_AgentInstruction,
> 		Model:       model,
> 		ToolsConfig: adk.ToolsConfig{
> 			ToolsNodeConfig: compose.ToolsNodeConfig{
> 				Tools: mcpTools,
> 			},
> 		},
> 	})
> 	return agent
> }
> 
> // Supervisor Agent：协调调研和撰写任务
> func NewReportSupervisor(model model.ToolCallingChatModel) adk.Agent {
> 	agent, _ := adk.NewChatModelAgent(context.Background(), &adk.ChatModelAgentConfig{
> 		Name:        "ReportSupervisor",
> 		Description: "ReportSupervisor agent.",
> 		Instruction: "请根据子agent的工具进行调用",
> 		Model:       model,
> 	})
> 	return agent
> }
> ```
