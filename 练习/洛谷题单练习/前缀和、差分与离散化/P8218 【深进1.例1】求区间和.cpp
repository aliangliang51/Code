#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
#define N 100001
ll prefix[N];

int main(){
ll arr[N],n;
cin>>n;
for (int i=1;i<=n;i++){
    cin>>arr[i];
}
for(int i=1;i<=n;i++){
    prefix[i]=prefix[i-1]+arr[i];
}
ll l,r,m;
cin>>m;
for(int i=0;i<m;i++){
    cin>>l>>r;
    cout<<prefix[r]-prefix[l-1]<<endl;
}

}