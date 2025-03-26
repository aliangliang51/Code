#include <iostream>
using namespace std;
typedef long long ll;
int main()
{
  ll n;
  ll x=0,count=0,flag=1,sum=0;
  cin>>n;
  while(sum<n)
  {
  	count++;
  	sum+=flag;
  	flag++;
  }
  
  cout<<count; 
  return 0;
}
