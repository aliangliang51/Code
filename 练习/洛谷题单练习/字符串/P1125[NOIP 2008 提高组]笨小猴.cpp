#include <bits/stdc++.h>

using namespace std;
string s;
int sum[100];
int m;

bool pd(int x){
    if(x==2 || x==3 || x==5 || x==7 || x==11 || x==13 || x==17 || x==19 || x==23 || x==29 || x==31 || x==37 || x==41 || x==43 || x==47 || x==53 || x==59 || x==61 || x==67 || x==71 || x==73 || x==79 || x==83 || x==89 || x==97){
        return true;
    }
    return false;
}

int main(){

    cin >> s;
    int n = s.size();
    for(int i=0;i<n;i++){
        if(s[i]!='\0')
            sum[m]=1;
        for(int j=i+1;j<n;j++){
            if(s[j]==s[i]&&s[j]!='\0'){
                sum[m]++;
                s[j]='\0';
            }
        }
        m++;
    }
    int max = sum[0];
    int min = sum[0];
    for(int i=0;i<m;i++){
        if(max<sum[i]){
            max = sum[i];
        }
        if(min>sum[i] && sum[i]!=0){
            min = sum[i];
        }
    }
    int flag = max - min;

    if(flag==0||flag==1){
        cout<<"No Answer"<<endl<<0;
    }
    else if(pd(flag)) {
        cout<<"Lucky Word"<<endl<<flag;
    }
    else{
        cout<<"No Lucky Word"<<endl<<0;
    }
    
    return 0;
}