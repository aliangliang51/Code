#include <bits/stdc++.h>
using namespace std;

const int N = 100010;

int a[N];
int prefix[N];

int main(){
	int n,i=1;
	cin>>n;
	for(int i=1;i<=n;i++){
	cin>>a[i];
	prefix[i]=prefix[i-1]+a[i];	
	} 
	
	int m,l,r;
	cin>>m;
	while(m--){
		cin>>l>>r;
		cout<<prefix[r]-prefix[l-1];
	}
	
	return 0;
}
