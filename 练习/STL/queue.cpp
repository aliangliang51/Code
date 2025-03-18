#include <iostream>
#include <queue>

using namespace std;

//队列的基本操作
//push(element):在队尾添加元素
//pop():在队头删除元素
//front():返回队头元素
//back():返回队尾元素
//empty():判断队列是否为空
//size():返回队列的大小

int main(){
    queue<int> q;
    //在队尾添加元素
    q.push(1);
    q.push(2);
    q.push(3);
    q.push(4);
    q.push(5);

    cout<<q.front()<<" ";
    cout<<q.back()<<" "<<endl;

    while(!q.empty()){
    //在队头删除元素
    q.pop();
    cout<<"头部元素"<<q.front()<<" ";
    cout<<"尾部元素"<<q.back()<<" ";
    cout<<"长度"<<q.size()<<endl;
    }
    

    return 0;
}