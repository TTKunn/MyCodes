#include <iostream>
#include <memory>

// �����õļ���
class MyClass {
public:
    MyClass(int id) : id_(id) {
        std::cout << "MyClass(" << id_ << ") ����" << std::endl;
    }
    ~MyClass() {
        std::cout << "MyClass(" << id_ << ") ����" << std::endl;
    }
    void print() {
        std::cout << "���� MyClass(" << id_ << ")" << std::endl;
    }
    int getId() const { return id_; }

private:
    int id_;
};

int main() {
    // 1. ����unique_ptr
    std::unique_ptr<MyClass> ptr1(new MyClass(1));

    // 2. operator->() �� operator*()
    std::cout << "\n--- ʹ�� operator->() �� operator*() ---" << std::endl;
    ptr1->print();       // ͨ��->���ʳ�Ա����
    (*ptr1).print();     // ͨ��*���ʶ�����

    // 3. get() - ��ȡԭʼָ�루��ת������Ȩ��
    std::cout << "\n--- ʹ�� get() ---" << std::endl;
    MyClass* raw_ptr = ptr1.get();
    std::cout << "ԭʼָ�����: ";
    raw_ptr->print();    // ����ʹ��ԭʼָ�룬������Ȩ������ptr1

    // 4. swap() - ��������unique_ptr������Ȩ
    std::cout << "\n--- ʹ�� swap() ---" << std::endl;
    std::unique_ptr<MyClass> ptr2(new MyClass(2));
    std::cout << "����ǰ: ";
    ptr1->print();
    ptr2->print();

    ptr1.swap(ptr2);
    std::cout << "������: ";
    ptr1->print();
    ptr2->print();

    // 5. reset() - ����ָ�루���Զ��ͷ�ԭ�ж���
    std::cout << "\n--- ʹ�� reset() ---" << std::endl;
    ptr1.reset(new MyClass(3));  // �ͷ�ԭ�ж���(2)��ָ���¶���(3)
    ptr1->print();

    ptr1.reset();  // �ͷŶ���(3)��ָ���Ϊnullptr
    if (!ptr1) {
        std::cout << "ptr1 ����Ϊ��" << std::endl;
    }

    // 6. release() - �ͷ�����Ȩ�����ֶ������ڴ棩
    std::cout << "\n--- ʹ�� release() ---" << std::endl;
    MyClass* released_ptr = ptr2.release();  // ptr2�ͷ�����Ȩ����Ϊnullptr
    std::cout << "release() ���ص�ָ��: ";
    released_ptr->print();

    delete released_ptr;  // �����ֶ��ͷţ������ڴ�й©

    std::cout << "\n�������" << std::endl;
    return 0;
}
