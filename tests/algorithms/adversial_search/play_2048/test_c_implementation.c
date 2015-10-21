#include <check.h>
#include <stdlib.h>
#include <expectimax.h>

START_TEST (test_copy_and_edit_new_array)
    {
        int array[16] = {1, 2, 3, 4};
        int solution_array[16] = {1, 2, 3, 4};
        int solution_array_new[16] = {4, 3, 2, 1};

        int* array_new = (int*) malloc(sizeof(int)*16);
        memcpy(array_new, array, sizeof(int)*16);

        array_new[0] = 4;
        array_new[1] = 3;
        array_new[2] = 2;
        array_new[3] = 1;

        ck_assert_int_eq(array_new[0], solution_array_new[0]);
        ck_assert_int_eq(array_new[1], solution_array_new[1]);
        ck_assert_int_eq(array_new[2], solution_array_new[2]);
        ck_assert_int_eq(array_new[3], solution_array_new[3]);

        ck_assert_int_eq(array[0], solution_array[0]);
        ck_assert_int_eq(array[1], solution_array[1]);
        ck_assert_int_eq(array[2], solution_array[2]);
        ck_assert_int_eq(array[3], solution_array[3]);
    }
END_TEST

START_TEST (test_array_of_arrays)
    {
        int array[16] = {1, 2, 3, 4};
        int solution_array[16] = {1, 2, 3, 4};
        int solution_array_new[16] = {8, 3, 5, 2};

        int* array_new = (int*) malloc(sizeof(int)*16);
        memcpy(array_new, array, sizeof(int)*16);

        array_new[0] = 8;
        array_new[1] = 3;
        array_new[2] = 5;
        array_new[3] = 2;

        int** array_of_arrays = (int**) malloc(sizeof(int*)*2);

        array_of_arrays[0] = array;
        array_of_arrays[1] = array_new;

        ck_assert_int_eq(array_of_arrays[1][0], solution_array_new[0]);
        ck_assert_int_eq(array_of_arrays[1][1], solution_array_new[1]);
        ck_assert_int_eq(array_of_arrays[1][2], solution_array_new[2]);
        ck_assert_int_eq(array_of_arrays[1][3], solution_array_new[3]);

        ck_assert_int_eq(array_of_arrays[0][0], solution_array[0]);
        ck_assert_int_eq(array_of_arrays[0][1], solution_array[1]);
        ck_assert_int_eq(array_of_arrays[0][2], solution_array[2]);
        ck_assert_int_eq(array_of_arrays[0][3], solution_array[3]);

    }
END_TEST

START_TEST (test_slides)
    {
    }
END_TEST

START_TEST (test_collides)
    {
    }
END_TEST

START_TEST (test_is_impossible)
    {
    }
END_TEST

START_TEST (test_amount_of_successors)
    {
    }
END_TEST

START_TEST (test_generate_successors_max)
    {
    }
END_TEST

START_TEST (test_generate_successors_chance)
    {
    }
END_TEST

START_TEST (test_perform_action)
    {
    }
END_TEST

Suite *expectimax_suite(void) {
    Suite *s;
    TCase *tc_core;

    s = suite_create("Expectimax");
    tc_core = tcase_create("Core");

    tcase_add_test(tc_core, test_copy_and_edit_new_array);
    tcase_add_test(tc_core, test_array_of_arrays);
    tcase_add_test(tc_core, test_slides);
    tcase_add_test(tc_core, test_collides);
    tcase_add_test(tc_core, test_is_impossible);
    tcase_add_test(tc_core, test_amount_of_successors);
    tcase_add_test(tc_core, test_generate_successors_max);
    tcase_add_test(tc_core, test_generate_successors_chance);
    tcase_add_test(tc_core, test_perform_action);

    suite_add_tcase(s, tc_core);

    return s;
}

int main(void) {
    int number_failed;
    Suite *s;
    SRunner *sr;

    s = expectimax_suite();
    sr = srunner_create(s);

    srunner_run_all(sr, CK_NORMAL);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}