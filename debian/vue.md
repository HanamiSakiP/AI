## 0. vue_js省流

### 结构
```demo
# 重要文件
package.json   // 查看已安装库（bash）
src/main.js   // 导入注册组件
src/router/index.js   // 配置路由
vite.config.js   // 配置路径别名
jsconfig.json   // 配置@路径提示（没有须自建）

# 一般结构
node_modules   // 依赖
src/views   // 主要页面-provide(传入给子组件)

# 匿名插槽
//      <Header>
//            <a href="123.com">关注塔菲喵</a>
//      </Header>
# 具名插槽(v-slot:url 简写 #url)
//      <Footer>
//          <template #url>
//                <a href="123.com">关注塔菲喵</a>
//          </template>
//      </Footer>
# 作用域插槽
# 解构
// <Footer><template #user="{url,title}"></template></Footer>

src/components   // 子组件

// provide(传入给子组件)
// defineProps/inject(注入父组件/依赖注入)二选一
// defineEmits(传入给父组件)

# 匿名插槽
// <slot/>
# 具名插槽
// <slot name="url" />
# 作用域插槽
// <slot name="user" url="123.com" title="塔菲直播" />

src/router   // 网页路由
src/assets   // 图标,图片等存储路径
src/store   // 状态管理
```


### 安装和使用vue
```bash
npm create vite@latest
# demo为项目名
cd demo
```

### 初始化项目结构
```bash
mkdir src/views src/router src/store
touch src/router/index.js
rm src/style.css
rm src/components/HelloWorld.vue
sed -i "s/import '\.\/style\.css'//g" src/main.js

# 初始内容
cat > src/App.vue << 'EOF'
<script setup>
</script>

<template>
    <router-view />
</template>

<style scoped>
</style>
EOF
```

### 下载组件
进入项目路径后
```bash
npm install
npm install vue-router@4
# 此处为导入全部
npm install element-plus --save
# 按需导入
# npm install -D unplugin-vue-compon ents unplugin-auto-import
# npm install -D unplugin-icons

# 状态管理库
# npm install pinia
# npm i pinia-plugin-persistedstate
```

### 启动
```bash
npm run dev
```

### src/main.js
```src/main.js
import { createApp } from 'vue'

//整体导入 ElementPlus 组件库
import ElementPlus from 'element-plus' //导入 ElementPlus 组件库的所有模块和功能 
import 'element-plus/dist/index.css' //导入 ElementPlus 组件库所需的全局 CSS 样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue' //导入 ElementPlus 组件库中的所有图标
import zhCn from 'element-plus/dist/locale/zh-cn.mjs' //导入 ElementPlus 组件库的中文语言包

// 导入 router 
import router from './router'

import App from './App.vue'

const app = createApp(App)

//注册 ElementPlus 组件库中的所有图标到全局 Vue 应用中
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

//app.use(ElementPlus) //将 ElementPlus 插件注册到 Vue 应用中s
app.use(ElementPlus, {
    locale: zhCn // 设置 ElementPlus 组件库的区域语言为中文简体
})

// 将Vue Router实例注册到Vue应用中
app.use(router)

app.mount('#app')
```


### 实例src/router/index.js
```src/router/index.js
import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const routes = [
    {
        path: "/", // http://localhost:5173
        // 定义别名 http://localhost:5173/home
        alias: ["/home", "/index"], // http://localhost:5173/index
        component: () => import("@/views/index.vue")
    },
    {
        path: "/content", // 查询字符串传参 http://localhost:5173/content?id=100&title=塔菲编程
        component: () => import("@/views/content.vue")
    },
    {
        path: "/user/:id/name/:name", // 路径传参 http://localhost:5173/user/007/name/塔菲
        component: () => import("@/views/user.vue")
    },
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

### 实例views/index.vue
```views/index.vue
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

### 实例views/content.vue
```views/content.vue
<script setup></script>

<template>
    内容页<hr>
    id: {{ $route.query.id }} <br>
    title: {{ $route.query.title }}
</template>

<style scoped></style>
```

### 实例views/user.vue
```views/user.vue
<script setup>
</script>

<template>
    个人主页<hr>
    id: {{ $route.params.id }} <br>
    name: {{ $route.params.name }}
</template>

<style scoped>
</style>
```

### 实例views/vip.vue
```views/vip.vue
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

### 实例views/vip/default.vue
```views/vip/default.vue
<script setup></script>

<template>
    会员默认页<br>
</template>

<style scoped></style>
```

### 实例views/vip/info.vue
```views/vip/info.vue
<script setup></script>

<template>
    会员资料
</template>

<style scoped></style>
```

### 实例components/header.vue
```components/header.vue
<script setup>
</script>

<template>
    Header<br>
</template>

<style scoped>
</style>
```

### 实例components/footer.vue
```components/footer.vue
<script setup>
</script>

<template>
    Footer<br>
</template>

<style scoped>
</style>
```


### vite.config.js
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

### 没有须自建jsconfig.json
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


## 1. 基于Vite创建Vue3项目 
[vite官网](https://cn.vitejs.dev)
```bash
npm create vite@latest
```
+ 选项
```bash
    Ok to proceed? (y) » y
    Project name: » demo
    Select a framework: » Vue
    Select a variant: » JavaScript
```

+ 启动项目
```bash
    # Done. Now run:
    cd demo
    npm install
    npm run dev
```

+ 删除文件
```init
rm src/style.css
rm src/components/HelloWorld.vue
```

+ 删除代码
```init
# main.js <- 文件名
import './style.css' 
```

编辑 src/App.vue 代码
```App.vue
<script setup>
</script>

<template>
内容
</template>

<style scoped>
</style>
```

## 2. Vue3 快速入门4-Pinia
   [Pinia官网](https://pinia.vuejs.org/zh)
```bash
npm install pinia
npm i pinia-plugin-persistedstate
```

## 3. Vue Router 快速掌握
[Vue Router 官网](https://router.vuejs.org/zh)
```bash
npm install vue-router@4
```

## 4. ElementPlus 快速掌握
[ElementPlus 官网](https://element-plus.org/zh-CN)
```bash
npm install element-plus --save
```

* 自动导入
+ 安装 unplugin-vue-components 和 unplugin-auto-import 插件
```bash
npm install -D unplugin-vue-compon ents unplugin-auto-import
```

* 自动导入 图标
+ 安装 unplugin-icons 插件
```bash
npm install -D unplugin-icons
```
