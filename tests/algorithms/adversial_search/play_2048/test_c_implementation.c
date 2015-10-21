#include <check.h>
#include <stdlib.h>
#include "expectimax.h"

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
        int board[16] = {2, 4, 0, 0,
                         0, 0, 8, 0,
                         0, 0, 0, 0,
                         0, 0, 0, 0};
        int solution1[16] = {0, 0, 2, 4,
                             0, 0, 0, 8,
                             0, 0, 0, 0,
                             0, 0, 0, 0};
        int did_move = 0;

        // Move right
        did_move = slides(2, board, 1);
        ck_assert_int_eq(did_move, 1);
        did_move = 0;

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution1[i]);
        }

        int solution2[16] = {0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 4,
                             0, 0, 2, 8};

        // Move down
        did_move = slides(3, board, 1);
        ck_assert_int_eq(did_move, 1);
        did_move = 0;

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution2[i]);
        }

        int solution3[16] = {0, 0, 0, 0,
                             0, 0, 0, 0,
                             4, 0, 0, 0,
                             2, 8, 0, 0};

        // Move left
        did_move = slides(0, board, 1);
        ck_assert_int_eq(did_move, 1);
        did_move = 0;

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution3[i]);
        }

        int solution4[16] = {4, 8, 0, 0,
                             2, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 0};

        // Move up
        did_move = slides(1, board, 1);
        ck_assert_int_eq(did_move, 1);
        did_move = 0;

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution4[i]);
        }
    }
END_TEST

START_TEST (test_collides)
    {
        int board[16] = {2, 2, 0, 0,
                         0, 4, 3, 0,
                         0, 0, 0, 0,
                         0, 3, 3, 4};
        int solution1[16] = {0, 0, 0, 3,
                             0, 0, 4, 3,
                             0, 0, 0, 0,
                             0, 0, 4, 4};
        int did_collide = 0;

        // Move right
        slides(2, board, 1);
        did_collide = collides(2, board, 1);
        ck_assert_int_eq(did_collide, 1);
        did_collide = 0;
        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution1[i]);
        }


        int solution2[16] = {0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 4,
                             0, 0, 5, 4};

        // Move down
        slides(3, board, 1);
        did_collide = collides(3, board, 1);
        ck_assert_int_eq(did_collide, 1);
        did_collide = 0;

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution2[i]);
        }

        int solution3[16] = {0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 5, 5};

        // Move down
        slides(3, board, 1);
        did_collide = collides(3, board, 1);
        ck_assert_int_eq(did_collide, 1);
        did_collide = 0;

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution3[i]);
        }

        int solution4[16] = {0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 6};

        // Move right
        slides(2, board, 1);
        did_collide = collides(2, board, 1);
        ck_assert_int_eq(did_collide, 1);

        for (int i=0; i < 16; i++) {
            ck_assert_int_eq(board[i], solution4[i]);
        }
    }
END_TEST

START_TEST (test_is_impossible)
    {
        // Test a possible board
        int board[16] = {2, 4, 0, 0,
                         0, 0, 8, 0,
                         0, 0, 0, 0,
                         0, 0, 0, 0};
        int impossible = is_impossible(board);
        ck_assert_int_eq(impossible, 0);

        // Test an impossible board
        int impossible_board[16] = {2, 4, 2, 4,
                                    4, 2, 4, 2,
                                    2, 4, 2, 4,
                                    4, 2, 4, 2};
        impossible = is_impossible(impossible_board);
        ck_assert_int_eq(impossible, 1);

    }
END_TEST

START_TEST (test_amount_of_successors)
    {
        // Should have 26 successors
        int board[16] = {2, 4, 0, 0,
                         0, 0, 8, 0,
                         0, 0, 0, 0,
                         0, 0, 0, 0};
        int num_successors = amount_of_successors(board);
        ck_assert_int_eq(num_successors, 26);

        // Should have no successors
        int impossible_board[16] = {2, 4, 2, 4,
                                    4, 2, 4, 2,
                                    2, 4, 2, 4,
                                    4, 2, 4, 2};
        num_successors = amount_of_successors(impossible_board);
        ck_assert_int_eq(num_successors, 0);
    }
END_TEST

START_TEST (test_move)
    {
        // Should have 26 successors
        int board[16] = {2, 4, 0, 0,
                         0, 0, 8, 0,
                         0, 0, 0, 0,
                         0, 0, 0, 0};

        // After a move to the left
        int left[16] = {2, 4, 0, 0,
                        8, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 0};

        // After a move to the right
        int right[16] = {0, 0, 2, 4,
                         0, 0, 0, 8,
                         0, 0, 0, 0,
                         0, 0, 0, 0};

        // After a move downwards
        int down[16] = {0, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 4,
                        0, 0, 2, 8};

        // After a move upwards
        int up[16] = {0, 0, 2, 4,
                      0, 0, 0, 8,
                      0, 0, 0, 0,
                      0, 0, 0, 0};

        int did_move = move(0, board);
        ck_assert_int_eq(did_move, 1);

        for (int i = 0; i < 16; i++) {
            ck_assert_int_eq(left[i], board[i]);
        }

        did_move = move(2, board);
        ck_assert_int_eq(did_move, 1);

        for (int i = 0; i < 16; i++) {
            ck_assert_int_eq(right[i], board[i]);
        }

        did_move = move(3, board);
        ck_assert_int_eq(did_move, 1);

        for (int i = 0; i < 16; i++) {
            ck_assert_int_eq(down[i], board[i]);
        }

        did_move = move(1, board);
        ck_assert_int_eq(did_move, 1);

        for (int i = 0; i < 16; i++) {
            ck_assert_int_eq(up[i], board[i]);
        }
    }
END_TEST

START_TEST (test_generate_successors_max)
    {
        int board[16] = {2, 4, 0, 0,
                         0, 0, 8, 0,
                         0, 0, 0, 0,
                         0, 0, 0, 0};

        int after_gen[16] = {2, 4, 0, 0,
                             0, 0, 8, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 0};

        int** successors = generate_successors_max(board);

        // Test if old board not modified
        for (int i = 0; i < 16; i++) {
            ck_assert_int_eq(board[i], after_gen[i]);
        }

        // After a move to the left
        int left[16] = {2, 4, 0, 0,
                        8, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 0};

        // After a move to the right
        int right[16] = {0, 0, 2, 4,
                         0, 0, 0, 8,
                         0, 0, 0, 0,
                         0, 0, 0, 0};

        // After a move upwards
        int up[16] = {2, 4, 8, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0};

        // After a move downwards
        int down[16] = {0, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 0,
                        2, 4, 8, 0};

        // Check if all successors have been successfully generated
        for (int j = 0; j < 16; j++) {
            ck_assert_int_eq(right[j], successors[2][j]);
            ck_assert_int_eq(left[j], successors[0][j]);
            ck_assert_int_eq(down[j], successors[3][j]);
            ck_assert_int_eq(up[j], successors[1][j]);

        }
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
    tcase_add_test(tc_core, test_move);
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