#include <bits/stdc++.h>
using namespace std;



bool pd(int x){
	int a=x,t;
	int flag=1;
	while(a){
		t = a%10;
		a/=10;
		if(flag==1){
			if(t%2!=0){
				flag=0;
				continue;
			}
			else return false;
		}else if(flag==0)
			if(t%2==0){
			flag=1;
			continue;
			}
			
		else return false;
	}
	return true;
}

int main(){
	int n;
	cin>>n;
	int sum=0;
	for(int i=1;i<=n;i++){
		if(pd(i))
		sum++;	
	}
	cout<<sum;
	return 0;
}
