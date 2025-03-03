#include <iostream>
using namespace std;

int main(){
	for(int a=1;a<=9;a++){
		for(int b=0;b<=9;b++){
			if (b!=a){
				for(int c=0;c<=9;c++){
					if(c!=b && c!=a){
						for(int d=0;d<=9;d++){
							if(d!=c &&d!=b &&d!=a){
								for(int e=1;e<=9;e++){
									if(e!=d &&e!=c &&e!=b&&e!=a){
										for(int f=0;f<=9;f++){
											if(f!=e &&f!=d &&f!=c &&f!=b&&f!=a){
												for(int g=0;g<=9;g++){
													if(g!=f&&g!=e &&g!=d &&g!=c &&g!=b&&g!=a){
														for(int h=0;h<=9;h++){
															if(h!=g && h!=f&&h!=e &&h!=d &&h!=c &&h!=b&&h!=a){
																int x=a*1000+b*100+c*10+d;
																int y=e*1000+f*100+g*10+b;
																int z=e*10000+f*1000+c*100+b*10+h;
																if(x+y==z)
																printf("%d %d %d\n",x,y,z);
															}
														}
													}
												}
											}
										}
									}
								}
							}
						}
					
					}	
				}	
			}
		
		}
	}
	
}

