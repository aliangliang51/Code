#include <iostream>
#define n 100
using namespace std;
typedef long long ll;

ll prefix[n];
ll N,M,K; 
ll arr[n][n];
int main()
{
	for(ll i=1;i<=N;i++){
		for(ll j=1;j<=M;j++)
		{
			cin >> arr[i][j]; 
		}
	}
	ll sum=0;
	for(ll i=1;i<=N;i++)
	for(ll j=1;j<=M;j++){
		prefix[i][j]=prefix[i][j-1]+arr[i][j];
		if(prefix[i][j]<=K)
		sum++;
	}
	for(ll j=1;j<=M;j++)
	for(ll i=1;i<=N;i++)
	{
		prefix[i][j]=prefix[i-1][j]+arr[i][j];
		if(prefix[i][j]<=K)
		sum++;
	}
	cout<<sum;
  return 0;
}
