#include <bits/stdc++.h> 
using namespace std;

int main()
{
	int a,b,x,y;
	cin>>a>>b>>x>>y;
	int m_min = min(a,b);
	int y_min=0,x_min=0;
//	y打完最小的
	int y_b=b,y_a=a;
	do{
		y_b-=y;
		y_a-=y;
		y_min++;
	}while(y_b>0);
	while(y_a>0){
		y_a-=x;
		y_min++;
	}

	x_min=((a+b)/x);
	if(x%(a+b)!=0)
	x_min++;
	
	cout<<min(x_min,y_min);
	return 0;
}
