#include <bits/stdc++.h>
using namespace std;
int main()
{
  int N;
  cin>>N;
  
  for(int i=0;i<N;i++)
  {
  	int x = max(N-i,i-1)*2;
  	cout<<x<<endl;
  }
  
  // 请在此输入您的代码
  return 0;
}
