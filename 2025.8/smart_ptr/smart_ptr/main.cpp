#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <memory>
#include <cstdio>

using namespace std;

// 定义日期结构体，用于演示资源管理
struct Date
{
    int _year;
    int _month;
    int _day;

    // 构造函数，初始化日期
    Date(int year = 1, int month = 1, int day = 1)
        : _year(year)
        , _month(month)
        , _day(day)
    {
        cout << "Date(" << _year << "," << _month << "," << _day << ")" << endl;
    }

    // 析构函数，用于观察对象释放
    ~Date()
    {
        cout << "~Date(" << _year << "," << _month << "," << _day << ")" << endl;
    }
};

// 1. 函数形式的删除器：用于释放动态数组
template<class T>
void DeleteArrayFunc(T* ptr)
{
    cout << "DeleteArrayFunc: 释放数组" << endl;
    delete[] ptr;  // 数组释放必须用delete[]
}

// 2. 函数对象（仿函数）形式的删除器：用于释放动态数组
template<class T>
class DeleteArray
{
public:
    // 重载()运算符，使对象可像函数一样调用
    void operator()(T* ptr)
    {
        cout << "DeleteArray: 释放数组" << endl;
        delete[] ptr;
    }
};

// 3. 资源管理专用删除器：用于关闭文件
class Fclose
{
public:
    void operator()(FILE* ptr)
    {
        if (ptr)
        {
            cout << "Fclose: 关闭文件指针 " << ptr << endl;
            fclose(ptr);  // 文件资源必须用fclose释放
        }
    }
};

int main()
{
    // 一、管理动态数组（默认删除器不适用，需自定义）
    // 方案1：利用智能指针的数组特化版本（自动使用delete[]）
    cout << "\n--- 数组特化版本 ---" << endl;
    unique_ptr<Date[]> up1(new Date[3]);  // unique_ptr对数组有特化
    shared_ptr<Date[]> sp1(new Date[3]);  // C++17后shared_ptr也支持数组特化

    // 方案2：使用函数对象作为删除器
    cout << "\n--- 函数对象删除器 ---" << endl;
    // unique_ptr的删除器是模板参数，必须显式指定类型
    unique_ptr<Date, DeleteArray<Date>> up2(new Date[3]);
    // shared_ptr的删除器是构造参数，不影响类型
    shared_ptr<Date> sp2(new Date[3], DeleteArray<Date>());

    // 方案3：使用函数指针作为删除器
    cout << "\n--- 函数指针删除器 ---" << endl;
    unique_ptr<Date, void(*)(Date*)> up3(new Date[3], DeleteArrayFunc<Date>);
    shared_ptr<Date> sp3(new Date[3], DeleteArrayFunc<Date>);

    // 方案4：使用lambda表达式作为删除器
    cout << "\n--- lambda删除器 ---" << endl;
    auto delArrLambda = [](Date* ptr) {
        cout << "lambda: 释放数组" << endl;
        delete[] ptr;
        };
    // unique_ptr需要用decltype获取lambda类型
    unique_ptr<Date, decltype(delArrLambda)> up4(new Date[3], delArrLambda);
    shared_ptr<Date> sp4(new Date[3], delArrLambda);

    // 二、管理非内存资源（文件句柄）
    cout << "\n--- 管理文件资源 ---" << endl;
    // 使用函数对象作为删除器
    shared_ptr<FILE> sp5(fopen("test.txt", "w"), Fclose());
    // 使用lambda作为删除器（更简洁）
    shared_ptr<FILE> sp6(fopen("test.txt", "w"), [](FILE* ptr) {
        if (ptr) {
            cout << "lambda: 关闭文件指针 " << ptr << endl;
            fclose(ptr);
        }
        });

    cout << "\n--- 程序结束 ---" << endl;
    return 0;
}
