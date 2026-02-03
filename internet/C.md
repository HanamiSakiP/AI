## C语言程序与设计
<details>
<summary>1. 常量,变量和数据类型（点击展开）</summary>

```c
// 常量
#include <stdio.h>

#define PI 3.14159  // 宏定义常量

int main() {
    const int MAX = 100;  // const常量
    
    // 字面常量
    printf("整数常量: %d\n", 10);
    printf("浮点数常量: %.2f\n", 3.14);
    printf("字符常量: %c\n", 'A');
    printf("字符串常量: %s\n", "Hello");
    
    printf("PI的值: %.5f\n", PI);
    printf("MAX的值: %d\n", MAX);
    
    return 0;
}
```

```c
// 变量和数据类型
#include <stdio.h>

int main() {
    // 基本数据类型
    int age = 25;              // 整型
    float height = 1.75f;      // 单精度浮点型
    double salary = 5000.50;   // 双精度浮点型
    char grade = 'A';          // 字符型
    
    // 修饰符
    short smallNumber = 100;   // 短整型
    long bigNumber = 100000L;  // 长整型
    unsigned int positive = 50; // 无符号整型
    
    printf("年龄: %d岁\n", age);
    printf("身高: %.2f米\n", height);
    printf("工资: %.2f元\n", salary);
    printf("等级: %c\n", grade);
    
    // 类型转换
    int x = 10;
    float y = 3.5;
    float result = x + y;  // 隐式类型转换
    printf("10 + 3.5 = %.2f\n", result);
    
    int explicit = (int)y;  // 显式类型转换
    printf("3.5转换为整数: %d\n", explicit);
    
    return 0;
}
```

</details>

<details>
<summary>2. 语法（点击展开）</summary>

```c
#include <stdio.h>

int main() {
    // 1. 控制结构
    
    // 条件语句
    int score = 85;
    
    if (score >= 90) {
        printf("优秀\n");
    } else if (score >= 60) {
        printf("及格\n");
    } else {
        printf("不及格\n");
    }
    
    // switch语句
    char op = '+';
    int a = 10, b = 5;
    
    switch(op) {
        case '+':
            printf("%d + %d = %d\n", a, b, a + b);
            break;
        case '-':
            printf("%d - %d = %d\n", a, b, a - b);
            break;
        default:
            printf("未知操作\n");
    }
    
    // 2. 循环语句
    
    // for循环
    printf("for循环: ");
    for(int i = 0; i < 5; i++) {
        printf("%d ", i);
    }
    printf("\n");
    
    // while循环
    printf("while循环: ");
    int j = 0;
    while(j < 3) {
        printf("%d ", j);
        j++;
    }
    printf("\n");
    
    // do-while循环
    printf("do-while循环: ");
    int k = 0;
    do {
        printf("%d ", k);
        k++;
    } while(k < 3);
    printf("\n");
    
    // 3. 数组
    int numbers[5] = {1, 2, 3, 4, 5};
    printf("数组元素: ");
    for(int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    
    // 字符串
    char name[] = "张三";
    printf("姓名: %s\n", name);
    
    return 0;
}
```

</details>

<details>
<summary>3. 函数（点击展开）</summary>

```c
#include <stdio.h>

// 1. 函数声明
int add(int a, int b);
void printMessage();
double calculateCircleArea(double radius);

// 2. 主函数
int main() {
    // 调用函数
    int sum = add(10, 20);
    printf("10 + 20 = %d\n", sum);
    
    printMessage();
    
    double area = calculateCircleArea(5.0);
    printf("半径为5的圆面积: %.2f\n", area);
    
    // 递归函数示例
    int factorial = calcFactorial(5);
    printf("5的阶乘: %d\n", factorial);
    
    return 0;
}

// 3. 函数定义

// 返回两个整数的和
int add(int a, int b) {
    return a + b;
}

// 无返回值的函数
void printMessage() {
    printf("这是一个无返回值的函数\n");
}

// 计算圆面积
double calculateCircleArea(double radius) {
    const double PI = 3.14159;
    return PI * radius * radius;
}

// 递归函数：计算阶乘
int calcFactorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * calcFactorial(n - 1);
}
```

</details>


<details>
<summary>4. 结构体（点击展开）</summary>

