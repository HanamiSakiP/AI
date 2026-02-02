> # RAG install
> ```go
> // home. fileLoader
> go get github.com/cloudwego/eino-ext/components/document/loader/file
> // word
> go get github.com/cloudwego/eino-ext/components/document/parser/docx
> // urlloader
> go get github.com/cloudwego/eino-ext/components/document/loader/url
> // 1. splitter
> go get github.com/cloudwego/eino-ext/components/document/transformer/splitter/markdown
> go get github.com/cloudwego/eino-ext/components/document/transformer/splitter/recursive
> go get github.com/cloudwego/eino-ext/components/document/transformer/splitter/html
> go get github.com/cloudwego/eino-ext/components/document/transformer/splitter/semantic
> // 2. embedding
> go get github.com/cloudwego/eino-ext/components/embedding/ollama
> // 3. db_client
> go get github.com/redis/go-redis/v9
> go get -u github.com/milvus-io/milvus/client/v2
> // 4. db_indexer
> go get github.com/cloudwego/eino-ext/components/indexer/redis
> go get github.com/cloudwego/eino-ext/components/indexer/milvus2
> // 5. db_retriever
> go get github.com/cloudwego/eino-ext/components/retriever/redis
> go get github.com/cloudwego/eino-ext/components/retriever/milvus2
> ```
> ## RAG
> ```go
> /*
> ->  // 1. ctx
> ->  // 2. redis
> ->  // 3. indexer_redis(ctx, rdb)
> ->  // 4. userQuestion
> ->  // 5. retriever_redis(ctx, rdb, userQuestion)
> */
> // func name(dataName type) return error
> // (ctx context.Context, db *db.Client) error {}
> // func prepareKnowledge(ctx context.Context, rdb *redis.Client) error {}
> 1. indexer_redis(ctx, rdb)
>     // home. Check indexer
> 	createRedisIndexIfNotExists(ctx, rdb)
> 	// 1. NewFileLoader
> 	// 2. loader file
> 	// 3. NewSplitter_recursive And splitter
> 	// 4. NewEmbedder
> 	// end. NewIndexer And Indexer storage
> createRedisIndexIfNotExists(ctx, rdb)
> 	// 固定模板
> 2. retriever_redis(ctx, rdb, userQuestion)
> 	// home. NewEmbedder
> 	// 1. NewRetriever-Redis
> 	// 2. Retrieve Docs
> 	// end. Print Retrieve Docs
> ```

