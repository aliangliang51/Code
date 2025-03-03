#include <iostream>
using namespace std;
int main() {
	long long a,b,n;
	cin>>a>>b>>n;
	long long sum=0,count=1;
	int i=1,j=1;
	int flag=1;
	while(flag==1) {
		for(; i<6; i++) {
			sum+=a;
			if(sum<n)
				count++;
			else {
				flag=0;
				break;
			}
		}
		if(i==6)
			for(; j<3; j++) {
				sum+=b;
				if(sum<n)
					count++;
				else {
					flag=0;
					break;
				}
			}
		if(i==6&&j==3)
			i=j=1;

	}
	cout<<count;
	return 0;
}
