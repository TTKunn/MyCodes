#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <memory>
#include <cstdio>

using namespace std;

// �������ڽṹ�壬������ʾ��Դ����
struct Date
{
    int _year;
    int _month;
    int _day;

    // ���캯������ʼ������
    Date(int year = 1, int month = 1, int day = 1)
        : _year(year)
        , _month(month)
        , _day(day)
    {
        cout << "Date(" << _year << "," << _month << "," << _day << ")" << endl;
    }

    // �������������ڹ۲�����ͷ�
    ~Date()
    {
        cout << "~Date(" << _year << "," << _month << "," << _day << ")" << endl;
    }
};

// 1. ������ʽ��ɾ�����������ͷŶ�̬����
template<class T>
void DeleteArrayFunc(T* ptr)
{
    cout << "DeleteArrayFunc: �ͷ�����" << endl;
    delete[] ptr;  // �����ͷű�����delete[]
}

// 2. �������󣨷º�������ʽ��ɾ�����������ͷŶ�̬����
template<class T>
class DeleteArray
{
public:
    // ����()�������ʹ���������һ������
    void operator()(T* ptr)
    {
        cout << "DeleteArray: �ͷ�����" << endl;
        delete[] ptr;
    }
};

// 3. ��Դ����ר��ɾ���������ڹر��ļ�
class Fclose
{
public:
    void operator()(FILE* ptr)
    {
        if (ptr)
        {
            cout << "Fclose: �ر��ļ�ָ�� " << ptr << endl;
            fclose(ptr);  // �ļ���Դ������fclose�ͷ�
        }
    }
};

int main()
{
    // һ������̬���飨Ĭ��ɾ���������ã����Զ��壩
    // ����1����������ָ��������ػ��汾���Զ�ʹ��delete[]��
    cout << "\n--- �����ػ��汾 ---" << endl;
    unique_ptr<Date[]> up1(new Date[3]);  // unique_ptr���������ػ�
    shared_ptr<Date[]> sp1(new Date[3]);  // C++17��shared_ptrҲ֧�������ػ�

    // ����2��ʹ�ú���������Ϊɾ����
    cout << "\n--- ��������ɾ���� ---" << endl;
    // unique_ptr��ɾ������ģ�������������ʽָ������
    unique_ptr<Date, DeleteArray<Date>> up2(new Date[3]);
    // shared_ptr��ɾ�����ǹ����������Ӱ������
    shared_ptr<Date> sp2(new Date[3], DeleteArray<Date>());

    // ����3��ʹ�ú���ָ����Ϊɾ����
    cout << "\n--- ����ָ��ɾ���� ---" << endl;
    unique_ptr<Date, void(*)(Date*)> up3(new Date[3], DeleteArrayFunc<Date>);
    shared_ptr<Date> sp3(new Date[3], DeleteArrayFunc<Date>);

    // ����4��ʹ��lambda���ʽ��Ϊɾ����
    cout << "\n--- lambdaɾ���� ---" << endl;
    auto delArrLambda = [](Date* ptr) {
        cout << "lambda: �ͷ�����" << endl;
        delete[] ptr;
        };
    // unique_ptr��Ҫ��decltype��ȡlambda����
    unique_ptr<Date, decltype(delArrLambda)> up4(new Date[3], delArrLambda);
    shared_ptr<Date> sp4(new Date[3], delArrLambda);

    // ����������ڴ���Դ���ļ������
    cout << "\n--- �����ļ���Դ ---" << endl;
    // ʹ�ú���������Ϊɾ����
    shared_ptr<FILE> sp5(fopen("test.txt", "w"), Fclose());
    // ʹ��lambda��Ϊɾ����������ࣩ
    shared_ptr<FILE> sp6(fopen("test.txt", "w"), [](FILE* ptr) {
        if (ptr) {
            cout << "lambda: �ر��ļ�ָ�� " << ptr << endl;
            fclose(ptr);
        }
        });

    cout << "\n--- ������� ---" << endl;
    return 0;
}
