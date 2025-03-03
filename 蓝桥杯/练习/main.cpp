#include <stdio.h>

int main(){
	int num = 0;
	for(int i=1;i<=9;i++)
	if(i!=4)
		for(int j=0;j<=9;j++)
		if(j!=4)
			for(int k=0;k<=9;k++)
			if(k!=4)
				for(int l=0;l<=9;l++)
				if(l!=4)
					for(int m=0;m<=9;m++)
					if(m!=4)
					num++;
	printf("%d",num);
	return 0;
} 
