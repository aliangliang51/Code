#include <iostream>
#include <map>
#include <stack>

using namespace std;

int main(){
    map<int ,char> mp;//定义一个map容器，其中int为键，char为值
    map<char,stack<int>> stk;
    mp[1]='a';mp[2]='b';mp[3]='c';mp[4]='d';mp[5]='e';mp[6]='f';mp[7]='g';mp[8]='h';mp[9]='i';mp[10]='j';//插入元素
    // stk['a']=stack<int>();//初始化栈
    stk['a'].push(1);
    cout<<stk['a'].top()<<endl;

    //获取值
    char val = mp[1];
    cout<<val<<endl;


    //遍历map容器
    for(auto it : mp){
        //first输出是键，second输出是值
        cout<<it.first<<" "<<it.second<<endl;
    }
//    for(auto it=mp.begin();it!=mp.end();it++){

//    }

    return 0;
}

