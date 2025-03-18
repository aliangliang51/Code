#include <iostream>
#include <map>
#include <stack>
using namespace std;

//基本操作
//1.插入元素：map[key] = value;
//2.获取元素：value = map[key];
//3.删除元素：map.erase(key);
//4.遍历容器：for(auto it : map){...}
//5.判断元素是否存在：if(map.count(key)){...}
//6.获取map大小：map.size()
//7.清空容器：map.clear()


int main(){
    map<int ,char> mp;//定义一个map容器，其中int为键，char为值
    map<char,stack<int>> stk;
    mp[1]='a';mp[2]='b';mp[3]='c';mp[4]='d';mp[5]='e';mp[6]='f';mp[7]='g';mp[8]='h';mp[9]='i';mp[10]='j';//插入元素
    // stk['a']=stack<int>();//初始化栈
    stk['a'].push(1);
    cout<<stk['a'].top()<<endl;
    cout<<"stk长度"<<stk.size()<<endl;

    //获取值
    char val = mp[1];
    cout<<val<<endl;


    //遍历map容器
    cout<<"删除前的map大小："<<mp.size()<<endl;
    for(auto it : mp){
        //first输出是键，second输出是值
        cout<<"删除前的键值对："<<it.first<<" "<<it.second<<endl;
    }
    
//    for(auto it=mp.begin();it!=mp.end();it++){
    cout<<endl;
//    }
    //删除元素
    mp.erase(1);
    cout<<"删除后的map大小："<<mp.size()<<endl;
    for (auto it : mp){
        cout<<"删除后的键值对："<<it.first<<""<<it.second<<endl;
    }
    return 0;
}

