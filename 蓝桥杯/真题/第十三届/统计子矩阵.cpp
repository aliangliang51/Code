#include <iostream>
#define n 100
using namespace std;
typedef long long ll;

ll prefix[n][n];
ll N,M,K; 
ll arr[n][n];
int main()
{
	ll sum=0;
	cin>>N>>M>>K; 
	for(ll i=1;i<=N;i++){
		for(ll j=1;j<=M;j++)
		{
			cin >> arr[i][j];
			prefix[i][j]=prefix[i-1][j]+prefix[i][j-1]-prefix[i-1][j-1]+arr[i][j];
			if(prefix[i][j]<=K)
			sum++;
		}
	}
	cout<<sum;
  return 0;
}