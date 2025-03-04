#include <iostream>
using namespace std;
int main() {
	long long a,b,n,per;
	cin>>a>>b>>n;
	long long count=0;
	
	per = a*5+b*2;//每天 
	count = n/per; //进行了几周 
	n %= per;//还剩几题
	
	//因为余数不可能大于除数，因此可以这样写
	if(n<=a*5){
		count += n/a*5 +(n%a != 0);
	}
	else{
		n-=a*5;
		count += 6+(n>b);
	} 
	
	
	
	cout << count;
	
	return 0;
}
