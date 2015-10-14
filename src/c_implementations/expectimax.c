#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

double max_value(int* board, int depth);
double chance_node(int* board, int depth);
int slides(int action, int* board, int perform);
int collides(int action, int* board, int perform);
int is_impossible(int* board);
double evaluation_function(int* board);
int amount_of_successors(int* board);
int** generate_successors_max(int* board);
int** generate_successors_change(int* board);
int* perform_action(int action, int* board);
int decision(int* board, int* actions, int depth);

typedef struct {
    int x;
    int y;
} Vector;

int LEFT = 0;
int UP = 1;
int RIGHT = 2;
int DOWN = 3;
int* LEFT_VECTOR[2] = { -1, 0 };
int* UP_VECTOR[2] = { 0, -1 };
int* RIGHT_VECTOR[2] = { 1, 0 };
int* DOWN_VECTOR[2] = { 0, 1 };

long random_num(long max) {
  unsigned long
  num_bins = (unsigned long) max + 1,
  num_rand = (unsigned long) RAND_MAX + 1,
  bin_size = num_rand / num_bins,
  defect   = num_rand % num_bins;

  long x;
  do {
   x = random();
  }

  while (num_rand - defect <= (unsigned long)x);

  return x/bin_size;
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
    // TODO: fix this successor_tiles
    // double probability = state.successor_tiles[i]
    double probability = 1; // TODO: remove this
    double value = probability *  max_value(successors[i], depth - 1);

    vs = vs + value;
    count++;
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

    int did_slide = slides(move, board);
    int did_collide = collides(move, board);

    int did_slides_after_collision = 0;

    if (did_collide==1):
        did_slides_after_collision = slides(move, board);

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

            if (board[x * y]==0) {
                continue;
            }

            move_to.x = x + move_modifier[0];
            move_to.y = y + move_modifier[1];

            if (action==LEFT) {
                for (int x_new=0; x_new < move_to.x + 1; x_new++) {
                    if (is_in_range(x_new, 0, 3) && is_in_range(move_to.y, 0, 3)) {
                        if (board[move_to.y*x_new]==0) {
                            if (perform) {
                                board[move_to.y*x_new] = board[x*y];
                                board[x*y] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            } else if (action==UP) {
                for (int y_new=0; y_new < move_to.y + 1; y_new++) {
                    if (is_in_range(y_new, 0, 3) && is_in_range(move_to.x, 0, 3)) {
                        if (board[move_to.x*y_new]==0) {
                            if (perform) {
                                board[move_to.x*y_new] = board[x*y];
                                board[x*y] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            } else if (action==RIGHT) {
                for (int x_new=3; x_new > move_to.x - 1; x_new--) {
                    if (is_in_range(x_new, 0, 3) && is_in_range(move_to.y, 0, 3)) {
                        if (board[move_to.y*x_new]==0) {
                            if (perform) {
                                board[move_to.y*x_new] = board[x*y];
                                board[x*y] = 0;
                            }

                            did_move = 1;
                            break;
                        }
                    }
                }
            } else if (action==DOWN) {
                for (int y_new=3; y_new > move_to.y - 1; y_new--) {
                    if (is_in_range(y_new, 0, 3) && is_in_range(move_to.x, 0, 3)) {
                        if (board[move_to.x*y_new]==0) {
                            if (perform) {
                                board[move_to.x*y_new] = board[x*y];
                                board[x*y] = 0;
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
                if (board[x*y]==0) {
                    continue;
                }
                if (board[neighbour.x*neighbour.y]==board[x*y]) {
                    if (perform) {
                        board[x*y] *= 2;
                        board[neighbour.x*neighbour.y] = 0;
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
    if (is_impossible(board)) {
        return 0;
    }

    // TODO: Write heuristics

    return 1;
}

int amount_of_successors(int* board) {
    int count = 0;

    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            if (board[x*y]==0) {
                count++;
            }
        }
    }

    return count;
}

int** generate_successors_max(int* board) {
  for (int m=0; m<4; m++) {
    int *copy = malloc(sizeof(board));
    memcpy(copy, board, sizeof(board));

    if (move(m)):


    // TODO: check if move is possible and append successor
  }
//    for move in self.possible_moves:
//            successor = self.copy_with_board(deepcopy(self.board))
//
//            if successor.move(move):
//                self.successors.append(successor)
}

int** generate_successors_chance(int* board) {
    Vector zero_tiles[16];
    int count = 0;

    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            if (board[x*y]==0) {
                Vector xy;
                xy.x = x;
                xy.y = y;
                zero_tiles[count] = xy;
                count++;
            }
        }
    }
    int num_possibilities = 2;
    int* possibilities[2] = { 2, 4 };

    for (int i=0; i < count; i++) {
        for (int p=0; p < num_possibilities; p++) {
            int *copy = malloc(sizeof(board));
            memcpy(copy, board, sizeof(board));
            copy[zero_tiles[i].x * zero_tiles[i].x] = possibilities[p];

            // TODO: fix this
        }
    }
//    zero_tiles = []
//        for x in range(4):
//            for y in range(4):
//                if self.board[y][x] is 0:
//                    zero_tiles.append((x, y))
//
//        possibilities = [2, 4]
//
//        for tile in zero_tiles:
//            for possibility in possibilities:
//                new_board = deepcopy(self.board)
//                new_board[tile[1]][tile[0]] = possibility
//
//                successor = self.copy_with_board(new_board)
//                self.successors.append(successor)
//                self.successor_tiles.append(possibility)
}

int* perform_action(int action, int* board) {
    int *new_game = malloc(sizeof(board));
    memcpy(new_game, board, sizeof(board));

    int did_move = move(action, board);

    if (did_move) {
        return new_game;
    } else {
        // TODO: What to do here?
        board[16] = -1;
        return board;
    }
}

int decision(int* board, int* actions, int depth) {
  double max_val = -INT_MAX;
  int max_action = -1;

  for (int a=0; a < 4; a++) {
    int* board = perform_action(actions[a], board);

    if (board[16] == -1) {
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

int main() {
  int arr[16] = {3, 4, 0, 1, 2, 4, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0};
  int actions[4] = { 0, 1, 2, 3 };
  printf("%d\n", INT_MIN);
  printf("%d\n", decision(arr, actions, 4));

  return 0;
}
