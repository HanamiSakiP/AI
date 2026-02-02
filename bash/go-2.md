# go-gin-grom

> ## 0. 基础知识
> test/test.go
> ```go
> # test.go
> # 导包
> package test
> 
> import (
> 
> )
> ```
> ```bash
> web 知识点
> # 前端  -> API层  -> Service层  -> Data Access 层  -> 数据库
> -> utils -> controllers
> -> middlewares -> router 
> -> models -> global-> config
> # 项目结构
> go-gin-grom/
> ├── config/  # 配置项
> │     └── config.go
> │     └── config.yml
> │     └── db.go
> │     └── redis.go
> └── models
> │     └── user.go
> └── global
> │     └── global.go
> └── controllers
> │     └── test_controller.go
> └── utils
> │     └── utils.go
> └── router
> │     └── router.go
> └── middlewares
>     └───── auth_middleware.go
> ```


> ## 1. 基础配置（数据库连接）-gorm
> config/config.go
> ```go
> # config/config.go
> package config
> 
> import (
> 	"log"
> 
> 	"github.com/spf13/viper"
> )
> 
> type Config struct {
> 	App struct {
> 		Name string
> 		Port string
> 	}
> 	Database struct {
> 		Dsn string
> 		MaxIdleConns int
> 		MaxOpenConns int
> 	}
> 	Redis struct{
> 		Addr string
> 		DB int
> 		Password string
> 	}
> }
> 
> // 全局配置指针，程序启动后会被 InitConfig 初始化
> var AppConfig *Config
> 
> func InitConfig() {
> 	// 将配置文件名设置为 "config"（不含扩展名）
> 	viper.SetConfigName("config")
> 	// 指定配置文件格式为 YAML
> 	viper.SetConfigType("yml")
> 	// 添加查找配置文件的路径
> 	viper.AddConfigPath("./config")
> 
> 	// 读取配置文件并检查错误；若读取失败则记录致命日志并退出程序
> 	if err := viper.ReadInConfig(); err !=nil{
> 		log.Fatalf("Error reading config file: %v", err)
> 	}
> 	
> 	// 为全局配置分配内存（实例化）
> 	AppConfig = &Config{}
> 	
> 	// 读取到的配置解码（反序列化）到 AppConfig 结构体；若失败则记录致命日志并退出
> 	if err:= viper.Unmarshal(AppConfig); err !=nil{
> 		log.Fatalf("Unable to decode into struct: %v", err)
> 	}
> 
> 	// 初始化数据库连接（调用自定义函数）
> 	initDB()
> 	initRedis()
> }
> ```

> config/config.yml
> ```yml
> # config/config.yml
> app:
>   name: test
>   port: :1145
>   
> database:
>   dsn: root:密码@tcp(127.0.0.1:3306)/库名?charset=utf8mb4&parseTime=True&loc=Local
>   MaxIdleConns: 11
>   MaxOpenCons: 114
> 
> redis:
>   addr: localhost:6379
>   DB: 0
>   Password: ""
> ```

