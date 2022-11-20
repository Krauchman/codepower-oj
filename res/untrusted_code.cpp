#include <iostream>

using namespace std;

int main() {

    int a, b;
    cin >> a >> b;

    int res = 0;
    for (int i = 1; i <= b; ++i) {
        res += a;
    }

    cout << res << endl;

    return 0;
}
