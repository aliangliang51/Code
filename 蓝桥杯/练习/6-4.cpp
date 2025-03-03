#include <iostream>
using namespace std;

int main(){
	int n,x,y;
	int xy2,xy1;
	cin>>n>>xy1>>xy2; 
	int arr[(xy1+xy2)/n][n]={0};
	int flag=1;
	for(int i=0;i<(xy1+xy2)/n;i++){
		if(i%2!=0){
			for(int a=n;a>1;a--){
				arr[i][a]=flag;
				flag++;
			} 
		}
		else{
			for(int a=0;a<n;a++){
				arr[i][a]=flag;
				flag++;
			}
		}
	}
	for(int i=0;i<=(xy1+xy2)/n;i++){
		for(int j=0;j<=n;j++){
	    	printf("%4d ",arr[i][j]);
	    }
	    printf("\n");
	}
	
	return 0;
} 
