#ifndef AIPROG_EXPECTIMAX_H
#define AIPROG_EXPECTIMAX_H

double max_value(int* board, int depth);
double chance_node(int* board, int depth);
int move(int move, int* board);
int slides(int action, int* board, int perform);
int collides(int action, int* board, int perform);
int is_impossible(int* board);
double evaluation_function(int* board);
double max_placement(int* board);
double order(int* board);
double max_tile(int* board);
int get_node_value(int* board, int pos_x, int pos_y);
int check_occupied(int* board, int pos_x, int pos_y);
int free_tiles(int* board);
double smoothness(int *board);
int get_neighbour_value(int* board, int x, int y, int direction);
int amount_of_successors(int* board);
int** generate_successors_max(int* board);
int** generate_successors_chance(int* board);
int* perform_action(int action, int* board);
int decision_map(int depth, int* board);
int decision(int depth, int b0, int b1, int b2, int b3, int b4, int b5, int b6,
                        int b7, int b8, int b9, int b10, int b11, int b12,
                        int b13, int b14, int b15);
void print_board(int* board);

#endif //AIPROG_EXPECTIMAX_H
