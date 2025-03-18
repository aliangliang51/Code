#include <iostream>
#include <stack>
using namespace std;

//基本操作
// push(x) 压栈
// pop() 弹栈
// top() 返回栈顶元素
// empty() 判断栈是否为空
// size() 返回栈的大小
int main(){
    // stack<int> s; // 声明栈
    stack<int> s;
    // s.push(1); // 压栈
    s.push(1);
    s.push(2);
    s.push(3);
    s.push(4);
    s.push(5);
    cout<<s.top()<<endl; // 栈顶元素
    //判断栈是否为空
    while(!s.empty()){
        s.pop(); // 弹栈
        cout<<" "<<s.size()<<endl;// 栈大小

    }



    return 0;
}