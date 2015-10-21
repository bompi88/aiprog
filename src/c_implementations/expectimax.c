#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <time.h>
#include "expectimax.h"

typedef struct {
    int x;
    int y;
} Vector;

int LEFT = 0;
int UP = 1;
int RIGHT = 2;
int DOWN = 3;
int LEFT_VECTOR[2] = { -1, 0 };
int UP_VECTOR[2] = { 0, -1 };
int RIGHT_VECTOR[2] = { 1, 0 };
int DOWN_VECTOR[2] = { 0, 1 };

int successor_tiles[50];
int num_successors = 0;

int random_num(int max) {
    return rand() % max;
}

void print_board(int* board) {
    for (int i=0; i<4; i++) {
        for (int j=0; j<4; j++) {
            printf("%d,", board[4*i+j]);
        }
        printf("\n");
    }
    printf("\n");
}

double max_value(int* board, int depth) {
    if (depth == 0 || is_impossible(board)) {
        return evaluation_function(board);
    }

    double v = -INT_MAX;
    int successor_amount = 4;
    int** successors = generate_successors_max(board);

    for (int i=0; i < successor_amount; i++) {
        double value = chance_node(successors[i], depth - 1);

        if (value > v) {
            v = value;
        }
        // free(successors[i]); // TODO: Is this necessary?
    }

    return v;
}

double chance_node(int* board, int depth) {
    if (depth == 0 || is_impossible(board)) {
        return evaluation_function(board);
    }
    int successor_amount = amount_of_successors(board);
    int** successors = generate_successors_chance(board);

    double vs = 0;
    int count = 0;

    for (int i=0; i < successor_amount; i++) {
        double probability = successor_tiles[i];
        double value = probability *  max_value(successors[i], depth - 1);

        vs = vs + value;
        count++;
        // free(successors[i]); // TODO: Is this necessary?
    }

    return vs / (double)count;
}

int is_in_range(int num, int start, int end) {
    if ((num >= start) && (num <= end)) {
        return 1;
    } else {
        return 0;
    }
}

int move(int move, int* board) {

    if (!move) {
        move = random_num(4);
    }

    int did_slide = slides(move, board, 1);
    int did_collide = collides(move, board, 1);

    int did_slides_after_collision = 0;

    if (did_collide==1) {
        did_slides_after_collision = slides(move, board, 0);
    }

    int did_move = did_slide || did_collide || did_slides_after_collision;

    return did_move;
}