> config/db.go
> ```go
> # config/db.go
> package config
> 
> import (
> 	"test/global"
> 	"log"
> 	"time"
> 
> 	"gorm.io/driver/mysql"
> 	"gorm.io/gorm"
> )
> 
> func initDB(){
> 	// 从配置中读取 DSN（数据源名称）
> 	dsn := AppConfig.Database.Dsn
> 	// 使用 GORM 打开数据库连接，传入 MySQL 驱动和配置
> 	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
> 	
> 	// 如果打开连接出错，记录致命日志并退出
> 	if err!=nil{
> 		log.Fatalf("Failed to initialize database, got error: %v", err)
> 	}
> 
> 	// 获取底层 *sql.DB 对象以设置连接池参数
> 	sqlDB, err := db.DB()
> 
> 	// 最大空闲连接数
> 	sqlDB.SetMaxIdleConns(AppConfig.Database.MaxIdleConns)
> 	// 最大空闲连接数
> 	sqlDB.SetMaxOpenConns(AppConfig.Database.MaxOpenConns)
> 	// 最大重用时长设置为 1 小时
> 	sqlDB.SetConnMaxLifetime(time.Hour)
> 
> 	if err !=nil{
> 		log.Fatalf("Failed to configure database, got error: %v", err)
> 	}
> 
> 	// 将 GORM DB 对象保存到全局变量，供应用其他地方使用
> 	global.Db = db
> }
> ```
> 
> config/redis.go
> ```go
> # config/redis.go
> package config
> 
> import (
> 	"exchangeapp/global"
> 	"log"
> 
> 	"github.com/go-redis/redis"
> )
> 
> func initRedis(){
> 
> 	// 从配置读取 Redis 地址.数据库索引.密码
> 	addr := AppConfig.Redis.Addr
> 	db := AppConfig.Redis.DB
> 	password := AppConfig.Redis.Password 
> 
> 
> 	// 从配置结构体中读取 Redis 地址、数据库编号和密码
> 	RedisClient := redis.NewClient(&redis.Options{
> 		Addr: addr,
> 		DB: db,
> 		Password: password,
> 	})
> 
> 	// _, err := 短变量声明语法，用来同时接收函数返回的多个值
> 	// 仅保存错误变量 err
> 	// 发送 PING 命令检查与 Redis 的连接是否可用，获取可能的错误
> 	_, err := RedisClient.Ping().Result()
> 
> 	// 若 PING 返回错误则记录致命日志并退出程序
> 	if err !=nil{
> 		log.Fatalf("Failed to connect to Redis, got error: %v", err)
> 	}
> 	
> 	// 将创建好的 Redis 客户端保存到全局变量
> 	global.RedisDB = RedisClient
> }
> ```

> ## 2. 数据库表,字段-gorm 
> models/user.go
> ```go
> # models/user.go
> package models
> 
> import "gorm.io/gorm"
> 
> type User struct{
> 	gorm.Model
> 	// gorm:"unique"标签表示字段在数据库中有唯一约束
> 	Username string `gorm:"unique"`
> 	Password string
> }
> ```
> 
> models/article.go
> ```go
> # models/article.go
> package models
> 
> import "gorm.io/gorm"
> 
> type Article struct {
> 	gorm.Model
> 	// binding（标签）   required（必填字段）
> 	Title string `binding:"required"`
> 	Content string `binding:"required"`
> 	Preview string `binding:"required"`
> }
> ```


> ## 3. 数据库全局使用-gorm 
> ```go
> # global/global.go
> package global
> 
> import (
> 	"github.com/go-redis/redis"
> 	"gorm.io/gorm"
> )
> 
> var(
> 	Db *gorm.DB
> 	RedisDB *redis.Client
> )
> ```

