#include <iostream>
#include <memory>

// 测试用的简单类
class MyClass {
public:
    MyClass(int id) : id_(id) {
        std::cout << "MyClass(" << id_ << ") 构造" << std::endl;
    }
    ~MyClass() {
        std::cout << "MyClass(" << id_ << ") 析构" << std::endl;
    }
    void print() {
        std::cout << "这是 MyClass(" << id_ << ")" << std::endl;
    }
    int getId() const { return id_; }

private:
    int id_;
};

int main() {
    // 1. 构造unique_ptr
    std::unique_ptr<MyClass> ptr1(new MyClass(1));

    // 2. operator->() 和 operator*()
    std::cout << "\n--- 使用 operator->() 和 operator*() ---" << std::endl;
    ptr1->print();       // 通过->访问成员函数
    (*ptr1).print();     // 通过*访问对象本身

    // 3. get() - 获取原始指针（不转移所有权）
    std::cout << "\n--- 使用 get() ---" << std::endl;
    MyClass* raw_ptr = ptr1.get();
    std::cout << "原始指针访问: ";
    raw_ptr->print();    // 可以使用原始指针，但所有权仍属于ptr1

    // 4. swap() - 交换两个unique_ptr的所有权
    std::cout << "\n--- 使用 swap() ---" << std::endl;
    std::unique_ptr<MyClass> ptr2(new MyClass(2));
    std::cout << "交换前: ";
    ptr1->print();
    ptr2->print();

    ptr1.swap(ptr2);
    std::cout << "交换后: ";
    ptr1->print();
    ptr2->print();

    // 5. reset() - 重置指针（会自动释放原有对象）
    std::cout << "\n--- 使用 reset() ---" << std::endl;
    ptr1.reset(new MyClass(3));  // 释放原有对象(2)，指向新对象(3)
    ptr1->print();

    ptr1.reset();  // 释放对象(3)，指针变为nullptr
    if (!ptr1) {
        std::cout << "ptr1 现在为空" << std::endl;
    }

    // 6. release() - 释放所有权（需手动管理内存）
    std::cout << "\n--- 使用 release() ---" << std::endl;
    MyClass* released_ptr = ptr2.release();  // ptr2释放所有权，变为nullptr
    std::cout << "release() 返回的指针: ";
    released_ptr->print();

    delete released_ptr;  // 必须手动释放，否则内存泄漏

    std::cout << "\n程序结束" << std::endl;
    return 0;
}
