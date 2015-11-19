from src.algorithms.ann.sum_of_squared_errors import SumOfSquaredErrors
from src.algorithms.ann.ann import Ann
from src.utils.ann2048_basics import load_2048_example
from src.utils.ann2048_basics import process_states
from src.puzzles.play_2048.play_2048_player import Play2048Player
from src.puzzles.play_2048.play_2048_state import Play2048State
from theano import tensor as T
from copy import deepcopy
from random import randint

class Ann2048Trainer(object):
    def __init__(self, gui_worker=None):

        self.game = Play2048State()
        self.mapping = ['left', 'up', 'right', 'down']
        self.trained = False

        print('----> Loading cases...')

        training_set = load_2048_example()
        testing_set = load_2048_example()

        provided_datasets = [
            training_set,
            testing_set
        ]

        self.net = Ann(
            structure=[16, 200, 4],
            datasets=provided_datasets,
            activation_function=[T.nnet.sigmoid, T.nnet.sigmoid],
            learning_rate=0.1,
            regression_layer=SumOfSquaredErrors
        )

        self.gui_worker = gui_worker

    def train(self, epochs=60):
        if not self.trained:
            self.net.train(epochs)
        self.trained = True

    def blind_test(self, state):
        return self.net.blind_test(state)

    # def test(self):
    #    minor_demo(self.net)

    def play(self):
        ended = False

        while not ended:
            new_game = self.game.copy_with_board(self.game.board)

            move = new_game.possible_moves[self.mapping[self.net.blind_test([deepcopy(new_game.board)], normalize=process_states)[0]]]

            state = (Play2048Player.move_id(move), list(self.game.board))

            if self.game.move(move):
                self.game.next_state()

                if self.gui_worker:
                    self.gui_worker.move_completed(state)
            else:
                # TODO: This must be removed, but how?
                if self.game.move(new_game.possible_moves[self.mapping[randint(0, 3)]]):
                    self.game.next_state()
            if not self.game.is_possible():
                ended = True

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])

if __name__ == '__main__':

    trainer = Ann2048Trainer()

    trainer.train(100)
    # trainer.test()
