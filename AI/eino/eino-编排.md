> ## 编排
> ```go
> // main.go
> /*
> ->  // 0. ctx
> ->  // 1. ChatTemplate
> ->  // 2. ChatModel
> ->  // 3. tool.InvokableTool
> ->  // 4. 绑定工具到模型
> ->  // 5. 创建工具节点
> ->  // 6. 开始编排
> */
> // 默认const
> const (
> 	ollamaBaseURL   = "http://localhost:11434"
> 	ollamaModelName = "qwen3:0.6b"
> )
> // 默认struct
> type userInfoRequest struct {
> 	Email string `json:"email"`
> 	Name  string `json:"name"`
> }
> type userInfoResponse struct {
> 	Name     string `json:"name"`
> 	Email    string `json:"email"`
> 	Company  string `json:"company"`
> 	Position string `json:"position"`
> 	Salary   string `json:"salary"`
> }
> ```

> ## home. node
> ```go
> // main.go
>  /* 
> --->  // 1. create an instance of ChatTemplate as 1st Graph Node
>  */ 
>     systemTpl := `你是一名房产经纪人，结合用户的薪酬和工作，使用 user_info API，为其提供相关的房产信息。邮箱是必须的`
>     chatTpl := prompt.FromMessages(schema.FString,
>        schema.SystemMessage(systemTpl),
>        schema.MessagesPlaceholder("message_histories", true),
>        schema.UserMessage("{user_query}"),
>     )
>  /* 
> --->  // 2. create an instance of ChatModel as 2nd Graph Node
>  */
> 	modelConf := &ollama.ChatModelConfig{
> 		Model:   ollamaModelName,
> 		BaseURL: ollamaBaseURL,
> 	}
> 	chatModel, err := ollama.NewChatModel(ctx, modelConf)
> 	if err != nil {
> 		panic(err)
> 	}
>  /* 
> --->  // 3. create an instance of tool.InvokableTool for Intent recognition and execution
>  */
>     userInfoTool := utils.NewTool(
>        &schema.ToolInfo{
>           Name: "user_info",
>           Desc: "根据用户的姓名和邮箱，查询用户的公司、职位、薪酬信息",
>           ParamsOneOf: schema.NewParamsOneOfByParams(map[string]*schema.ParameterInfo{
>              "name": {
>                 Type: "string",
>                 Desc: "用户的姓名",
>              },
>              "email": {
>                 Type: "string",
>                 Desc: "用户的邮箱",
>              },
>           }),
>        },
>        func(ctx context.Context, input *userInfoRequest) (output *userInfoResponse, err error) {
>           return &userInfoResponse{
>              Name:     input.Name,
>              Email:    input.Email,
>              Company:  "Bytedance",
>              Position: "CEO",
>              Salary:   "99999",
>           }, nil
>        })
>     info, err := userInfoTool.Info(ctx)
>     // 4. bind ToolInfo to ChatModel. ToolInfo will remain in effect until the next BindTools.
> 	// BindForcedTools -> BindTools (26.1.19)
>     err = chatModel.BindForcedTools([]*schema.ToolInfo{info})
>     // 5. create an instance of ToolsNode as 3rd Graph Node
>     toolsNode, err := compose.NewToolNode(ctx, &compose.ToolsNodeConfig{
>        Tools: []tool.BaseTool{userInfoTool},
>     })
> ```

