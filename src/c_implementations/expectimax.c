#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <time.h>
#include <math.h>
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
    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            printf("%d,", board[4*y+x]);
        }
        printf("\n");
    }
    printf("\n");
}

double max_value(int* board, int depth) {
    if (depth == 0 || is_impossible(board)) {
        printf("eval: %d depth: %d impossible: %d\n", (int) evaluation_function(board), depth, is_impossible(board));
        return evaluation_function(board);
    }

    double v = -INT_MAX;
    int successor_amount = 4;
    int** successors = generate_successors_max(board);

    for (int i=0; i < successor_amount; i++) {
        if(successors[i][15]==-1) {
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
        printf("eval: %d depth: %d impossible: %d\n", (int) evaluation_function(board), depth, is_impossible(board));
        return evaluation_function(board);
    }
    int successor_amount = amount_of_successors(board);
    int** successors = generate_successors_chance(board);

    double vs = 0;
    int count = 0;

    for (int i=0; i < successor_amount; i++) {
        double probability = (successor_tiles[i] == 2) ? 0.9 : 0.1;
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
        printf("should never not have a move here");
        move = random_num(4);
    }

    int did_slide = slides(move, board, 1);
    int did_collide = collides(move, board, 1);

    if (did_collide==1) {
        slides(move, board, 0);
    }

    int did_move = did_slide || did_collide;

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
                x = 3 - i;

                move_modifier = RIGHT_VECTOR;
            } else {
                x = i;
            }
            if (action==DOWN) {
                y = 3 - j;
                move_modifier = DOWN_VECTOR;
            } else {
                y = j;
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
                x = 3 - i;
                move_modifier = RIGHT_VECTOR;
            } else {
                x = i;
            }
            if (action==DOWN) {
                y = 3 - j;
                move_modifier = DOWN_VECTOR;
            } else {
                y = j;
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
    return ((smoothness(board) * 0.23) + maxTile(board) +
            (log(freeTiles(board)) * 2.3) + maxPlacement(board) +
            (order(board) * 1.9));
}

double maxPlacement(int* board) {
    double maxPlacementH = 0;

    double maxTileValue = 0;
    double maxTileIndex = 0;

    for (int i = 0; i < 16; i++) {
        int tile = board[i];

        if (tile > maxTileValue) {
            maxTileValue = tile;
            maxTileIndex = i;
        }

         // Not in the middle
        if (maxTileIndex != 5 && maxTileIndex != 6 &&
                maxTileIndex != 9 && maxTileIndex != 10) {
            maxPlacementH = maxTileValue;

             // In a corner
            if (maxTileIndex == 0 || maxTileIndex == 3 ||
                    maxTileIndex == 12 || maxTileIndex == 15) {
                maxPlacementH = maxTileValue * 2.4;
            }
        }
    }

    return maxPlacementH;
}

double maxTile(int* board) {
    double maxTile = 0;

    for (int i = 0; i < 16; i++) {
        if (board[i] > maxTile) {
            maxTile = board[i];
        }
    }

    return maxTile;
}

int get_neighbour_value(int* board, int pos_x, int pos_y, int direction) {
    if(direction==LEFT) {
        if(pos_x==0) {
            return 0;
        }
        for (int x = pos_x - 1; x >= 0; x--) {
            if (board[4*pos_y+x] == 0) { continue; }

            return board[4*pos_y+x];
        }
        return 0;
    } else if(direction==UP) {
        if(pos_y==0) {
            return 0;
        }
        for (int y = pos_y - 1; y >= 0; y--) {
            if (board[4*y+pos_x] == 0) { continue; }

            return board[4*y+pos_x];
        }
        return 0;
    } else if(direction==RIGHT) {
        if (pos_x == 3) { return 0; }
        for (int x = pos_x + 1; x <= 3; x++) {
            if (board[4*pos_y+x] == 0) { continue; }

            return board[4*pos_y+x];
        }
        return 0;
    } else if(direction==DOWN) {
        if (pos_y == 3) { return 0; }
        for (int y = pos_y + 1; y <= 3; y++) {
            if (board[4*y+pos_x] == 0) { continue; }

            return board[4*y+pos_x];
        }
        return 0;
    }
    return 0;
}

double smoothness(int *board) {
    double smoothness = 0;

    for (int x = 0; x < 4; x++) {
        for (int y = 0; y < 4; y++) {
            if (board[4*y+x] == 0) {
                continue;
            }

            int value = board[4*x+y];

            for (int m = 0; m < 4; m++) {
                int target_val = get_neighbour_value(board, x, y, m);
                if (target_val != 0) {
                    smoothness -= abs(value - target_val);
                }
            }
        }
    }

    return smoothness;
}

double order(int* board) {
    double totals[] = {0.0, 0.0 ,0.0, 0.0};

    for (int i = 0; i < 4; i++) { // Check up and down
        int current = 0;
        int next = current + 1;

        while (next < 4) {
            while ((next < 4) && !checkOccupied(board, i, next)) {
                next++;
            }

            if (next >= 4) { next--; }

            double currentValue = 0;
            double nextValue = 0;

            if (checkOccupied(board, i, current)) {
                currentValue = getNodeValue(board, i, current);
            }

            if (checkOccupied(board, i, next)) {
                nextValue = getNodeValue(board, i, next);
            }

            if (currentValue > nextValue) {
                totals[0] += nextValue - currentValue;
            } else if (nextValue > currentValue) {
                totals[1] += currentValue - nextValue;
            }

            current = next;
            next++;
        }
    }


    for (int j = 0; j < 4; j++) { // Check left and right
        int current = 0;
        int next = current + 1;

        while (next < 4) {
            while ((next < 4) && !checkOccupied(board, j, next)) {
                next++;
            }

            if (next >= 4) { next--; }

            double currentValue = 0;
            double nextValue = 0;

            if (checkOccupied(board, current, j)) {
                currentValue = getNodeValue(board, current, j);
            }

            if (checkOccupied(board, next, j)) {
                nextValue = getNodeValue(board, next, j);
            }

            if (currentValue > nextValue) {
                totals[2] += nextValue - currentValue;
            } else if (nextValue > currentValue) {
                totals[3] += currentValue - nextValue;
            }

            current = next;
            next++;
        }
    }

    int total_up_down = (totals[0] > totals[1]) ? totals[0] : totals[1];
    int total_left_right = (totals[2] > totals[3]) ? totals[2] : totals[3];

    return total_up_down + total_left_right;
}

int getNodeValue(int* board, int posX, int posY) {
    int withinX = (posX >= 0) && (posX < 4);
    int withinY = (posY >= 0) && (posY < 4);

    return (withinX && withinY) ? board[4 * posY + posX] : 0;
}

int checkOccupied(int* board, int posX, int posY) {
    return getNodeValue(board, posX, posY) != 0;
}

double freeTiles(int* board) {
    double free = 0;

    for (int i = 0; i < 16; i++) {
        if (board[i] == 0) {
            free++;
        }
    }

    return free;
}

int amount_of_successors(int* board) {
    return freeTiles(board) * 2;
}

int** generate_successors_max(int* board) {
    num_successors = 0;
    int** successors = malloc(4 * sizeof(int*));

    for (int m=0; m<4; m++) {
        int* successor = malloc(16 * sizeof(int));
        memcpy(successor, board, 16 * sizeof(int));

        if (move(m, successor)==0) {
            successor[15] = -1;
        }
        successors[m] = successor;
        num_successors++;
    }

//    printf("board\n");
//
//    for (int i = 0; i < 16; i++) {
//        printf("%d, ", board[i]);
//    }
//
//    printf("\n");
//
//    printf("successors\n");
//
//    for (int j = 0; j < num_successors; j++) {
//        for (int i = 0; i < 16; i++) {
//            printf("%d, ", successors[j][i]);
//        }
//        printf("\n");
//    }
//
//    printf("\n");

    return successors;
}

int** generate_successors_chance(int* board) {
    num_successors = 0;
    Vector zero_tiles[16];
    int count = 0;

    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            if (board[4*y+x]==0) {
                Vector xy;
                xy.x = x;
                xy.y = y;
                zero_tiles[count] = xy;
                count++;
            }
        }
    }

    int** successors = malloc(2 * count * sizeof(int*));
    int num_possibilities = 2;
    int possibilities[2] = { 2, 4 };

    for (int i=0; i < count; i++) {
        for (int p=0; p < num_possibilities; p++) {
            int* successor = malloc(16 * sizeof(int));
            memcpy(successor, board, 16 * sizeof(int));
            successor[4*zero_tiles[i].y+zero_tiles[i].x] = possibilities[p];

            successors[num_successors] = successor;
            successor_tiles[num_successors] = possibilities[p];
            num_successors++;
        }
    }
    return successors;
}

