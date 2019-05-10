#include "unittest.h"

void f1()
{
    printf("1");
    // set 0 to raise error
    assert_msg(1, "Wrong!!!!!!!!!");
}
void f2() { printf("2"); }
void f3() { printf("3"); }

TestCase tests[] = {
    f1,
    f2,
    f3,
};

int main()
{
    run_all_tests(tests);
    return 0;
}
