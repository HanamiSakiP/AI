#### 流程
```go
->  // 0. ctx
```

#### 类型设置
```go
// 常量
const (
	knowledgeFilePath  = "./md"
	embeddingModelName = "embeddinggemma:300m"
	ollamaBaseURL      = "http://localhost:11434"
	chatModelName      = "qwen3:0.6b"
	openaiBaseURL      = "https://api.deepseek.com"
	openModelName      = "deepseek-chat"
	openaiAPIKey      = "key"
)
// 结构体
type userInfoRequest struct {
	Email string `json:"email"`
	Name  string `json:"name"`
	CurrentWeather       struct {
		Weathercode   int     `json:"weathercode"`
		IsDay         int     `json:"is_day"`
		Time          string  `json:"time"`
	} `json:"current_weather"`
}
```

#### err处理
```go
 	// 如果创建失败，终止程序
	if err != nil {
		panic(err)
	}
	// 如果初始化失败，返回错误
	if err != nil {
		return nil, err
	}
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
```

#### 非err处理
```go
	if !ok || cityName == "" {
		return nil, fmt.Errorf("city is required")
	}
```