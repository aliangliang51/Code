#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main()
{
  ll n = 2021041820210418;
  ll j,k;
  ll sum=0;
  for (ll i = 1;i*i*i<=n;i++)
  if(n%i==0)
  for(j=i;i*j*j<=n;j++)
  if(n/i%j==0){
  	k = n/i/j;
  	if(i==k&&i==k) sum++;
  	if(i==j||i==k||j==k) sum+=3;
  	else sum+=6;
  }
  cout<<sum;

  return 0;
}