> ## 4. 网站控制器-gin 
> ```go
> # controllers/article_controller.go
> func GetArticles(ctx *gin.Context){
>     // 声明一个名为 article 的变量,变量的类型是 models.Article。        
>     var article models.Article
>     
>     // err-1
>     if err := 塔菲； err ！= nil{
>         ctx.JSON(HTTP状态码, gin.H{"error": err.Error()})
>         return
>     }
>     
>     // err-2
>     test, err:= 塔菲
>     if err !=nil{
>         ctx.JSON(HTTP状态码, gin.H{"error": err.Error()})
>         return
>     }   
>     
>     // 把变量 article 作为 JSON 响应发送给客户端，状态码为 200（OK）。
> 	ctx.JSON(http.StatusOK, article)
> }
> ```
> 
> HTTP 状态码
> ```go
> # controllers/test_controller.go
>     // HTTP 状态码
>     // 400，请求参数或输入校验有问题
>     // 401，凭证不正确
>     // 500，服务器内部错误
>     // 404，资源未找到
>     // 201，资源已创建
>     // 200，操作成功
> 
>     
>     // 函数？启动！！！处理单个 HTTP 请求的上下文对象
>     func test(ctx *gin.Context){}
>     
>     // 基本只使用一次> 
>     // 从 请求体 绑定 JSON 到 user 结构体，出错返回绑定错误
>     ctx.ShouldBindJSON(&user)
>     // 基本只使用一次
>     // 返回 400 Bad Request 并带错误信息，请求参数或输入校验有问题
>     ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
>     
>     // 基本用于操作数据库
>     // 返回 401 Unauthorized（例如登录失败），凭证不正确
>     ctx.JSON(http.StatusUnauthorized, gin.H{"error": "wrong credentials"})
>     
>     
>     // 基本常用
>     // 返回 500 Internal Server Error 并带错误信息，服务器内部错误
>     ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
>     
>     
>     // 基本少用，一般用于查看 资源 使用，与配合返回 500 使用
>     // 返回 404 Not Found 并带错误信息，资源未找到
>     ctx.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
>     
>     
>     // 基本少用，用于创建时使用
>     // 返回 201 Created 并把新创建的 article 序列化为 JSON，资源已创建
>     ctx.JSON(http.StatusCreated, article)
>     
>     // 基本收尾用，ok
>     // 返回 200 OK 并把 article 序列化为 JSON，操作成功
>     ctx.JSON(http.StatusOK, article)
> ```
> 
> DB操作
> ```go
> # controllers/db_controller.go
>     // mysql
>     // 自动迁移，根据 article 结构体创建/更新表结构（会同步字段和索引）
>     global.Db.AutoMigrate(&article)
>     // 创建记录，将 article 插入数据库
>     global.Db.Create(&article).Error
>     // 询所有记录并写入 articles 切片
>     global.Db.Find(&articles).Error
>     // 按 id 查询第一条匹配记录并写入 article
>     global.Db.Where("id = ?", id).First(&article).Error
>     
>     // Redis
>     // 删除指定的缓存键（如果存在）
>     global.RedisDB.Del(cacheKey).Err()
>     // 获取指定缓存键的值，Result() 返回 value 和 error（nil 表示存在）
>     global.RedisDB.Get(cacheKey).Result()
>     // 设置缓存键的值为 articleJSON，过期时间为 10 分钟；返回的 Error 可用来判断是否失败
>     global.RedisDB.Set(cacheKey, articleJSON, 10*time.Minute).Err()
>     // 将 likeKey 的数值自增 1（如果键不存在会初始化为 0 然后自增）
>     global.RedisDB.Incr(likeKey).Err()
> ```

