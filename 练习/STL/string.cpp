#include <iostream>
#include <string>

using namespace std;

int main(){
    string s1("hello");
    string a = "aa";

    // 使用迭代器版本
    s1.insert(s1.begin(), 'a');
    cout << s1 << endl; // 输出结果为 "aahello"
    s1.insert(s1.begin(), 1, 'a'); // 在开头插入两个字符 'a'
    cout << s1 << endl; // 输出结果为 "aaaahello"
    // 使用下标版本
    s1.insert(0, a);
    cout << s1 << endl; // 输出结果为 "aaaahello"

    return 0;
}