int slides(int action, int* board, int perform) {
    int did_move = 0;

    for (int i=0; i<4; i++) {
        for (int j=0; j<4; j++) {
            int x = 0;
            int y = 0;
            int* move_modifier;
            Vector move_to;

            if (action==LEFT) {
                move_modifier = LEFT_VECTOR;
            }
            if (action==UP) {
                move_modifier = UP_VECTOR;
            }
            if (action==RIGHT) {
                x = 3 - j;
                move_modifier = RIGHT_VECTOR;
            } else {
                x = j;
            }
            if (action==DOWN) {
                y = 3 - i;
                move_modifier = DOWN_VECTOR;
            } else {
                y = i;
            }

            if (board[4*x+y]==0) {
                continue;
            }

            move_to.x = x + move_modifier[0];
            move_to.y = y + move_modifier[1];

            int tile = 4 * y + x;

            if (action==LEFT) {
                for (int x_new=0; x_new < move_to.x + 1; x_new++) {
                    int new_tile = 4*move_to.y+x_new;
                    if (is_in_range(x_new, 0, 3)) {
                        if (board[new_tile]==0) {
                            if (perform==1) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            } else if (action==RIGHT) {

                for (int x_new=3; x_new > move_to.x - 1; x_new--) {
                    int new_tile = 4*move_to.y+x_new;
                    if (is_in_range(x_new, 0, 3)) {
                        if (board[new_tile]==0) {

                            if (perform==1) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            } else if (action==UP) {
                for (int y_new=0; y_new < move_to.y + 1; y_new++) {
                    int new_tile = 4*y_new+x;
                    if (is_in_range(y_new, 0, 3)) {
                        if (board[new_tile]==0) {
                            if (perform==1) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            } else if (action==DOWN) {
                for (int y_new=3; y_new > move_to.y - 1; y_new--) {
                    int new_tile = 4*y_new+x;
                    if (is_in_range(y_new, 0, 3)) {
                        if (board[new_tile]==0) {
                            if (perform==1) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            }
        }
    }

    return did_move;
}

int collides(int action, int* board, int perform) {
    int x = 0;
    int y = 0;
    int collision = 0;
    int* move_modifier;

    for (int i=0; i<4; i++) {
        for (int j=0; i<4; i++) {
            if (action==LEFT) {
                move_modifier = LEFT_VECTOR;
            }
            if (action==UP) {
                move_modifier = UP_VECTOR;
            }
            if (action==RIGHT) {
                x = 3 - j;
                move_modifier = RIGHT_VECTOR;
            } else {
                x = j;
            }
            if (action==DOWN) {
                y = 3 - i;
                move_modifier = DOWN_VECTOR;
            } else {
                y = i;
            }

            Vector neighbour;

            neighbour.x = x + move_modifier[0];
            neighbour.y = y + move_modifier[1];

            if (is_in_range(neighbour.x, 0, 3) && is_in_range(neighbour.y, 0, 3)) {
                if (board[4*x+y]==0) {
                    continue;
                }
                if (board[4*neighbour.x+neighbour.y]==board[4*x+y]) {
                    if (perform==1) {
                        board[4*x+y] *= 2;
                        board[4*neighbour.x+neighbour.y] = 0;
                    }
                    collision = 1;
                }
            }
        }
    }

    return collision;
}

int is_impossible(int* board) {
    int impossible = 1;

    for (int m=0; m<4; m++) {
        if (slides(m, board, 0)) {
            impossible = 0;
            break;
        }
        if (collides(m, board, 0)) {
            impossible = 0;
            break;
        }
    }

    return impossible;
}

double evaluation_function(int* board) {
    if (is_impossible(board)==1) {
        return 0;
    }

    // TODO: Write heuristics

    return 1;
}

int amount_of_successors(int* board) {
    int count = 0;

    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            if (board[4*x+y]==0) {
                count++;
            }
        }
    }

    return count * 2;
}

int** generate_successors_max(int* board) {
    num_successors = 0;
    int** successors = (int**) malloc(sizeof(int*)*4);

    for (int m=0; m<4; m++) {
        int* successor = (int*) malloc(sizeof(int)*16);
        memcpy(successor, board, sizeof(int)*16);

        if (move(m, successor)==1) {
            successors[m] = successor;
            num_successors++;
        } else {
            successors[m] = -1;
        }
    }

    return successors;
}

int** generate_successors_chance(int* board) {
    num_successors = 0;
    Vector zero_tiles[16];
    int count = 0;

    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            if (board[4*x+y]==0) {
                Vector xy;
                xy.x = x;
                xy.y = y;
                zero_tiles[count] = xy;
                count++;
            }
        }
    }

    int** successors = (int**) malloc(sizeof(int*)*count*2);
    int num_possibilities = 2;
    int possibilities[2] = { 2, 4 };

    for (int i=0; i < count; i++) {
        for (int p=0; p < num_possibilities; p++) {
            int* successor = (int*) malloc(sizeof(int)*16);
            memcpy(successor, board, sizeof(int)*16);
            successor[4*zero_tiles[i].x+zero_tiles[i].y] = possibilities[p];

            successors[num_successors] = successor;
            successor_tiles[num_successors] = possibilities[p];
            num_successors++;
        }
    }
    return successors;
}

int* perform_action(int action, int* board) {
    int* new_game = (int*) malloc(sizeof(int)*16);
    memcpy(new_game, board, sizeof(int)*16);

    int did_move = move(action, board);

    if (did_move==1) {
        return new_game;
    } else {
        board[15] = -1;
        return board;
    }
}

int decision(int* board, int depth) {
    srand(time(0));
    double max_val = -INT_MAX;
    int max_action = -1;

    for (int a=0; a < 4; a++) {
        board = perform_action(a, board);

        if (board[15] == -1) {
            continue;
        }

        double value = max_value(board, depth);

        if (value > max_val) {
            max_val = value;
            max_action = a;
        }
    }

    return max_action;
}

//int main() {
//    int arr[16] = {3, 4, 0, 1, 2, 4, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0};
//    printf("%d\n", INT_MIN);
//    printf("%d\n", decision(arr, 4));
//}