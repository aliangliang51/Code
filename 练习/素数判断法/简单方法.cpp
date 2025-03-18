#include <iostream>
using namespace std;

bool isPrime(int n){
    for(int i=2;i<n;i++){
        if(n%i==0){
            return false;
        }
    }
    return true;
}

int main(){
    int n;
    cin>>n;
    if(isPrime(n))
        cout<<"是素数"<<endl;
    else
        cout<<"不是素数"<<endl;
    return 0;

}