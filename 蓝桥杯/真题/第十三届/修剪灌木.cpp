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
  
  // ���ڴ��������Ĵ���
  return 0;
}
