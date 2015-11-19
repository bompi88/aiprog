#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "expectimax.h"

#define LEFT 0
#define UP 1
#define RIGHT 2
#define DOWN 3
#define BOARD_ARGS int b0, int b1, int b2, int b3, int b4, int b5, int b6, int b7, int b8, int b9, int b10, int b11, int b12, int b13, int b14, int b15
#define BOARD_ARGS_VALUES b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15
#define BOARD_ARGS_ELEMENTS board[0], board[1], board[2], board[3], board[4], board[5], board[6], board[7], board[8], board[9], board[10], board[11], board[12], board[13], board[14], board[15]
static int LEFT_VECTOR[2] = { -1, 0 };
static int UP_VECTOR[2] = { 0, -1 };
static int RIGHT_VECTOR[2] = { 1, 0 };
static int DOWN_VECTOR[2] = { 0, 1 };
static int NO_MOVE_VECTOR[2] = { 0, 0 };

#define TILE_0_VALUE 0
#define TILE_2_VALUE 1
#define TILE_4_VALUE 2

#define TRUE 1
#define FALSE 0
#define IS_FALSE ==0

#define HEURISTIC_CONSTANTS double smoothness, double max_tile, double free_tiles_multiplier, double max_placement, double monotonicity

static double smoothness_constant;
static double max_tile_constant;
static double free_tiles_constant;
static double max_placement_constant;
static double monotonicity_constant;

static int successor_tiles[32];
static int num_successors = 0;


