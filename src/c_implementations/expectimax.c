#include <stdio.h>
#include <limits.h>

double max_value(int* board, int depth);
double chance_node(int* board, int depth);
int slides(int action, int* board, int perform);
int collides(int action, int* board, int perform);
int is_impossible(int* board);
double evaluation_function(int* board);
int amount_of_successors(int* board);
int** generate_successors(int* board);
int* perform_action(int action, int* board);
int expectimax_decision(int* board, int depth);

typedef struct {
    char *strVal; // or char strVal[20];
    int intVal;
} vector;

double max_value(int* board, int depth) {
  if (depth == 0 || is_impossible(board)) {
    return evaluation_function(board);
  }

  double v = -INT_MAX;

  int successor_amount = amount_of_successors(board);
  int** successors = generate_successors(board);

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
  int** successors = generate_successors(board);

  double vs = 0;
  double count = 0;

  for (int i=0; i < successor_amount; i++) {
    // TODO: fix this successor_tiles
    double probability = state.successor_tiles[i]
    double value = probability *  max_value(successors[i], depth - 1);

    vs = vs + value;
    count++;
  }

  return vs / count;
}

int slides(int action, int* board, int perform) {

}

int collides(int action, int* board, int perform) {

}

int is_impossible(int* board) {
  int possible = 0;

  for (int m=0; m<4; m++) {
    if slides(m, board, 0) {
      possible = 1;
      break;
    }
    if collides(m, board, 0) {
      possible = 1;
      break;
    }
  }

  return possible;
}

double evaluation_function(int* board) {
    if (is_impossible(board)) {
        return 0
    }

    return 1
    // return self.heuristic.evaluation_function(self)
}

int amount_of_successors(int* board) {

}

int** generate_successors_max(int* board) {
  for (int m=0; m<4; m++) {
    int *copy = malloc(sizeof(board));
    memcpy(copy, board, sizeof(board));

    // TODO: check if move is possible and append successor
  }
//    for move in self.possible_moves:
//            successor = self.copy_with_board(deepcopy(self.board))
//
//            if successor.move(move):
//                self.successors.append(successor)
}

int** generate_successors_chance(int* board) {
    struct vector zero_tiles[16];
    int count = 0;

    for (int x=0; x<4; x++) {
        for (int y=0; y<4; y++) {
            if (board[x*y]==0) {
                struct vector xy;
                xy.x = x
                xy.y = y
                zero_tiles[count] = xy
                count++;
            }
        }
    }
    int num_possibilities = 2
    int possibilities[num_possibilities] = {2, 4}

    for (int i=0; i < count; i++) {
        for (int p=0; p < num_possibilities; p++) {
            int *copy = malloc(sizeof(board));
            memcpy(copy, board, sizeof(board));
            copy[zero_tiles[i].x * zero_tiles[i].x] = possibilities[p]

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
  printf("%d\n", INT_MIN);
  printf("%d\n", expectimax_decision(arr, 9));

  return 0;
}
