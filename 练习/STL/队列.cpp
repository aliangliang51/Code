#include <iostream>
#include <queue>

using namespace std;

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