int main() {
    int board[] = {0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    printf("%d\n", decision_map(2, board));
}

int decision(int depth, BOARD_ARGS, HEURISTIC_CONSTANTS) {
    srand((unsigned int)time(NULL));

    int arg_board[] = {BOARD_ARGS_VALUES};

    smoothness_constant = smoothness;
    max_tile_constant = max_tile;
    free_tiles_constant = free_tiles_multiplier;
    max_placement_constant = max_placement;
    monotonicity_constant = monotonicity;

    int* start_board = malloc(16 * sizeof(int));
    for (int i = 0; i < 16; i++) { start_board[i] = arg_board[i]; }

    ExpectimaxNode max_node = max_value(start_board, depth);

    free(start_board);

    return max_node.move;
}

int decision_map(int depth, int* board) {
    return decision(depth, BOARD_ARGS_ELEMENTS, 0.2, 0.9, 2.3, 1.0, 1.9);
}

ExpectimaxNode max_value(int* board, int depth) {
    int successor_amount = 4;
    int** successors = generate_successors_max(board);

    ExpectimaxNode v = create_expectimax_node(-1, INT_MIN);
    ExpectimaxNode current = create_expectimax_node(-1, INT_MIN);

    for (int i=0; i < successor_amount; i++) {
        if(successors[i][15]==-1) {
            continue;
        }

        if (depth IS_FALSE) {
            current.move = i;
            current.heuristic = evaluation_function(successors[i]);
        } else {
            current = chance_node(successors[i], depth - 1);
        }

        if (current.heuristic > v.heuristic) {
            v.move = i;
            v.heuristic = current.heuristic;
        }
    }

    for (int i=0; i < successor_amount; i++) {
        free(successors[i]);
    }

    free(successors);

    return v;
}

ExpectimaxNode chance_node(int* board, int depth) {
    int successor_amount = amount_of_successors(board);
    int** successors = generate_successors_chance(board);

    double vs = 0;
    double count = 0;

    for (int i=0; i < successor_amount; i++) {
        ExpectimaxNode node = max_value(successors[i], depth);
        double heuristic = node.heuristic;

        double probability = (successor_tiles[i] == TILE_2_VALUE) ? 0.9 : 0.1;
        double value = probability * heuristic;

        vs += value;
        count++;
    }

    for (int i = 0; i < successor_amount; i++) {
        free(successors[i]);
    }
    free(successors);

    return create_expectimax_node(-1, vs / count);
}

ExpectimaxNode create_expectimax_node(int move, double heuristic) {
    ExpectimaxNode node = {move, heuristic};
    return node;
}

int amount_of_successors(int* board) {
    int count = 0;

    for (int i = 0; i < 16; i++) {
        if (board[i] == TILE_0_VALUE) {
            count++;
        }
    }

    return count * 2;
}

int** generate_successors_max(int* board) {
    num_successors = 0;
    int** successors = malloc(4 * sizeof(int*));

    for (int m=0; m<4; m++) {
        int* successor = malloc(16 * sizeof(int));
        memcpy(successor, board, 16 * sizeof(int));

        if (move(m, successor) == 0) {
            successor[15] = -1;
        }
        successors[m] = successor;
        num_successors++;
    }

    return successors;
}

int** generate_successors_chance(int* board) {
    num_successors = 0;
    int zero_tiles[16];
    int count = 0;

    for (int i=0; i < 16; i++) {
        if (board[i] == 0) {
            zero_tiles[count] = i;
            count++;
        }
    }

    int** successors = malloc(2 * count * sizeof(int*));
    int num_possibilities = 2;
    int possibilities[2] = { 2, 4 };

    for (int i = 0; i < count; i++) {
        for (int p = 0; p < num_possibilities; p++) {
            int* successor = malloc(16 * sizeof(int));
            memcpy(successor, board, 16 * sizeof(int));

            int tile = 4 * (zero_tiles[i] / 4) + (zero_tiles[i] % 4);
            successor[tile] = possibilities[p];

            successors[num_successors] = successor;
            successor_tiles[num_successors] = possibilities[p];
            num_successors++;
        }
    }
    return successors;
}

int is_in_range(int num, int start, int end) {
    if ((num >= start) && (num <= end)) {
        return TRUE;
    } else {
        return FALSE;
    }
}

int move(int move, int* board) {
    int slid = slides(move, board, 1);
    int collided = collides(move, board, 1);

    if (collided) {
        slides(move, board, 1);
    }

    return slid || collided;
}

int slides(int action, int* board, int perform) {
    int did_move = FALSE;
    int x = 0;
    int y = 0;
    int* move_modifier = NO_MOVE_VECTOR;
    int move_to_x;
    int move_to_y;

    for (int i=0; i<4; i++) {
        for (int j=0; j<4; j++) {
            x = 0;
            y = 0;

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

            if (board[4*y+x]==TILE_0_VALUE) {
                continue;
            }

            move_to_x = x + move_modifier[0];
            move_to_y = y + move_modifier[1];

            int tile = 4 * y + x;

            if (action==LEFT) {
                for (int x_new=0; x_new < move_to_x + 1; x_new++) {
                    int new_tile = 4*move_to_y+x_new;
                    if (is_in_range(x_new, 0, 3)) {
                        if (board[new_tile]==0) {
                            if (perform) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = TRUE;
                            break;
                        }
                    }
                }
            } else if (action==RIGHT) {
                for (int x_new=3; x_new > move_to_x - 1; x_new--) {
                    int new_tile = 4*move_to_y+x_new;
                    if (is_in_range(x_new, 0, 3)) {
                        if (board[new_tile]==0) {

                            if (perform) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = TRUE;
                            break;
                        }
                    }
                }
            } else if (action==UP) {
                for (int y_new=0; y_new < move_to_y + 1; y_new++) {
                    int new_tile = 4*y_new+x;
                    if (is_in_range(y_new, 0, 3)) {
                        if (board[new_tile]==0) {
                            if (perform) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = TRUE;
                            break;
                        }
                    }
                }
            } else if (action==DOWN) {
                for (int y_new=3; y_new > move_to_y - 1; y_new--) {
                    int new_tile = 4*y_new+x;
                    if (is_in_range(y_new, 0, 3)) {
                        if (board[new_tile]==0) {
                            if (perform) {
                                board[new_tile] = board[tile];
                                board[tile] = 0;
                            }

                            did_move = TRUE;
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
    int collision = FALSE;
    int* move_modifier = NO_MOVE_VECTOR;
    int neighbour_x = 0;
    int neighbour_y = 0;

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

            neighbour_x = x - move_modifier[0];
            neighbour_y = y - move_modifier[1];

            int tile = 4 * y + x;

            if (is_in_range(neighbour_x, 0, 3) && is_in_range(neighbour_y, 0, 3)) {
                if (board[tile]==0) {
                    continue;
                }

                int neighbour_tile = 4 * neighbour_y + neighbour_x;

                if (board[neighbour_tile]==board[tile]) {
                    if (perform) {
                        board[tile] += 1;
                        board[neighbour_tile] = TILE_0_VALUE;
                    }
                    collision = TRUE;
                }
            }
        }
    }

    return collision;
}

int is_impossible(int* board) {
    int impossible = TRUE;

    for (int m=0; m<4; m++) {
        if (slides(m, board, 0)) {
            impossible = FALSE;
            break;
        }
        if (collides(m, board, 0)) {
            impossible = FALSE;
            break;
        }
    }

    return impossible;
}


int free_tiles(int* board) {
    int free_value = 0;

    for (int i = 0; i < 16; i++) {
        if (board[i] == 0) {
            free_value++;
        }
    }

    return free_value;
}

int max_tile(int* board) {
    int max_tile = 0;

    for (int i = 0; i < 16; i++) {
        if (board[i] > max_tile) {
            max_tile = board[i];
        }
    }

    return max_tile;
}

double evaluation_function(int* board) {
    if (is_impossible(board)) {
        return INT_MIN;
    }

    int modifier[] = {
            // Top left corner
            15, 14, 13, 12,
            8, 9, 10, 11,
            7, 6, 5, 4,
            0, 1, 2, 3,

            15, 8, 7, 0,
            14, 9, 6, 1,
            13, 10, 5, 2,
            12, 11, 4, 3,

            // Top right corner

            12, 13, 14, 15,
            11, 10, 9, 8,
            4, 5, 6, 7,
            3, 2, 1, 0,

            0, 7, 8, 15,
            1, 6, 9, 14,
            2, 5, 10, 13,
            3, 4, 11, 12,

            //Bottom left corner

            0, 1, 2, 3,
            7, 6, 5, 4,
            8, 9, 10, 11,
            15, 14, 13, 12,

            12, 11, 4, 3,
            13, 10, 5, 2,
            14, 9, 6, 1,
            15, 8, 7, 0,

            // Bottom right corner

            3, 2, 1, 0,
            4, 5, 6, 7,
            11, 10, 9, 8,
            12, 13, 14, 15,

            3, 4, 11, 12,
            2, 5, 10, 13,
            1, 6, 9, 14,
            0, 7, 8, 15
    };

    int sub = 15 - max_tile(board);

    int min_possibility = INT_MAX;

    for (int k = 0; k < 1; k++) {
        int sum = 0;

        for (int i = 0; i < 16; i++) {

            if (modifier[i+4*k] - sub > 0) {
                modifier[i+4*k] = sub - modifier[i+4*k];
            }

            if (board[i+4*k] == 0) {
                modifier[i+4*k] = 0;
            } else {
                modifier[i+4*k] = modifier[i+4*k] + board[i+4*k];
            }

            sum = sum + abs(modifier[i+4*k]);
        }

        if(sum < min_possibility) {
            min_possibility = sum;
        }
    }

    return (-(float)min_possibility + 1.5 * (float)free_tiles(board));
}

double max_placement(int* board) {
    double max_placement_h = 0;

    double max_tile_value = 0;
    int max_tile_index = 0;

    for (int i = 0; i < 16; i++) {
        int tile = board[i];

        if (tile > max_tile_value) {
            max_tile_value = tile;
            max_tile_index = i;
        }

         // Not in the middle
        if (max_tile_index != 5 && max_tile_index != 6 &&
                max_tile_index != 9 && max_tile_index != 10) {
            max_placement_h = 1;

             // In a corner
            if (max_tile_index == 0 || max_tile_index == 3 ||
                    max_tile_index == 12 || max_tile_index == 15) {
                max_placement_h = 2;
            }
        }
    }

    return max_placement_h;
}

double smoothness(int *board) {
    double smoothness = 0;

    for (int x = 0; x < 4; x++) {
        for (int y = 0; y < 4; y++) {
            if (board[4 * y + x] == 0) {
                continue;
            }

            int value = board[4 * y + x];

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

double monotonicity(int* board) {
    double totals[] = {0.0, 0.0 ,0.0, 0.0};

    int current = 0;
    int next = 0;

    double current_value = 0;
    double next_value = 0;

    for (int i = 0; i < 4; i++) { // Check up and down
        current = 0;
        next = current + 1;

        while (next < 4) {
            while ((next < 4) && !check_occupied(board, i, next)) {
                next++;
            }

            if (next >= 4) { next--; }

            current_value = 0;
            next_value = 0;

            if (check_occupied(board, i, current)) {
                current_value = get_node_value(board, i, current);
            }

            if (check_occupied(board, i, next)) {
                next_value = get_node_value(board, i, next);
            }

            if (current_value > next_value) {
                totals[0] += next_value - current_value;
            } else if (next_value > current_value) {
                totals[1] += current_value - next_value;
            }

            current = next;
            next++;
        }
    }

    for (int j = 0; j < 4; j++) { // Check left and right
        current = 0;
        next = current + 1;

        while (next < 4) {
            while ((next < 4) && !check_occupied(board, j, next)) {
                next++;
            }

            if (next >= 4) { next--; }

            current_value = 0;
            next_value = 0;

            if (check_occupied(board, current, j)) {
                current_value = get_node_value(board, current, j);
            }

            if (check_occupied(board, next, j)) {
                next_value = get_node_value(board, next, j);
            }

            if (current_value > next_value) {
                totals[2] += next_value - current_value;
            } else if (next_value > current_value) {
                totals[3] += current_value - next_value;
            }

            current = next;
            next++;
        }
    }

    double total_up_down = (totals[0] > totals[1]) ? totals[0] : totals[1];
    double total_left_right = (totals[2] > totals[3]) ? totals[2] : totals[3];

    return total_up_down + total_left_right;
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

int get_node_value(int* board, int pos_x, int pos_y) {
    int within_x = is_in_range(pos_x, 0, 3);
    int within_y = is_in_range(pos_y, 0, 3);

    return (within_x && within_y) ? board[4 * pos_y + pos_x] : 0;
}

int check_occupied(int* board, int pos_x, int pos_y) {
    return get_node_value(board, pos_x, pos_y) != TILE_0_VALUE;
}
