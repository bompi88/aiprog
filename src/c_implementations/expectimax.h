#ifndef AIPROG_EXPECTIMAX_H
#define AIPROG_EXPECTIMAX_H

double max_value(int* board, int depth);
double chance_node(int* board, int depth);
int slides(int action, int* board, int perform);
int collides(int action, int* board, int perform);
int is_impossible(int* board);
double evaluation_function(int* board);
int amount_of_successors(int* board);
int** generate_successors_max(int* board);
int** generate_successors_chance(int* board);
int* perform_action(int action, int* board);
int decision(int* board, int depth);
void print_board(int* board);

#endif //AIPROG_EXPECTIMAX_H