> ## 5. 自定义工具配置
> ```go
> utils/utils.go
> package utils
> 
> import (
> 	"errors"
> 	"time"
> 
> 	"github.com/golang-jwt/jwt"
> 	"golang.org/x/crypto/bcrypt"
> )
> 
> // 参数部分 (pwd string)：函数接受一个名为 pwd 的参数，类型为 string
> // 返回值部分 (string, error)：函数返回两个值
> // 第一个返回值类型为 string（通常是处理结果，例如哈希后的密码）
> // 第二个返回值类型为 error（用于指示是否发生错误；没有错误时为 nil）
> func HashPassword(pwd string) (string, error) {
>     // 将密码转换为字节切片
>     // bcrypt.GenerateFromPassword 会对密码加盐并计算哈希
> 	hash, err := bcrypt.GenerateFromPassword([]byte(pwd), 12)
> 	// 将字节切片转换为字符串并返回
> 	return string(hash), err
> }
> 
> 
> func GenerateJWT(username string) (string, error) {
> 	// 使用 HMAC-SHA256 签名方法创建一个新 token，并用 MapClaims 存放声明（claims）
> 	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
> 		"username": username,                          // 自定义声明：用户名
> 		"exp":      time.Now().Add(time.Hour * 72).Unix(), // 过期时间（Unix 时间戳），72 小时后过期
> 	})
> 
> 	// 使用密钥对 token 进行签名；注意这里把密钥写死为 "secret"
> 	signedToken, err := token.SignedString([]byte("secret"))
> 	// 返回带 "Bearer " 前缀的签名 token 和签名过程中可能发生的错误
> 	return "Bearer " + signedToken, err
> }
> 
> 
> // CheckPassword 比较明文密码与 bcrypt 哈希是否匹配。
> // 参数:
> //   password - 用户输入的明文密码
> //   hash     - 存储的 bcrypt 哈希字符串
> // 返回值:
> //   bool - 匹配时返回 true，否则返回 false
> func CheckPassword(password string, hash string) bool {
> 	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password)) // 将 hash 与密码比较
> 	return err == nil // 无错误表示匹配
> }
> 
> // ParseJWT 解析并验证带或不带 "Bearer " 前缀的 JWT，返回 token 中的 username 声明。
> // 参数:
> //   tokenString - 带或不带 "Bearer " 前缀的 JWT 字符串
> // 返回值:
> //   username - token 中的 username 声明（成功时）
> //   error    - 验证或解析失败时返回非 nil 错误
> func ParseJWT(tokenString string) (string, error) {
> 	// 如果包含 "Bearer " 前缀则去掉它
> 	if len(tokenString) > 7 && tokenString[:7] == "Bearer " {
> 		tokenString = tokenString[7:]
> 	}
> 
> 	// 解析 token，并在回调中验证签名算法与返回签名密钥
> 	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
> 		// 确保使用的是 HMAC 类型的签名方法（防止算法替换攻击）
> 		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
> 			return nil, errors.New("unexpected Signing Method")
> 		}
> 		// 注意：密钥此处硬编码为 "secret"，应改为从配置/环境变量读取
> 		return []byte("secret"), nil
> 	})
> 	if err != nil {
> 		return "", err
> 	}
> 
> 	// 提取并断言为 jwt.MapClaims，检查 token 是否有效
> 	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
> 		username, ok := claims["username"].(string)
> 		if !ok {
> 			return "", errors.New("username claim is not a string")
> 		}
> 		return username, nil
> 	}
> 
> 	// 若未通过上面分支，返回解析时的错误（如果没有具体 err，可返回通用错误）
> 	return "", err
> }
> ```
> bcrypt AND jwt
> ```go
> // 使用 bcrypt 将明文密码 pwd 进行哈希，工作因子（cost）为 12，返回哈希字节切片或错误。
> bcrypt.GenerateFromPassword([]byte(pwd), 12)
> // 将已存储的 bcrypt 哈希与用户输入的明文密码比较，匹配时返回 nil。
> bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
> 
> 
> // 创建一个新的 JWT 对象并附带指定的声明（claims）。
> jwt.NewWithClaims()
> // 表示使用 HMAC-SHA256 作为 JWT 的签名算法。
> jwt.SigningMethodHS256
> // 以 map[string]interface{} 形式表示 JWT 的声明集合（动态、不严格的声明类型）。
> jwt.MapClaims
> // 解析并验证一个 JWT 字符串，需要提供一个回调以返回用于验证签名的密钥。
> jwt.Parse()
> // 表示解析或创建的 JWT 结构体，包含头部、声明和签名等信息。
> jwt.Token
> // JWT 库中 HMAC 类型签名方法的通用接口类型（用于类型断言以防算法替换攻击）。
> jwt.SigningMethodHMAC
> // 同上：动态的声明类型，常用于快速构造/读取自定义字段。
> jwt.MapClaims
> 
> 
> // 计算当前时间向后 72 小时（3 天）的 Unix 时间戳，常用于设置 token 过期时间（exp）。
> time.Now().Add(time.Hour * 72).Unix()
> // 创建并返回一个描述签名算法不符合预期的错误（通常在解析 JWT 时用于拒绝不安全的算法）。
> errors.New("unexpected Signing Method")
> ```