int* perform_action(int action, int* board) {
    int* new_game = malloc(16 * sizeof(int));
    memcpy(new_game, board, 16 * sizeof(int));

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
    int* start_board = malloc(16 * sizeof(int));

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
/*
int main() {
    int board[16] = {1, 0, 0, 0, 0, 0, 1, 1, 5, 5, 5, 3, 0, 3, 0, 0};
    int dec = decision(4, board[0], board[1], board[2], board[3], board[4], board[5],
                            board[6], board[7], board[8], board[9], board[10], board[11],
                            board[12], board[13], board[14], board[15]);
    printf("%d\n", dec);

    int* next_board = (int*) malloc(sizeof(int)*16);

    for (int i = 0; i < 16; i++) {
        next_board[i] = board[i];
    }

    move(dec, next_board);
    print_board(next_board);

    for (int i=0; i<50; i++) {
        for (int i = 0; i < 16; i++) {
            board[i] = next_board[i];
        }

        if (is_impossible(next_board)) {
            printf("Finished after %d moves\n", i);
            break;
        }

        int dec = decision(4, board[0], board[1], board[2], board[3], board[4], board[5],
                            board[6], board[7], board[8], board[9], board[10], board[11],
                            board[12], board[13], board[14], board[15]);

        move(dec, next_board);

        for (int i = 0; i < 16; i++) {
            if (next_board[i] == 0) {
                next_board[i] = 1;
                break;
            }
        }

        print_board(next_board);
        printf("%d\n", dec);
    }
}
*/
//int main() {
    // int board[16] = {};
//    printf("%d", decision(4, 1, 0, 0, 0, 0, 0, 1, 1, 5, 5, 5, 3, 0, 3, 0, 0));
//}
//
//    printf("%d", decision(board, 6));
//}
