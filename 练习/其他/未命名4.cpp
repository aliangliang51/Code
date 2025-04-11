#include<bits/stdc++.h>
using namespace std; 
typedef long long LL;

int gcd(int a,int b)
{
	if(a % b==0) return b;
	else return gcd(b,a%b);
}

int lcm(int a,int b){
	int temp = a*b;
	int res = temp/gcd(a,b);
	return res; 

}



int main()
{
    int a=1,b=2021;
    int min=2021;
	for(int a=1;a<=2021;a++)
	for(int b=1;b<=2021;b++){
		if(b-a>=21)
		break;
		else{
			int t = lcm(a,b);
			if(min>t)
			min=t;
		}
		
	} 
	cout<<min;
    
//    while(1){
//    	int a,b;
//    	cin>>a>>b;
//    	cout<<lcm(a,b)<<endl;
//	}
    
    
    return 0;
}
