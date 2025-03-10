#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
#define N 10

ll prefix[N];


int main(){
    
    ll arr[N]={1,2,3,4,5,6,7,8,9,10};
    ll n;
    cin>>n;
    for(int i=1;i<=n;i++){
        prefix[i]=prefix[i-1]+arr[i];
    }
    ll l,r;
    cin>>l>>r;
    cout<<prefix[r]-prefix[l-1]<<endl;
    return 0;
}