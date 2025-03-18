#include <iostream>
#include <vector>
using namespace std;

//基本操作
//1.插入元素：vec.push_back(value);
//2.获取元素：value = vec[index];
//3.删除元素：vec.erase(vec.begin()+index);
//4.遍历容器：for(int i=0;i<vec.size();i++){...}
//5.判断元素是否存在：if(find(vec.begin(),vec.end(),value)!=vec.end()){...}
//6.获取vec大小：vec.size()
//7.清空容器：vec.clear()

int main(){
    vector<int> vec;
    vec.push_back(3);
    vec.push_back(5);
    vec.push_back(7);
    vec.push_back(9);
    vec.push_back(11);

    cout<<"vec大小：" << vec.size() << endl;
    for(int i=0;i<vec.size();i++){
        cout<<vec[i]<<" ";
    }
    cout<<endl;
    cout<<"第一个元素：" << vec[0] << endl;
    cout<<"第一个元素：" << vec.at(0) << endl;
    cout<<"vec的大小：" << vec.size() << endl;

    for( auto it : vec){
        cout<<it<<" ";
    }
    cout<<endl;
    cout<<"删除第二个元素：";
    vec.erase(vec.begin()+1);
    for( auto it : vec){
        cout<<it<<" ";
    }
    cout<<endl;
    cout<<"vec的大小：" << vec.size() << endl;
    for(int v : vec){
        cout<<v<<" ";
    }
    cout<<endl;
    return 0;
}