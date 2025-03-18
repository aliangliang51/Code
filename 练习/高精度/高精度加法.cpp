#include <bits/stdc++.h>

using namespace std;
const int N = 100010;

int a[N],b[N];
int al,bl;

void add(int a[],int &al,int b[],int &bl){
    int t = 0;
    al = max(al,bl);
    for(int i=0;i<al;i++){
        t += a[i] + b[i];
        a[i] = t%10;
        t /=10;
    }
    if(t) a[al] = 1;
    while(al > 0 && a[al]==1) al--;
}

int main(){
    string x,y;
    cin>>x>>y;
    
    for(int i=x.size()-1;i>=0;i--) a[al++] = x[i]-'0';
    for(int i=y.size()-1;i>=0;i--) b[bl++] = y[i]-'0';

    add(a,al,b,bl);

    for(int i=al;i>=0;i--) cout<<a[i];

}