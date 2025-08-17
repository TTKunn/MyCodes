#include <iostream>
#include <exception>
using namespace std;

double Divide(int a, int b){
    // 当b == 0时抛出异常
    if (b == 0)
        throw "Divide by zero condition!";
    else
        return (double)a / (double)b;
}

void Func(){
    int* array1 = new int[10];
    int* array2 = new int[10];  // 抛异常呢
    try{
        int len, time;
        cin >> len >> time;
        cout << Divide(len, time) << endl;
    }
    catch (...){
        cout << "delete []" << array1 << endl;
        cout << "delete []" << array2 << endl;
        delete[] array1;
        delete[] array2;
        throw; // 异常重新抛出，捕获到什么抛出什么
    }
    cout << "delete []" << array1 << endl;
    delete[] array1;
    cout << "delete []" << array2 << endl;
    delete[] array2;
}

int main(){
    try{
        Func();
    }
    catch (const char* errmsg){
        cout << errmsg << endl;
    }
    catch (const exception& e){
        cout << e.what() << endl;
    }
    catch (...){
        cout << "未知异常" << endl;
    }

    return 0;
}