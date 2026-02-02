## 0. 安装路由
[Vue Router 官网](https://router.vuejs.org/zh)
```bash
npm install vue-router@4
```

## 1. 设置路由

src/main.js  注册路由
```src/main.js
import router from './router'

//use(router) 将Vue Router实例注册到Vue应用中
createApp(App).use(router).mount('#app')
```

src/router/index.js  配置路由
```src/router/index.js
import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const routes = [
    {
        path: "/", // http://localhost:5173
	    component: () => import("../views/index.vue")
	},
	{
	    path: "/content", // http://localhost:5173/content
	    component: () => import("../views/content.vue")
	},
]

const router = createRouter({
	//使用url的#符号之后的部分模拟url路径的变化,因为不会触发页面刷新,所以不需要服务端支持
	//history: createWebHashHistory(), 
	history: createWebHistory(),
	routes
})

export default router
```

src/App.vue  设置路由
```src/App.vue
<script setup></script>

<template>
	<router-view />
</template>

<style scoped></style>
```

src/views/index.vue  首页
```src/views/index.vue
<script setup></script>

<template>
	首页 - https://live.bilibili.com/22603245
</template>

<style scoped></style>
```

src/views/content.vue  内容页
```src/views/content.vue
<script setup></script>

<template>
	内容页 - 塔菲编程
</template>

<style scoped></style>
```

## 2. 配置路径别名@和VSCode路径提示

vite.config.js
```vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' //导入 node.js path

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
      alias: { //配置路径别名
        '@': path.resolve(__dirname, 'src')
      }
    }
})
```

jsconfig.json
```jsconfig.json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@/*": [
                "src/*"
            ] // 配置 @ 符号指向 src 目录及其子目录
        }
    }
}
```

src/router/index.js
```src/router/index.js
import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const routes = [
    {
        path: "/", // http://localhost:5173
	    component: () => import("@/views/index.vue")
	},
	{
	    path: "/content", // http://localhost:5173/content
	    component: () => import("@/views/content.vue")
	},
]

const router = createRouter({
	//使用url的#符号之后的部分模拟url路径的变化,因为不会触发页面刷新,所以不需要服务端支持
	//history: createWebHashHistory(), 
	history: createWebHistory(),
	routes
})

export default router
```

## 3.使用查询字符串或路径传递参数

src/router/index.js
```src/router/index.js
import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const routes = [
    {
        path: "/", // http://localhost:5173
        component: () => import("@/views/index.vue")
    },
    {
        path: "/content", // 使用查询字符串传递参数 http://localhost:5173/content?id=100&title=塔菲编程
        component: () => import("@/views/content.vue")
    },
    {
        path: "/user/:id/name/:name", // 使用路径传递参数 http://localhost:5173/user/007/name/塔菲
        component: () => import("@/views/user.vue")
    },
    {
        //可选参数 name? 表示该参数不是必需的
        path: "/userHistory/:id/name/:name?", // http://localhost:5173/userHistory/007/name
        component: () => import("@/views/user.vue")
    }
]

const router = createRouter({
    //使用url的#符号之后的部分模拟url路径的变化,因为不会触发页面刷新,所以不需要服务端支持
    //history: createWebHashHistory(), 
    history: createWebHistory(),
    routes
})

export default router
```

src/views/content.vue
```src/views/content.vue
<script setup></script>

<template>
	内容页 - 塔菲编程 <hr>
	
	id: {{ $route.query.id }} <br>
	title: {{ $route.query.title }}
</template>

<style scoped></style>
```

src/views/user.vue
```src/views/user.vue
<script setup></script>

<template>
	个人主页 - https://live.bilibili.com/22603245 <hr>
	
	id: {{ $route.params.id }} <br>
	name: {{ $route.params.name }}
</template>

<style scoped></style>
```

## 4. 别名、路由名称、编程式导航

省流
src/router/index.js
```src/router/index.js
        path: "/", // http://localhost:5173
# 在下方添加别名
        //alias:"/home", //定义别名 http://localhost:5173/home
        alias: ["/home", "/index"], // http://localhost:5173/home http://localhost:5173/index
```

完整版
src/router/index.js
```src/router/index.js
import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const routes = [
    {
        path: "/", // http://localhost:5173
        //alias:"/home", //定义别名 http://localhost:5173/home
        alias: ["/home", "/index"], // http://localhost:5173/home http://localhost:5173/index
        component: () => import("@/views/index.vue")
    },
    {
        path: "/content", // 使用查询字符串传递参数 http://localhost:5173/content?id=100&title=塔菲编程
        component: () => import("@/views/content.vue")
    },
    {
        path: "/user/:id/name/:name", // 使用路径传递参数 http://localhost:5173/user/007/name/塔菲
        component: () => import("@/views/user.vue")
    },
    {
        //可选参数 name? 表示该参数不是必需的
        path: "/userHistory/:id/name/:name?", // http://localhost:5173/userHistory/007/name
        component: () => import("@/views/user.vue")
    }
]

const router = createRouter({
    //使用url的#符号之后的部分模拟url路径的变化,因为不会触发页面刷新,所以不需要服务端支持
    //history: createWebHashHistory(), 
    history: createWebHistory(),
    routes
})

export default router
```

src/views/index.vue
```src/views/index.vue
<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()

let userId = 100
let userName = "塔菲"

const goTo = () => {
	//router.push("/user/007/name/塔菲")
	//router.push({ path: '/content', query: { id: 200, title: '塔菲' } })
	router.push({ name: 'history', params: { id: '300', name: '塔菲编程' } })
}
</script>

<template>
	首页 - dengruicode.com
	<hr>

	<router-link to="/content?id=100&title=塔菲编程">查询字符串传参</router-link> <br>
	<router-link to="/user/007/name/塔菲">路径传参</router-link> <br>

	<!-- 动态属性绑定 -->
	<router-link :to="{ path: '/content', query: { id: 200, title: '塔菲' } }">查询字符串传参 - 动态属性绑定</router-link> <br>
	<router-link :to="{ path: `/user/${userId}/name/${userName}` }">路径传参 - 动态属性绑定</router-link> <br>

	<!-- 定义路由名称 -->
	<router-link :to="{ name: 'history', params: { id: '300', name: '塔菲编程' } }">路径传参 - 定义路由名称</router-link> <br>

	<!-- 编程式导航 -->
	<button @click="goTo()">编程式导航</button>
</template>

<style scoped></style>
```

## 5. 嵌套路由结合共享组件

省流
src/router/index.js
```src/router/index.js
# 添加
    {
        path: "/vip",
        component: () => import("@/views/vip.vue"),
        children: [ // 子路由
            {
                path: '', // 默认页 http://localhost:5173/vip
                component: import("@/views/vip/default.vue")
            },
            {
                path: 'order', // 会员订单 http://localhost:5173/vip/order
                component: import("@/views/vip/order.vue")
            },
            {
                path: 'info', // 会员资料 http://localhost:5173/vip/info
                component: import("@/views/vip/info.vue")
            }
        ]
    }
```

完整版
src/router/index.js
```src/router/index.js
import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const routes = [
    {
        path: "/", // http://localhost:5173
        //alias:"/home", //定义别名 http://localhost:5173/home
        alias: ["/home", "/index"], // http://localhost:5173/home http://localhost:5173/index
        component: () => import("@/views/index.vue")
    },
    {
        path: "/content", // 使用查询字符串传递参数 http://localhost:5173/content?id=100&title=塔菲编程
        component: () => import("@/views/content.vue")
    },
    {
        path: "/user/:id/name/:name", // 使用路径传递参数 http://localhost:5173/user/007/name/塔菲
        component: () => import("@/views/user.vue")
    },
    {
        //可选参数 name? 表示该参数不是必需的
        path: "/userHistory/:id/name/:name?", // http://localhost:5173/userHistory/007/name
        component: () => import("@/views/user.vue")
    },
    {
        path: "/vip",
        component: () => import("@/views/vip.vue"),
        children: [ // 子路由
            {
                path: '', // 默认页 http://localhost:5173/vip
                component: import("@/views/vip/default.vue")
            },
            {
                path: 'order', // 会员订单 http://localhost:5173/vip/order
                component: import("@/views/vip/order.vue")
            },
            {
                path: 'info', // 会员资料 http://localhost:5173/vip/info
                component: import("@/views/vip/info.vue")
            }
        ]
    }
]

const router = createRouter({
    //使用url的#符号之后的部分模拟url路径的变化,因为不会触发页面刷新,所以不需要服务端支持
    //history: createWebHashHistory(), 
    history: createWebHistory(),
    routes
})

export default router
```

src/views/vip.vue
```src/views/vip.vue
<script setup>
//导入子组件
import Header from "@/components/header.vue"
import Footer from "@/components/footer.vue"
</script>

<template>
	<!-- 共享的Header组件 -->
	<Header />

	<!-- 根据不同的子路由加载不同子页面 -->
	<router-view />

	<!-- 共享的Footer组件 -->
	<Footer />
</template>


<style scoped></style>
```

src/views/vip/default.vue
```src/views/vip/default.vue
<script setup></script>

<template>
	会员默认页
</template>

<style scoped></style>
```

src/views/vip/order.vue
```src/views/vip/order.vue
<script setup></script>

<template>
	会员订单
</template>

<style scoped></style>
```

src/views/vip/info.vue
```src/views/vip/info.vue
<script setup></script>

<template>
	会员资料
</template>

<style scoped></style>
```

## 6. 重定向

src/router/index.js
```src/router/index.js
# 添加自定义路由名称
    {
        //可选参数 name? 表示该参数不是必需的
        path: "/userHistory/:id/name/:name?", // http://localhost:5173/userHistory/007/name
        name: "history", // 定义路由名称
        component: () => import("@/views/user.vue")
    },
    {
        path: "/svip", // http://localhost:5173/svip
        //redirect: "/vip" // 重定向
        redirect: { name: 'history', params: { id: '100', name: 'David' } }
    }
```

## 7. 全局前置守卫

src/main.js
```src/main.js
import { createApp } from 'vue'
import App from './App.vue'

import router from './router'

//createApp(App).mount('#app')
const app = createApp(App)
app.use(router)

//全局前置守卫
router.beforeEach((to, from, next) => {
    console.log("to:", to) //即将进入的路由的信息
    console.log("from:", from) //当前即将离开的路由信息

    next()

    /*
        if(to.name == "history"){
            next(false) //拦截
        }else{
            next() //继续
        }
    */
})

app.mount('#app')
```