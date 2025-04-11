#include <bits/stdc++.h>

using namespace std;
int t,n;
int flag;
long long sum[100010]; 
int swap(string a,int n){
	int l=0,r=n*2-1;
	int count=0;
	while(n--){
		do{
			l++;
		}while(a[l-1]!=a[l]&&l<n);
		do{
			r--;
		}while(a[r+1]!=a[r]&&r>=n);
		
		if(l<r){
		char tm = a[l];
		a[l]=a[r];
		a[r]=tm;
		count++;
		} 
		if(l>r) break; 
	}
	
	return count;
}

int main(){
	string a;
	cin>>t;
	
	for(int i=0;i<t;i++){
		cin>>n;
		cin>>a;
		sum[i]=swap(a,n);
	} 
	for(int i=0;i<t;i++){
		cout<<sum[i]<<endl;
	}
	
	return 0; 
} 
