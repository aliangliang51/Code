#include <iostream>
#include <math.h>
typedef long long ll;
using namespace std;

int main(){
	// ll a,b;
	// cin>>a>>b;

	ll arr[5]={1,2,3,4,5};
	ll sum[6];
	sum[0]=0;

	for(int i=1;i<=5;i++){
		sum[i]=sum[i-1]+arr[i-1];
	}
	for(int i=0;i<=5;i++){
		cout<<sum[i]<<" ";
	}

	return 0;
} 