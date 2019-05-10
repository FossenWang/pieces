/*
Simple unit test framework.

Define TestCase and add it to TestCase array:

#include "unittest.h"
viod test_wrong()
{
    assert_msg(0, 'Wrong!');
}
TestCase tests[] = {test_wrong};

Run tests:

int main
{
    run_all_tests(tests);
    return 0
}
*/

#include <stdio.h>
#include <assert.h>

// Assert the "expression", if false, "message" will be printed to "stderr" and exit.
#define assert_msg(expression, message)             \
    do                                              \
    {                                               \
        if (!(expression))                          \
        {                                           \
            fprintf(stderr, "\n---------------\n"); \
            fprintf(stderr, (message));             \
            fprintf(stderr, "\n\n");                \
            assert(expression);                     \
        }                                           \
    } while (0)

// Run all unittests, tests must be "TestCase tests[]".
#define run_all_tests(tests)                        \
    do                                              \
    {                                               \
        int i;                                      \
        int len = sizeof(tests) / sizeof(tests[0]); \
        for (i = 0; i < len; i++)                   \
        {                                           \
            tests[i]();                             \
        }                                           \
        printf("\n---------------\n");              \
        printf("ALL %d TESTS PASSED\n", len);       \
    } while (0)

typedef void (*TestCase)();

extern TestCase tests[];
