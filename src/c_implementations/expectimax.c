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
        if(successors[i][16]==-1) {
            continue;
        }

        double value = chance_node(successors[i], depth - 1);

        if (value > v) {
            v = value;
        }
    }

    free(successors);

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
    }

    free(successors);

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

    if (move==-1) {
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

            if (board[4*y+x]==0) {
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
        for (int j=0; j<4; j++) {
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

            neighbour.x = x - move_modifier[0];
            neighbour.y = y - move_modifier[1];

            int tile = 4 * y + x;

            if (is_in_range(neighbour.x, 0, 3) && is_in_range(neighbour.y, 0, 3)) {
                if (board[tile]==0) {
                    continue;
                }

                int neighbour_tile = 4 * neighbour.y + neighbour.x;

                if (board[neighbour_tile]==board[tile]) {
                    if (perform==1) {
                        board[tile] += 1;
                        board[neighbour_tile] = 0;
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

    int mask[16*4] = {
                        // Top left
                        10, 9, 8, 7,
                        9, 6, 5, 4,
                        8, 5, 3, 2,
                        7, 4, 2, 1,
                        // Top right
                        7, 8, 9, 10,
                        4, 5, 6, 9,
                        2, 3, 5, 8,
                        1, 2, 4, 7,
                        // Bottom right
                        1, 2, 4, 7,
                        2, 3, 5, 8,
                        4, 5, 6, 9,
                        7, 8, 9, 10,
                        // Bottom left
                        7, 4, 2, 1,
                        8, 5, 3, 2,
                        9, 6, 5, 4,
                        10, 9, 8, 7};

    int grid_component = INT_MIN;

    int h = 0;
    for(int k=0; k<4; k++) {
        for (int y = 0; y < 4; y++) {
            for (int x = 0; x < 4; x++) {
                int tile = 4 * y + x;
                h += (int)mask[(k * 16) + tile] * (int)board[tile];

                if(h>grid_component) {
                    grid_component = h;
                }
                double free_tiles_component = amount_of_successors(board) / (double) 16;

                return ((double)grid_component) / free_tiles_component;
            }
        }
    }
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

        if (move(m, successor)==0) {
            successor[16] = -1;
        }
        successors[m] = successor;
        num_successors++;
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

    int did_move = move(action, new_game);

    if (did_move==1) {
        return new_game;
    } else {
        // print_board(board);
        new_game[15] = -1;
        return new_game;
    }
}

int decision(int depth, int b0, int b1, int b2, int b3, int b4, int b5, int b6,
                        int b7, int b8, int b9, int b10, int b11, int b12,
                        int b13, int b14, int b15) {
    srand(time(0));
    double max_val = -INT_MAX;
    int max_action = -1;
    int arg_board[] = {b0, b1, b2, b3, b4, b5, b6, b7, b8,
                       b9, b10, b11, b12, b13, b14, b15};
    int* start_board = (int*) malloc(sizeof(int)*16);

    for (int i = 0; i < 16; i++) {
        start_board[i] = arg_board[i];
    }

    // int* board = &start_board;

    for (int a=0; a < 4; a++) {
        int *board = perform_action(a, start_board);

        if (board[15] == -1) {
            continue;
        }

        double value = max_value(board, depth);

        if (value > max_val) {
            max_val = value;
            max_action = a;
        }
        free(board);
    }
    free(start_board);

    return max_action;
}

int decision_map(int depth, int* board) {
    return decision(depth, board[0], board[1], board[2], board[3], board[4], board[5], board[6], board[7],
                    board[8], board[9], board[10], board[11], board[12], board[13], board[14], board[15]);
}

//int main() {
    // int board[16] = {};
//    printf("%d", decision(4, 1, 0, 0, 0, 0, 0, 1, 1, 5, 5, 5, 3, 0, 3, 0, 0));
//}
//
//    printf("%d", decision(board, 6));
//}