> ## end. Graph-Add
> ```go
> 	const (
> 		promptNodeKey        = "prompt"
> 		chatNodeKey          = "chat"
> 		toolsNodeKey         = "tools"
> 		recommendChatNodeKey = "chat_recommend"
> 		lambdaNodeKey        = "lambda"
> 		lambdaPromptNodeKey  = "lambdaPrompt"
> 	)
> 	// 1-Graph. 创建Graph编排
> 	g := compose.NewGraph[map[string]any, *schema.Message]()
> 	// 2-Graph. 添加节点
> 	_ = g.AddChatTemplateNode(promptNodeKey, chatTpl)
> 	_ = g.AddChatModelNode(chatNodeKey, chatModel)
> 	_ = g.AddToolsNode(toolsNodeKey, toolsNode)
> 	_ = g.AddChatModelNode(recommendChatNodeKey, chatModel)
> 	_ = g.AddLambdaNode(lambdaNodeKey, lambda)
> 	_ = g.AddLambdaNode(lambdaPromptNodeKey, lambdaPrompt)
> 	// 3-Graph. 添加边 也就是节点之间的依赖关系
> 	_ = g.AddEdge(compose.START, promptNodeKey)
> 	_ = g.AddEdge(promptNodeKey, chatNodeKey)
> 	_ = g.AddEdge(chatNodeKey, toolsNodeKey)
> 	_ = g.AddEdge(toolsNodeKey, lambdaNodeKey)
> 	_ = g.AddEdge(lambdaNodeKey, lambdaPromptNodeKey)
> 	_ = g.AddEdge(lambdaPromptNodeKey, recommendChatNodeKey)
> 	_ = g.AddEdge(recommendChatNodeKey, compose.END)
> 	// 4-Graph. 编译运行
> 	r, err := g.Compile(ctx)
> 	if err != nil {
> 		panic(err)
> 	}
> 	output, err := r.Invoke(ctx, map[string]any{
> 		"message_histories": []*schema.Message{},
> 		"user_query":        "我叫 zhangsan, 邮箱是 zhangsan@bytedance.com, 帮我推荐一处房产",
> 	})
> 	// end. 内容输出
> 	println("=====================思考内容====================")
> 	if output.ReasoningContent != "" {
> 		println(output.ReasoningContent)
> 	}
> 	println("=========================================")
> 	if output.Content != "" {
> 		println(output.Content)
> 	}
> ```
> ## end. Chain-Add
> ```go
> 	const (
> 		promptNodeKey        = "prompt"
> 		chatNodeKey          = "chat"
> 		toolsNodeKey         = "tools"
> 		recommendChatNodeKey = "chat_recommend"
> 		lambdaNodeKey        = "lambda"
> 		lambdaPromptNodeKey  = "lambdaPrompt"
> 	)
> 	// 1-Chain. 创建Chain编排
> 	chain := compose.NewChain[map[string]any, *schema.Message]()
> 	// 2-Chain. 将节点添加到Chain中
> 	chain.
> 		AppendChatTemplate(chatTpl).
> 		AppendChatModel(chatModel).
> 		AppendToolsNode(toolsNode).
> 		AppendLambda(lambda).
> 		AppendLambda(lambdaPrompt).
> 		AppendChatModel(chatModel)
> 	// 3-Chain. 编译运行
> 	runnable, err := chain.Compile(ctx)
> 	if err != nil {
> 		panic(err)
> 	}
> 	output, err := runnable.Invoke(ctx, map[string]any{
> 		"histories":  []*schema.Message{},
> 		"user_query": "我叫 zhangsan, 邮箱是 zhangsan@bytedance.com, 帮我推荐一处房产",
> 	})
> ```
> 
> ## end. Workflow-Add
> ```go
> 	// 1-Workflow. 创建Workflow编排
> 	wf := compose.NewWorkflow[map[string]any, *schema.Message]()
> 	// 2-Workflow. 添加节点到Workflow
> 	wf.AddChatTemplateNode("prompt", chatTpl).AddInput(compose.START)
> 	wf.AddChatModelNode("chat", chatModel).AddInput("prompt")
> 	wf.AddToolsNode("tools", toolsNode).AddInput("chat")
> 	wf.AddLambdaNode("transform", lambda).AddInput("tools")
> 	wf.AddLambdaNode("prompt_transform", lambdaPrompt).AddInput("transform")
> 	wf.AddChatModelNode("chat_recommend", chatModel).AddInput("prompt_transform")
> 	wf.End().AddInput("chat_recommend")
> 	// 3-Workflow. 编译运行
> 	runnable, err := wf.Compile(ctx)
> 	if err != nil {
> 		panic(err)
> 	}
> 	output, err := runnable.Invoke(ctx, map[string]any{
> 		"histories":  []*schema.Message{},
> 		"user_query": "我叫 zhangsan, 邮箱是 zhangsan@bytedance.com, 帮我推荐一处房产",
> 	})
> ```

> ## end. 内容输出
> ```go
> 	// end. 内容输出
> 	println("=====================思考内容====================")
> 	if output.ReasoningContent != "" {
> 		println(output.ReasoningContent)
> 	}
> 	println("=========================================")
> 	if output.Content != "" {
> 		println(output.Content)
> 	}
> ```
