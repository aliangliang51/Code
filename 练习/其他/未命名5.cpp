#include <iostream>
using namespace std;
typedef long long ll;
int main()
{
  ll n,h;
  int hh,mm,ss;
  cin>>n;
  h = n%(1000*60*60*24);
  hh = h/(1000*60*60)%24;
  mm = h/(1000*60)%60;
  ss = h/(1000)%60;
  cout<<hh<<endl;
  cout<<mm<<endl;
  cout<<ss<<endl;
  printf("%02d:%02d:%02d",hh,mm,ss);
  return 0;
}
