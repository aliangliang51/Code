#include <iostream>
using namespace std;
int main() {
	long long a,b,n,per;
	cin>>a>>b>>n;
	long long count=0;
	
	per = a*5+b*2;//ÿ�� 
	count = n/per*7; //�����˼��� 
	n %= per;//��ʣ����
	
	//��Ϊ���������ܴ��ڳ�������˿�������д
	if(n<=a*5){
		count += n/a*5 +(n%a != 0);//�������ʽ��Ϊ��ȷ����1 
	}
	else{
		n-=a*5;
		count += 6+(n>b);
	} 
	
	
	
	cout << count;
	
	return 0;
}
