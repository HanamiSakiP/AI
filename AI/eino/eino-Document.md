> ## Document
> ```go
>  /*
> ->  // 0. ctx
> ->  // 1. Loader
> ->  // 2. Splitter
> ->  // 3. Embedding
> ->  // 4. Embedding_db Indexer
> ->  // 5. Embedding_db Retriever
>  */
> ```

> ### 1. Loader - local file
> ```go
> package main
> import (
>     "github.com/cloudwego/eino/components/document/loader/file"
> )
> func main() {
>     loader, err := file.NewFileLoader(ctx, &FileLoaderConfig{
>         UseNameAsID: true,                // 是否使用文件名作为文档ID
>         Parser:      &parser.TextParser{}, // 可选：指定自定义解析器
>     })
>     // 文档加载通过 Load 方法实现
>     docs, err := loader.Load(ctx, document.Source{
>         URI: "./path/to/document.txt",
>     })
> /*
> 文档加载后会自动添加以下元数据文档加载后会自动添加以下元数据：
> _file_name：文件名
> _extension：文件扩展名
> _source：文件的完整路径
> 注意事项：
> 路径必须指向一个文件，不能是目录
> 文件必须可读
> 如果 UseNameAsID 为 true，单文件时使用文件名作为 ID，多文档时使用 文件名_序号 作为 ID
> */
>     // 使用文档内容
>     for _, doc := range docs {
>         println(doc.Content)
>         // 访问元数据
>         fileName := doc.MetaData[file.MetaKeyFileName]
>         extension := doc.MetaData[file.MetaKeyExtension]
>         source := doc.MetaData[file.MetaKeySource]
>     }
> }
> ```
> 
> ### 2. Splitter - recursive
> ```go
> package main
> import (
>     "context"
>     
>     "github.com/cloudwego/eino-ext/components/document/transformer/splitter/recursive"
>     "github.com/cloudwego/eino/schema"
> )
> func main() {
>     ctx := context.Background()
>     // 初始化分割器
>     splitter, err := recursive.NewSplitter(ctx, &recursive.Config{
>         ChunkSize:    1000,           // 必需：目标片段大小
>         OverlapSize:  200,            // 可选：片段重叠大小
>         Separators:   []string{"\n", ".", "?", "!"}, // 可选：分隔符列表
>         LenFunc:      nil,            // 可选：自定义长度计算函数
>         KeepType:     recursive.KeepTypeNone, // 可选：分隔符保留策略
>     })
> /*
> 配置参数说明：
> ChunkSize：必需参数，指定目标片段的大小
> OverlapSize：片段之间的重叠大小，用于保持上下文连贯性
> Separators：分隔符列表，按优先级顺序使用
> LenFunc：自定义文本长度计算函数，默认使用 len()
> KeepType：分隔符保留策略，可选值：
> KeepTypeNone：不保留分隔符
> KeepTypeStart：在片段开始处保留分隔符
> KeepTypeEnd：在片段结尾处保留分隔符
> */
>     // 准备要分割的文档
>     docs := []*schema.Document{
>         {
>             ID: "doc1",
>             Content: `这是第一个段落，包含了一些内容。
>             这是第二个段落。这个段落有多个句子！这些句子通过标点符号分隔。
>             这是第三个段落。这里有更多的内容。`,
>         },
>     }
>     
>     // 执行分割
>     results, err := splitter.Transform(ctx, docs)
>     if err != nil {
>         panic(err)
>     }
>     
>     // 处理分割结果
>     for i, doc := range results {
>         println("片段", i+1, ":", doc.Content)
>     }
> }
> /*
> 高级用法
> 自定义长度计算：
> splitter, err := recursive.NewSplitter(ctx, &recursive.Config{
>     ChunkSize: 1000,
>     LenFunc: func(s string) int {
>         // eg: 使用 unicode 字符数而不是字节数
>         return len([]rune(s))
>     },
> })
> */
> /*
> 调整重叠策略：
> splitter, err := recursive.NewSplitter(ctx, &recursive.Config{
>     ChunkSize:   1000,
>     // 增大重叠区域以保持更多上下文
>     OverlapSize: 300,
>     // 在片段结尾保留分隔符
>     KeepType:    recursive.KeepTypeEnd,
> })
> */
> /*
> 自定义分隔符：
> splitter, err := recursive.NewSplitter(ctx, &recursive.Config{
>     ChunkSize: 1000,
>     // 按优先级排序的分隔符列表
>     Separators: []string{
>         "\n\n",     // 空行（段落分隔）
>         "\n",       // 换行
>         "。",       // 句号
>     },
> })
> */
> ```
> 
> ### 2. Splitter - markdown
> ```go
> package main
> import (
>     "context"
>     
>     "github.com/cloudwego/eino-ext/components/document/transformer/splitter/markdown"
>     "github.com/cloudwego/eino/schema"
> )
> func main() {
>     ctx := context.Background()
>     
>     // 初始化分割器
>     splitter, err := markdown.NewHeaderSplitter(ctx, &markdown.HeaderConfig{
>         Headers: map[string]string{
>             "#":   "h1", // 一级标题
>             "##":  "h2", // 二级标题
>             "###": "h3", // 三级标题
>         },
>         TrimHeaders: false, // 是否在输出中保留标题行
>     })
> /*
> 配置参数说明：
> Headers：必需参数，定义标题标记和对应的元数据键名映射
> TrimHeaders：是否在输出的内容中移除标题行
> */
>     if err != nil {
>         panic(err)
>     }
>     
>     // 准备要分割的文档
>     docs := []*schema.Document{
>         {
>             ID: "doc1",
>             Content: `# 文档标题
> 
> 这是介绍部分的内容。
> 
> ## 第一章
> 
> 这是第一章的内容。
> 
> ### 1.1 节
> 
> 这是 1.1 节的内容。
> 
> ## 第二章
> 
> 这是第二章的内容。
> 
> \`\`\`
> # 这是代码块中的注释，不会被识别为标题
> \`\`\`
> `,
>         },
>     }
>     
>     // 执行分割
>     results, err := splitter.Transform(ctx, docs)
>     if err != nil {
>         panic(err)
>     }
>     
>     // 处理分割结果
>     for i, doc := range results {
>         println("片段", i+1, ":", doc.Content)
>         println("标题层级：")
>         for k, v := range doc.MetaData {
>             if k == "h1" || k == "h2" || k == "h3" {
>                 println("  ", k, ":", v)
>             }
>         }
>     }
> }
> 
> ```

### 3. Embedding - Ollama
```go
package main
import (
	"context"
	"log"
	"os"
	"time"

	"github.com/cloudwego/eino-ext/components/embedding/ollama"
	"github.com/cloudwego/eino/components/embedding"
)
func main() {
	ctx := context.Background()
	baseURL := os.Getenv("OLLAMA_BASE_URL")
	if baseURL == "" {
		baseURL = "http://localhost:11434" // 默认本地
	}
	model := os.Getenv("OLLAMA_EMBED_MODEL")
	if model == "" {
		model = "nomic-embed-text"
	}

	embedder, err := ollama.NewEmbedder(ctx, &ollama.EmbeddingConfig{
		BaseURL: baseURL,
		Model:   model,
		Timeout: 10 * time.Second,
	})
/*
type EmbeddingConfig struct {
    // Timeout specifies the maximum duration to wait for API responses
    // If HTTPClient is set, Timeout will not be used.
    // Optional. Default: no timeout
    Timeout time.Duration `json:"timeout"`
    
    // HTTPClient specifies the client to send HTTP requests.
    // If HTTPClient is set, Timeout will not be used.
    // Optional. Default &http.Client{Timeout: Timeout}
    HTTPClient *http.Client `json:"http_client"`
    
    // BaseURL specifies the Ollama service endpoint URL
    // Format: http(s)://host:port
    // Optional. Default: "http://localhost:11434"
    BaseURL string `json:"base_url"`
    
    // Model specifies the ID of the model to use for embedding generation
    // Required. You can also set it when calling the EmbedStrings with `embedding.WithModel(model)`
    Model string `json:"model"`
    
    // Truncate specifies whether to truncate text to model's maximum context length
    // When set to true, if text to embed exceeds the model's maximum context length,
    // a call to EmbedStrings will return an error
    // Optional.
    Truncate *bool `json:"truncate,omitempty"`
    
    // KeepAlive controls how long the model will stay loaded in memory following this request.
    // Optional. Default 5 minutes
    KeepAlive *time.Duration `json:"keep_alive,omitempty"`
    
    // Options lists model-specific options.
    // Optional
    Options map[string]any `json:"options,omitempty"`
}
*/
	if err != nil {
		log.Fatalf("NewEmbedder of ollama error: %v", err)
		return
	}

	log.Printf("===== call Embedder directly =====")

	vectors, err := embedder.EmbedStrings(ctx, []string{"hello", "how are you"})
	if err != nil {
		log.Fatalf("EmbedStrings of Ollama failed, err=%v", err)
	}

	log.Printf("vectors : %v", vectors)

	// you can use WithModel to specify the model
	vectors, err = embedder.EmbedStrings(ctx, []string{"hello", "how are you"}, embedding.WithModel(model))
	if err != nil {
		log.Fatalf("EmbedStrings of Ollama failed, err=%v", err)
	}

	log.Printf("vectors : %v", vectors)
}
```

> ### 4. Embedding - Indexer
> ```go
>     // 1. NewEmbedder
> 	indexer, err := ri.NewIndexer(ctx, &ri.IndexerConfig{
> 		Client:    rdb,
> 		KeyPrefix: redisKeyPrefix,
> 		Embedding: embedder,
> 	})
>     // 2. Indexer storage
>     ids, err := indexer.Store(ctx, splitDocs)
> ```
> 
> ### 5. Embedding - Retriever
> ```go
> 	// 1. NewRetriever-Redis
> 	retriever, err := rr.NewRetriever(ctx, &rr.RetrieverConfig{
> 		Client:    rdb,
> 		Index:     redisIndexName,
> 		Embedding: embedder,
> 		TopK:      10,
> 	})
> 	// 2. Retrieve Docs
> 	retrievedDocs, err := retriever.Retrieve(ctx, question)
> ```
