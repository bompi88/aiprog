#include <stdio.h>
#include <limits.h>

double max_value(int* board, int depth);
double chance_node(int* board, int depth);
int is_impossible(int* board);
double evaluation_function(int* board);
int amount_of_successors(int* board);
int** generate_successors(int* board);
int* perform_action(int action, int* board);

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

  int* values[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

  return -1.0;
  // generate_spawns();
}

//    def min_value(self, state, alpha, beta, depth):
//        if state.cutoff_test(depth):
//            # print(state.evaluation_function())
//            return state.evaluation_function()
//
//        values = []
//
//        for tile, successor in state.generate_successors(False):
//            v = self.max_value(successor, alpha, beta, depth - 1)
//
//            if tile is 2:
//                values.append(v * 0.9)
//            elif tile is 4:
//                values.append(v * 0.1)
//            else:
//                print('what')
//
//        return sum(values) / float(len(values))

int expectimax_decision(int* board, int depth) {
  double max_val = -INT_MAX;
  int max_action = -1;

  for (int a=0; a < 4; a++) {
    int* board = perform_action(a, board);

    if (board[16] == -1) {
      continue;
    }

    double value = max_value(board, depth);

    if (value > max_val) {
      max_val = value;
      max_action = a;
    }
  }

  // return max_action;
  return depth;
}

int main() {
  int arr[16] = {3, 4, 0, 1, 2, 4, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0};
  printf("%d\n", INT_MIN);
  printf("%d\n", expectimax_decision(arr, 9));

  return 0;
}