> ### RAG_indexer_redis
> ```go
> func indexer_redis(ctx context.Context, rdb *redis.Client) error {
> 	// home. Check indexer (Redis/Milvus)是否存在，不存在则创建
> 	if err := createRedisIndexIfNotExists(ctx, rdb); err != nil {
> 		return err
> 	}
> 
> 	// 1. NewFileLoader
> 	loader, err := file.NewFileLoader(ctx, &file.FileLoaderConfig{
> 		UseNameAsID: true, // 多文档时使用"文件名_序号"作为ID
> 	})
> 	if err != nil {
> 		return err
> 	}
> 
> 	// 2. 读取目录下所有文件
> 	var allDocs []*schema.Document
> 	// 遍历目录
> 	err = filepath.Walk(knowledgeDirPath, func(path string, info os.FileInfo, err error) error {
> 		if err != nil {
> 			return err
> 		}
> 		// 跳过目录，只处理文件
> 		if info.IsDir() {
> 			return nil
> 		}
> 		// 可以在这里添加文件类型过滤
> 		ext := strings.ToLower(filepath.Ext(path))
> 		// 例如：只处理.txt和.md文件
> 		if ext != ".txt" && ext != ".md" {
> 			return nil
> 		}
> 		log.Printf("正在加载文件: %s", path)
> 
> 		// 2. Load file
> 		docs, err := loader.Load(ctx, document.Source{
> 			URI: path,
> 		})
> 		if err != nil {
> 			log.Printf("加载文件失败 %s: %v", path, err)
> 			return nil // 跳过无法加载的文件
> 		}
> 
> 		// 显示元数据信息
> 		for i, doc := range docs {
> 			log.Printf("  文档 %d:", i+1)
> 			log.Printf("    ID: %s", doc.ID)
> 			log.Printf("    文件名: %v", doc.MetaData[file.MetaKeyFileName])
> 			log.Printf("    扩展名: %v", doc.MetaData[file.MetaKeyExtension])
> 			log.Printf("    源路径: %v", doc.MetaData[file.MetaKeySource])
> 		}
> 
> 		allDocs = append(allDocs, docs...)
> 		return nil
> 	})
> 	if err != nil {
> 		return fmt.Errorf("遍历目录失败: %w", err)
> 	}
> 	if len(allDocs) == 0 {
> 		return fmt.Errorf("目录中没有找到可用的文件")
> 	}
> 	log.Printf("总共加载了 %d 个文档片段", len(allDocs))
> 
> 	// 3. NewSplitter_recursive And splitter
> 	splitter, err := recursive.NewSplitter(ctx, &recursive.Config{
> 		ChunkSize:   1000,
> 		OverlapSize: 200,
> 		Separators:  []string{"\n\n", "\n", "。", "！", "？"},
> 		KeepType:    recursive.KeepTypeEnd,
> 	})
> 	// 3. NewSplitter_markdown
> 	// splitter, err := markdown.NewHeaderSplitter(ctx, &markdown.HeaderConfig{
> 	// 	Headers: map[string]string{
> 	// 		"#":    "h1",
> 	// 		"##":   "h2",
> 	// 		"###":  "h3",
> 	// 		"####": "h4",
> 	// 	},
> 	// 	TrimHeaders: md_biaoti, // 是否在输出的内容中移除标题行
> 	// })
> 	if err != nil {
> 		return err
> 	}
> 	splitDocs, err := splitter.Transform(ctx, allDocs)
> 	if err != nil {
> 		return err
> 	}
> 	log.Printf("分割后得到 %d 个文档片段", len(splitDocs))
> 
> 	// 4. NewEmbedder
> 	embedder, err := ollama.NewEmbedder(ctx, &ollama.EmbeddingConfig{
> 		Model:   embeddingModelName,
> 		BaseURL: ollamaBaseURL,
> 	})
> 	if err != nil {
> 		return err
> 	}
> 
> 	// end. NewIndexer And Indexer storage
> 	indexer, err := ri.NewIndexer(ctx, &ri.IndexerConfig{
> 		Client:    rdb,
> 		KeyPrefix: redisKeyPrefix,
> 		Embedding: embedder,
> 	})
> 	if err != nil {
> 		return err
> 	}
> 	ids, err := indexer.Store(ctx, splitDocs)
> 	if err != nil {
> 		return err
> 	}
> 	log.Printf("成功存储了 %d 个文档片段到索引", len(ids))
> 	return nil
> }
> ```

> #### RAG_indexer_redis Check_indexer
> ```go
> func createRedisIndexIfNotExists(ctx context.Context, rdb *redis.Client) error {
> 	indices, err := rdb.Do(ctx, "FT._LIST").StringSlice()
> 	if err != nil {
> 		return err
> 	}
> 	for _, v := range indices {
> 		if v == redisIndexName {
> 			return nil
> 		}
> 	}
> 	_, err = rdb.FTCreate(ctx, redisIndexName, &redis.FTCreateOptions{
> 		OnHash: true,
> 		Prefix: []any{redisKeyPrefix},
> 	}, &redis.FieldSchema{FieldName: "content", FieldType: redis.SearchFieldTypeText},
> 		&redis.FieldSchema{
> 			FieldName: "vector_content",
> 			FieldType: redis.SearchFieldTypeVector,
> 			VectorArgs: &redis.FTVectorArgs{
> 				FlatOptions: &redis.FTFlatOptions{
> 					Type:           "FLOAT64",
> 					Dim:            384,
> 					DistanceMetric: "L2",
> 				},
> 			},
> 		},
> 	).Result()
> 	if err != nil {
> 		return err
> 	}
> 	return nil
> }
> ```

