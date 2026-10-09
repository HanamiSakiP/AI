## go-gin-grom

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

<details>
<summary>基础知识2</summary>

```bash
# 1. 配置java环境(Spring Boot)

# windows环境配置
# 新建 JAVA_HOME
JAVA_HOME
# 路径
C:\Program Files\Java\jdk-17

# Path 配置
%JAVA_HOME%\bin
%JAVA_HOME%\jre\bin

# 确认是否配置成功
java -version
javac -version

# 2. 配置Maven环境(Spring Boot)
# 新建 MAVEN_HOME
MAVEN_HOME
# 路径
C:\apache-maven-3.9.11
# Path 配置
%MAVEN_HOME%\bin

# 确认是否配置成功
mvn -v


# 配置Nodejs环境(frontend)
# 配置 数据库 环境 (如:mysql,redis)
# 配置go环境
```

```bash
# Spring Boot-js_vue结构
demo/
├── frontend/  # 前端
│   └── src/
│   │    ├── api/
│   │    ├── components/  # 公共页面
│   │    └── router/  # 路由
│   │    └── stores/  # 状态
│   │    └── views/  # 主要页面
│   │    └── App.vue  # 主入口
│   │    └── main.js  # 导入配置
│   │    └── request.js  # 拦截器
│   └── vite.config.js  # 配置文件
│   └── package.json  # 导入包信息
│   └── node_modules/  # 前端依赖
├── backend/  # 后端
│   └── src/main/          # Maven标准的主代码目录（生产环境代码）
│        └── resources/application.yml # Spring Boot核心配置文件（非Maven配置）
│        └── java/com/office/          # 项目Java代码的基础包路径
│               └── common/            # 通用公共模块
│               └── config/            # 配置类模块
│               └── controller/        # 控制器模块-接收前端请求，返回响应（RESTful接口层）
│               └── entity/            # 实体类模块：对应数据库表结构的POJO/Entity类
│               └── mapper/            # Mapper接口模块：MyBatis的Mapper接口（数据访问层）
│               └── service/           # 服务层模块：业务逻辑处理（含接口和实现类，通常分impl子目录）
│               └── util/              # 工具类模块
└── pom.xml  # Maven项目核心配置文件
└── target/  # Maven依赖
└── README.md  # 项目说明文档
```

```bash
# Spring Boot
entity -> mapper 
entity -> service --> impl
common,config,utils -> controller

# 前端依赖下载
npm install
# 前端启动
npm run dev
# 后端Maven依赖下载
mvn clean install
# 后端 Spring Boot 启动
mvn spring-boot:run
```

```bash
# go-gin-grom
demo/
├── frontend/  # 前端
│   └── src/
│   │    ├── api/
│   │    ├── components/  # 公共页面
│   │    └── router/  # 路由
│   │    └── stores/  # 状态
│   │    └── views/  # 主要页面
│   │    └── App.vue  # 主入口
│   │    └── main.js  # 导入配置
│   │    └── request.js  # 拦截器
│   └── vite.config.js  # 配置文件
│   └── package.json  # 导入包信息
│   └── node_modules/  # 前端依赖
├── backend/  # 后端
│   └── config/  # 配置
│   └── controller/  # 控制器
│   └── initialize/  # 数据库初始数据
│   └── middlewares/  # 中间件
│   └── models/  # 模型
│   └── router/  # 路由
│   └── util/  # 工具
└── main.go  # go程序的入口
└── go.mod  # Go Modules 的核心配置文件
└── go.sum  # go依赖
└── README.md  # 项目说明文档
```



```bash
# vue(frontend)
# axios
request.js -> api
stores -> router
stores/user.js -> Login.vue,Register.vue,router.js
--> user.vue,admin.vue(角色区分导航栏)
api -> test.vue
main.js -> App.vue -> router.js -> test.vue


# go-gin-grom(backend)
models -> controller,initialize
config,util,middlewares -> controller
controller -> router


# frontend -> backend
vite.config.js,request.js -> router(backend)
api -> controller
# backend -> databases
config -> databases


# go依赖下载
go mod tidy
# go后端启动
go run .
```

</details>

<details>
<summary>常用数据库命令</summary>

```bash
# mysql
# 连接mysql数据库
mysql -u root -p
# mysql命令
# 创建 test 库
create database test;
# 查询所有 库
show databases;
# 1. 使用 test 库
use test;
# 2. 查询 test 库 所有 表
show tables;
```

</details>


<details>
<summary>go-gin-grom代码（点击展开）</summary>

```bash
# config
# router
# controllers
```

白嫖禁止

[![](../../img/95750227_p0.png)](/show?code=AI-code.git "关注塔菲喵")

</details>
