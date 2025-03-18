#include <iostream>
#include <set>
using namespace std;

//插入元素
//insert()函数  
//删除元素 
//erase()函数 
//查找元素  
//find()函数  
//size()函数  
//清空集合  
//clear()函数  
//判断集合是否为空
//empty()函数  
//交集、并集、差集、对称差集  

int main() {
    set<int> st;
    st.insert(1);
    st.insert(2);   
    st.insert(3);
    st.insert(4);
    st.insert(20);

    for(auto it :st){
        cout<<it<<" ";
    }
    cout<<endl;

    if(st.find(2)!=st.end()){
        cout<<"存在2"<<endl;
    }

    st.erase(20);
    cout<<"删除20后"<<endl;
    for(auto it :st){
        cout<<it<<" ";
    }
    cout<<endl;
    st.clear();
    if(st.empty()){
        cout<<"集合为空"<<endl;
    }
    else{
        cout<<"集合不为空"<<endl;
        cout<<"集合大小为"<<st.size()<<endl;
    }
    cout<<endl;
    return 0;
}