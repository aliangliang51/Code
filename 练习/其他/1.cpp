#include <iostream>

using namespace std;

int main(){
    int n[10]={1,2,3,4,5,6,7,8,9,10};

    for(auto i : n){
        cout<<i<<" ";
    }
    cout<<endl;
    for(int i : n){
        cout<<i<<" ";
    }
    return 0;
}
