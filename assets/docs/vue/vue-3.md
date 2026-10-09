## 0. 基于Vite创建Vue3项目 
[vite官网](https://cn.vitejs.dev)
```bash
npm create vite@latest
```

## 1.父传子 defineProps
+ App.vue（父）（    script   标签）
```App.vue
<script setup>
  import { reactive } from 'vue'

  //导入子组件（首字母大写）
  //App.vue是父组件,因为它包含了header.vue和footer.vue两个子组件
  import Header from "./components/header.vue"
  import Footer from "./components/footer.vue"

  /*
  const propsWeb = {
    user: 10,
    ip: '127.0.0.1'
  }
  */
  //响应式数据
  const propsWeb = reactive({
    user: 10,
    ip: '127.0.0.1'
  })

  //添加用户
  const userAdd = () => {
    propsWeb.user++
    console.log(propsWeb.user)
  }
</script>
```

+ App.vue（父）（    template   标签）
```App.vue
<template>
  <!-- 父传子 - 方式1 -->
  <Header propsName="塔菲编程" propsUrl="live.bilibili.com/22603245/" />

  live.bilibili.com/22603245/

  <button @click="userAdd">添加用户</button>

  <!-- 父传子 - 方式2 -->
  <!-- <Footer v-bind="propsWeb" /> -->
  <Footer :="propsWeb" />
</template>
```

components/header.vue（子1）
```components/header.vue
<script setup>
    //子组件

    //接收方式1 - 数组
    /*
        defineProps是Vue3的编译时宏函数,
        用于接收父组件向子组件传递的属性(props)

        注
        当使用Vue编译器编译包含defineProps的组件时,
        编译器会将这些宏替换为相应的运行时代码
    */
    const props = defineProps(["propsName","propsUrl"])
    console.log(props)
</script>

<template>
    <h3>Header</h3>
</template>

<style scoped></style>
```

components/footer.vue（子2）
```components/footer.vue
<script setup>
    //子组件

    //接收方式2 - 对象
    /*
    const props = defineProps({
        user: Number,
        ip: String
    })
    */
    const props = defineProps({
        user: Number,
        ip: {
            type: String,
            required: true, //true表示必传属性,若未传则会提示警告信息
            default: 'localhost' //未传默认值
        }
    })

    console.log(props)
</script>

<template>
    <h3>Footer</h3>
    user: {{ props.user }}
</template>

<style scoped></style>
```

##  2.子传父 defineEmits
App.vue父
```App.vue
<script setup>
  import { reactive,ref } from 'vue'

  //导入子组件
  import Header from "./components/header.vue"

  //响应式数据
  const web = reactive({
    name: "塔菲编程",
    url: 'live.bilibili.com/22603245/'
  })

  const user = ref(0)

  //子传父
  const emitsWeb = (data) => {
    console.log("emitsWeb:",data)
    web.url = data.url
  }

  const emitsUser = (data) => {
    console.log("emitsUser:",data)
    user.value += data
  }
</script>

<template>
  <!-- 子传父 -->
  <Header @web="emitsWeb" @user="emitsUser" />

  {{ web.url }} - {{ user }}
</template>
<style scoped></style>
```

components/header.vue子
```components/header.vue
<script setup>
    //子组件

    /*
        defineEmits是Vue3的编译时宏函数,
        用于子组件向父组件发送自定义事件
    */
    //子传父
    //定义一个名为 emits 的对象, 用于存储自定义事件
    const emits = defineEmits(["web","user"])
    //发送名为 web 和 user 的自定义事件
    emits("web", {name:"塔菲",url:"https://live.bilibili.com/22603245/"})
    
    //添加用户
    const userAdd = () => {
        //发送名为 user 的自定义事件
        emits("user", 10)
    }
</script>

<template>
    <h3>Header</h3>

    <button @click="userAdd">添加用户</button>
</template>

<style scoped></style>
```

## 3. 跨组件通信-依赖注入

App.vue父
```App.vue
<script setup>
  import { provide, ref } from 'vue'

  //导入子组件
  import Header from "./components/header.vue"

  //provide用于父组件将 数据 提供给所有子组件
  /*
    若使用了provide和inject来进行数据传递,
    则一般不需要再使用defineProps
  */
  provide("provideWeb",{name:"塔菲",url:"https://live.bilibili.com/22603245"})

  //传递响应式数据
  const user = ref(0)
  provide("provideUser",user)

  //添加用户
  const userAdd = () => {
    user.value++
  }
  //用于父组件将 函数 提供给所有子组件
  provide("provideFuncUserAdd",userAdd)
</script>

<template>
  <h3>App.vue-Top组件</h3>

  {{ user }}

  <!-- 子组件 -->
  <Header/>
</template>
<style scoped></style>
```

components/header.vue子
```components/header.vue
<script setup>
    import { provide, inject } from 'vue'

    //导入子组件
    import Nav from "./nav.vue"

    //子组件通过inject注入父组件提供的 响应式数据
    const user = inject("provideUser")
    console.log("provideUser:",user.value)

    //provide用于父组件将 数据 提供给所有子组件
    provide("provideUrl","live.bilibili.com/22603245")
</script>

<template>
    <h3>header.vue-Middle组件</h3>

    <!-- 子组件 -->
    <Nav/>
</template>
<style scoped></style>
```

components/nav.vue子的子组件
```components/nav.vue
<script setup>
    //子组件
    import { inject } from 'vue'

    //子组件通过inject注入父组件提供的 数据
    const web = inject("provideWeb")
    console.log("provideWeb:",web)

    const url = inject("provideUrl")
    console.log("provideUrl:",url)

    //子组件通过inject注入父组件提供的 函数
    const funcUserAdd = inject("provideFuncUserAdd")
    console.log("provideFuncUserAdd:",funcUserAdd)
</script>

<template>
    <h3>nav.vue-Bottom组件</h3>

    <button @click="funcUserAdd">添加用户</button>
</template>
<style scoped></style>
```

## 4. 匿名插槽和具名插槽


App.vue父
```App.vue
<script setup>
  //导入子组件
  import Header from "./components/header.vue"
  import Footer from "./components/footer.vue"
</script>

<template>
  <h3>App.vue</h3>

  <!-- <Header/> -->
  <!-- 匿名插槽 -->
  <Header>
    <a href="https://space.bilibili.com/1265680561">关注塔菲喵</a>
  </Header>

  <!-- 具名插槽 -->
  <Footer>
    <template v-slot:url>
      <a href="https://live.bilibili.com/22603245/">塔菲直播</a>
    </template>

    <!-- v-slot:user 简写 #user -->
    <template #user>
      1000
    </template>
  </Footer>

</template>

<style scoped></style>
```

components/header.vue子1
```components/header.vue
<script setup></script>

<template>
    <h3>header.vue - 子组件</h3>

    <!-- 匿名插槽 -->
    <slot/>
</template>

<style scoped></style>
```

components/footer.vue子2
```components/footer.vue
<script setup></script>

<template>
    <h3>footer.vue - 子组件</h3>

    <!-- 具名插槽 -->
    <slot name="url" />
    <slot name="user" />
</template>

<style scoped></style>
```

## 5. 作用域插槽
App.vue父
```App.vue
<script setup>
  //导入子组件
  import Header from "./components/header.vue"
  import Footer from "./components/footer.vue"
</script>

<template>
  <h3>App.vue</h3>

  <!-- <Header/> -->
  <!-- 匿名插槽 -->
  <Header>
    <a href="https://space.bilibili.com/1265680561">关注塔菲喵</a>
  </Header>

  <!-- 具名插槽 -->
  <Footer>
    <template v-slot:url>
      <a href="https://live.bilibili.com/22603245/">塔菲直播</a>
    </template>

    <!--
      v-slot:user 简写 #user

      作用域插槽
      子组件将url和title数据传递给 name="user" 的插槽,
      父组件通过 #user="data" 来接收这些数据

      <template #user="data">
        1000 {{ data.url }} {{ data.title }}
      </template>
    -->
    <!-- 解构 -->
    <template #user="{url,title}">
      1000 {{ url }} {{ title }}
    </template>
  </Footer>

</template>

<style scoped></style>
```

components/header.vue子1
```components/header.vue
<script setup></script>

<template>
    <h3>header.vue - 子组件</h3>

    <!-- 匿名插槽 -->
    <slot/>
</template>

<style scoped></style>
```

components/footer.vue子2
```components/footer.vue
<script setup></script>

<template>
    <h3>footer.vue - 子组件</h3>

    <!-- 具名插槽 -->
    <slot name="url" />
    <slot name="user" url="https://gakuen.idolmaster-official.jp/" title="学园偶像大师官网" />
</template>

<style scoped></style>
```

##  6. toRef和toRefs
App.vue
```App.vue
<script setup>
  import { reactive, toRef, toRefs } from 'vue'

  /*
  let {name,url} = reactive({
    name:"关注塔菲喵",
    url:"https://space.bilibili.com/1265680561"
  })
  */
  let web = reactive({
    name:"关注塔菲喵",
    url:"https://space.bilibili.com/1265680561"
  })

  //toRefs将一个响应式对象的所有属性转换为ref对象
  //let {name,url} = toRefs(web)

  //toRef将一个响应式对象的某个属性转换为ref变量
  let url = toRef(web, "url")

  const setUrl = () => {
    console.log(url)
    url.value = "https://live.bilibili.com/22603245"
  }
</script>

<template>
  {{ url }}

  <button @click="setUrl">设置网址</button>
</template>


<style scoped></style>
```

## 7. 生命周期函数

```生命周期函数
生命周期函数

       是组件实例从创建到销毁过程中不同时间点自动调用的函数


挂载阶段

       onBeforeMount

               在组件实例即将被挂载到DOM树之前调用

               此时模板还未编译或渲染到DOM,通常用于执行初始化操作,

               如:获取异步数据、设置初始属性值等

       onMounted

               在组件成功挂载到DOM并完成首次渲染后调用

               此时可以访问和操作DOM元素,

               并执行与页面交互相关的逻辑

更新阶段

       onBeforeUpdate (由于响应式数据变化)

               在组件更新之前即将重新渲染时调用

               可以根据新的参数判断是否需要进行特殊处理,

               甚至可以选择阻止此次更新过程

       onUpdated

               在组件完成更新并重新渲染后调用

               可以基于新的渲染结果处理更新后的数据

卸载阶段

       onBeforeUnmount

               在组件从DOM中销毁之前调用

               用于释放资源,如:清理计时器、解绑事件监听器等

       onUnmounted

               在组件已经从DOM中移除并销毁后调用

               确保组件所占用的所有资源都被正确释放

错误处理

       onErrorCaptured

               在捕获到组件中的错误时调用

               用于处理错误,如:记录错误日志等


注

组件挂载的过程

模板编译

       将组件的模板转换为JS代码

渲染

       在模板编译后生成的JS代码渲染到页面上,

       生成虚拟DOM

挂载

       在渲染完成后将虚拟DOM挂载到真实的DOM树上,

       使其在页面上显示出来
```

App.vue
```App.vue
<script setup>
  import { onMounted, onUpdated, ref } from 'vue'

  //在组件成功挂载到DOM并完成首次渲染后调用
  onMounted(() => {
    console.log("onMounted")
  })

  //在组件更新之后调用
  onUpdated(() => {
    console.log("onUpdated:",user.value)
  })

  const user = ref(0)
  console.log("user:",user.value)
</script>

<template>
  <h3>App.vue</h3>

  {{ user }}

  <button @click="user++">添加用户</button>
</template>

<style scoped></style>
```