> ## 6. 网站路由-gin
> go
> ```router/router.go
> # router/router.go
> package router
> import (
> 	"test/controllers"
> 	"test/middlewares"
> 	"time"
> 
> 	"github.com/gin-gonic/gin"
> 	"github.com/gin-contrib/cors"
> )
> ```
> 定义一个名为 SetupRouter 的函数，返回类型是 *gin.Engine（Gin 框架的路由引擎）
> ```router/router.go
> func SetupRouter() *gin.Engine{
> 
>     // 创建并返回一个带有默认中间件的 Gin 引擎实例，赋值给变量 r
> 	r := gin.Default()
> 
>     // 为路由 r 添加 CORS 中间件，配置跨域请求策略
> 	r.Use(cors.New(cors.Config{
> 	
>     // 允许的来源（前端地址），只允许来自 http://localhost:5173 的请求
> 		AllowOrigins:     []string{"http://localhost:5173"},
> 		
> 		// 允许的 HTTP 方法
> 		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
> 		
> 		// 允许的请求头（客户端可以发送这些头）
> 		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
> 		
> 		// 可以暴露给客户端的响应头（浏览器可通过 JS 访问）
> 		ExposeHeaders:    []string{"Content-Length"},
> 		
> 		// 允许携带 Cookie 或 Authorization 等凭证
> 		AllowCredentials: true,
> 		
> 		// 预检请求（OPTIONS）缓存时长，12 小时内浏览器不会重复发预检请求
> 		MaxAge: 12 * time.Hour,
> 	  }))
> 	  
> 
>     // 在 Gin 引擎上创建一个路由组，前缀为 /api/auth
> 	auth := r.Group("/api/auth")
> 	{
> 	
> 	// POST /api/auth/login -> controllers.Login 处理登录请求
> 		auth.POST("/login", controllers.Login)
> 	
> 		auth.POST("/register", controllers.Register)
> 	}
> 
>   // 创建 /api 路由组
> 	api := r.Group("/api")
> 	
> 	// GET /api/exchangeRates（无需授权） -> controllers.GetExchangeRates，通常用于公开接口或健康检查
> 	api.GET("/exchangeRates", controllers.GetExchangeRates)
> 	
> 	// 为下面的路由启用认证中间件（需要先登录/验证）
> 	api.Use(middlewares.AuthMiddleWare())
> 	{
>     // 受保护的路由：需要通过 AuthMiddleWare 验证
> 		api.POST("/exchangeRates", controllers.CreateExchangeRate)
> 		api.POST("/articles", controllers.CreateArticle)
> 		api.GET("/articles", controllers.GetArticles)
> 		api.GET("/articles/:id", controllers.GetArticleByID)
> 		
> 		api.POST("/articles/:id/like", controllers.LikeArticle)
> 		api.GET("/articles/:id/like", controllers.GetArticleLikes)
> 	}
> 	
> 	// 返回已配置好的 Gin 引擎实例 r，供外部调用
> 	return r
> }
> ```
> ## 7. 中间件-gin
> ```go
> # middlewares/auth_middleware.go
> // AuthMiddleWare 返回一个 Gin 中间件处理函数
> func AuthMiddleWare() gin.HandlerFunc{
>     // 这里返回的函数会在每个请求进来时被调用
>     return func(ctx *gin.Context){
>     
>     }
> }
>   ```
> HTTP 状态码
> ```middlewares/auth_middleware.go
> 
>     // 从请求头获取 Authorization 值（通常是 Bearer token）
>     ctx.GetHeader("Authorization")
>     
>     // 返回 401 Unauthorized，并在响应体中写入错误信息
>     ctx.JSON(http.StatusUnauthorized, gin.H{"error": "Missing"})
>     // 中断当前请求的后续处理（停止执行后续处理器/路由处理函数）
>     ctx.Abort()
>     
>     // 在上下文中设置键值对，后续中间件或处理函数可通过 ctx.Get("username") 读取
>     ctx.Set("username", username)
>     // 在中间件执行结束后继续执行下一个处理器
>     ctx.Next()
> ```