```c
#include <stdio.h>
#include <string.h>

// 1. 定义结构体
struct Student {
    int id;
    char name[50];
    int age;
    float score;
};

// 2. 定义结构体别名
typedef struct {
    char title[100];
    char author[50];
    float price;
} Book;

int main() {
    // 3. 声明结构体变量
    struct Student stu1;
    stu1.id = 1001;
    strcpy(stu1.name, "李四");
    stu1.age = 20;
    stu1.score = 88.5;
    
    printf("学生信息:\n");
    printf("学号: %d\n", stu1.id);
    printf("姓名: %s\n", stu1.name);
    printf("年龄: %d\n", stu1.age);
    printf("成绩: %.1f\n", stu1.score);
    
    // 4. 初始化结构体
    struct Student stu2 = {1002, "王五", 21, 92.0};
    
    // 5. 使用typedef定义的结构体
    Book book1;
    strcpy(book1.title, "C语言程序设计");
    strcpy(book1.author, "张三");
    book1.price = 45.5;
    
    printf("\n图书信息:\n");
    printf("书名: %s\n", book1.title);
    printf("作者: %s\n", book1.author);
    printf("价格: %.2f元\n", book1.price);
    
    // 6. 结构体数组
    struct Student class[3] = {
        {1001, "小明", 18, 85.5},
        {1002, "小红", 19, 90.0},
        {1003, "小刚", 20, 78.5}
    };
    
    printf("\n班级学生信息:\n");
    for(int i = 0; i < 3; i++) {
        printf("%s: %.1f分\n", class[i].name, class[i].score);
    }
    
    // 7. 结构体指针
    struct Student *stuPtr = &stu1;
    printf("\n通过指针访问:\n");
    printf("姓名: %s\n", stuPtr->name);  // 使用->访问成员
    printf("成绩: %.1f\n", (*stuPtr).score);  // 使用(*ptr).访问成员
    
    return 0;
}
```

</details>

<details>
<summary>5. 指针（点击展开）</summary>

```c
#include <stdio.h>

int main() {
    // 1. 基本指针
    int num = 100;
    int *ptr = &num;  // ptr指向num的地址
    
    printf("变量num的值: %d\n", num);
    printf("变量num的地址: %p\n", &num);
    printf("指针ptr的值（存储的地址）: %p\n", ptr);
    printf("通过指针访问的值: %d\n", *ptr);  // 解引用
    
    // 2. 修改指针指向的值
    *ptr = 200;
    printf("修改后num的值: %d\n", num);
    
    // 3. 指针运算
    int arr[5] = {10, 20, 30, 40, 50};
    int *arrPtr = arr;  // 指向数组首元素
    
    printf("\n数组元素:\n");
    for(int i = 0; i < 5; i++) {
        printf("arr[%d] = %d, 地址: %p\n", i, *(arrPtr + i), arrPtr + i);
    }
    
    // 4. 指针与函数
    int a = 10, b = 20;
    printf("\n交换前: a=%d, b=%d\n", a, b);
    swap(&a, &b);  // 传递地址
    printf("交换后: a=%d, b=%d\n", a, b);
    
    // 5. 指针与数组
    char str[] = "Hello";
    char *strPtr = str;
    
    printf("\n字符串: ");
    while(*strPtr != '\0') {
        printf("%c", *strPtr);
        strPtr++;  // 指针移动到下一个字符
    }
    printf("\n");
    
    // 6. 指针数组
    char *names[] = {"张三", "李四", "王五"};
    printf("\n指针数组:\n");
    for(int i = 0; i < 3; i++) {
        printf("names[%d] = %s\n", i, names[i]);
    }
    
    // 7. 指向指针的指针
    int value = 300;
    int *p1 = &value;
    int **p2 = &p1;  // 指向指针的指针
    
    printf("\n多级指针:\n");
    printf("value的值: %d\n", value);
    printf("通过p1访问: %d\n", *p1);
    printf("通过p2访问: %d\n", **p2);
    
    // 8. 动态内存分配
    int *dynamicArr = (int*)malloc(5 * sizeof(int));
    
    if(dynamicArr != NULL) {
        for(int i = 0; i < 5; i++) {
            dynamicArr[i] = (i + 1) * 10;
        }
        
        printf("\n动态数组:\n");
        for(int i = 0; i < 5; i++) {
            printf("dynamicArr[%d] = %d\n", i, dynamicArr[i]);
        }
        
        free(dynamicArr);  // 释放内存
        dynamicArr = NULL;
    }
    
    return 0;
}

// 交换两个变量的值
void swap(int *x, int *y) {
    int temp = *x;
    *x = *y;
    *y = temp;
}
```

</details>

* 好了,你已经学会了.
  * 动手操作吧
  
![](../../img/zdl.jpg)