> ### RAG_retriever_redis
> ```go
> func retriever_redis(ctx context.Context, rdb *redis.Client, question string) error {
> 	// home. NewEmbedder
> 	embedder, err := ollama.NewEmbedder(ctx, &ollama.EmbeddingConfig{
> 		Model:   embeddingModelName,
> 		BaseURL: ollamaBaseURL,
> 	})
> 	if err != nil {
> 		return err
> 	}
> 	// 1. NewRetriever-Redis
> 	retriever, err := rr.NewRetriever(ctx, &rr.RetrieverConfig{
> 		Client:    rdb,
> 		Index:     redisIndexName,
> 		Embedding: embedder,
> 		TopK:      10,
> 	})
> 	// NewRetriever-milvus2
> 	// retriever, err := milvus2.NewRetriever(ctx, &milvus2.RetrieverConfig{
> 	//     ClientConfig: &milvusclient.ClientConfig{
> 	//             Address:  addr,
> 	//             Username: username,
> 	//             Password: password,
> 	//     },
> 	//     Collection: "my_collection", // 集合名称
> 	//     TopK:       10, // 返回结果数量
> 	//     SearchMode: search_mode.NewApproximate(milvus2.COSINE), // 	搜索策略（必需）
> 	//     Embedding:  embedder, // 用于查询向量化的 Embedder（必需）
> 	// })
> 	if err != nil {
> 		return err
> 	}
> 	// 2. Retrieve Docs
> 	retrievedDocs, err := retriever.Retrieve(ctx, question)
> 	if err != nil {
> 		return err
> 	}
> 	if len(retrievedDocs) == 0 {
> 		log.Println("未能从知识库中找到相关信息。")
> 		return nil
> 	}
> 	// end. Print Retrieve Docs
> 	if err := retriever_redis_fz_Chain(ctx, question, retrievedDocs); err != nil {
> 		return err
> 	}
> 	return nil
> }
> ```
> 
> #### RAG_retriever_redis_fz_Chain
> ```go
> func retriever_redis_fz_Chain(ctx context.Context, question string, retrievedDocs []*schema.Document) error {
> 	// 1. create an instance of ChatTemplate as 1st Graph Node
> 	systemTpl := ragPrompt
> 	ragTemplate := prompt.FromMessages(schema.FString,
> 		schema.SystemMessage(systemTpl),
> 		schema.MessagesPlaceholder("message_histories", true),
> 		schema.UserMessage("{question}"),
> 	)
> 	// 2. create an instance of ChatModel as 2nd Graph Node
> 	modelConf := &ollama2.ChatModelConfig{
> 		Model:   chatModelName,
> 		BaseURL: ollamaBaseURL,
> 	}
> 	chatModel, err := ollama2.NewChatModel(ctx, modelConf)
> 	if err != nil {
> 		panic(err)
> 	}
> 	// home. Chain_NewChain
> 	chain := compose.NewChain[map[string]any, *schema.Message]()
> 	// 1. Chain_Add_Node
> 	chain.
> 		AppendChatTemplate(ragTemplate).
> 		AppendChatModel(chatModel)
> 	// 2. Chain_Run
> 	runnable, err := chain.Compile(ctx)
> 	if err != nil {
> 		panic(err)
> 	}
> 
> 	// DATA retrievedDocs
> 	var contextBuilder strings.Builder
> 	for i, doc := range retrievedDocs {
> 		log.Printf("  - 相关片段 %d: %s\n", i+1, strings.ReplaceAll(doc.Content, "\n", " "))
> 		// 显示来源文件的元数据
> 		if fileName, ok := doc.MetaData[file.MetaKeyFileName]; ok {
> 			log.Printf("    来源文件: %v", fileName)
> 		}
> 		contextBuilder.WriteString(doc.Content)
> 		contextBuilder.WriteString("\n\n")
> 	}
> 	var vars = map[string]any{
> 		"message_histories": []*schema.Message{},
> 		"question":          question,
> 		"context":           contextBuilder.String(),
> 	}
> 
> 	// 2. Chain_Run_output
> 	output, err := runnable.Invoke(ctx, vars)
> 	if err != nil {
> 		return err
> 	}
> 
> 	// end. Graph_output
> 	println("=====================思考内容====================")
> 	if output.ReasoningContent != "" {
> 		println(output.ReasoningContent)
> 	}
> 	println("==================RAG输出=======================")
> 	if output.Content != "" {
> 		println(output.Content)
> 	}
> 
> 	return nil
> }
> ```
