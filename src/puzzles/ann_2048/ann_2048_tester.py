from src.utils.ann2048_basics import process_states
from src.puzzles.play_2048.play_2048_player import Play2048Player
from src.puzzles.play_2048.play_2048_state import Play2048State
from copy import deepcopy
from random import randint
import res.play2048s.anns
import pickle
from src.utils.ann2048_basics import process


class Ann2048Tester(object):
    def __init__(self, path=None, ann=None, gui_worker=None):

        self.game = Play2048State()
        self.mapping = ['left', 'up', 'right', 'down']

        print('----> Loading Neural net from file...')
        if ann:
            self.net = ann
        else:
            self.net = self.open(path)
        self.gui_worker = gui_worker

        if self.assert_no_net("No supported ann file found at current path."):
            return

    def assert_no_net(self, error=None):
        if not self.net:
            if error:
                print(error)
            return True
        return False

    def blind_test(self, state):
        if self.assert_no_net():
            return
        return self.net.blind_test(state)

    def set_ann(self, ann):
        self.net = ann

    @staticmethod
    def open(path=None):
        ann = None
        if not path:
            path = res.play2048s.anns.__path__[0] + "/trained-ann-2048"

        try:
            file = open(path, 'rb')
            ann = pickle.load(file)
            file.close()
        except FileNotFoundError:
            return ann
        print("net loaded")
        return ann

    def play(self):
        if self.assert_no_net():
            return
        ended = False

        while not ended:
            new_game = self.game.copy_with_board(self.game.board)
            print(deepcopy(new_game.board))
            int_move = self.net.blind_test([new_game.board], normalize=process_states)[0]

            move = new_game.possible_moves[
                self.mapping[
                    int_move
                ]
            ]

            state = (Play2048Player.move_id(move), list(self.game.board))

            if self.game.move(move):
                self.game.next_state()

                if self.gui_worker:
                    self.gui_worker.move_completed(state)
            else:
                print("Could not move in the specified direction. Used random direction instead.")
                # TODO: This must be removed, but how? Maybe select the next most probabilistic move? and then select a
                # a random move if that also do not work?
                move = new_game.possible_moves[
                    self.mapping[
                        (int_move + 1) % 3
                    ]
                ]
                if self.game.move(move):
                    self.game.next_state()
                else:
                    move = new_game.possible_moves[
                        self.mapping[
                            (int_move + 2) % 3
                        ]
                    ]
                    if self.game.move(move):
                        self.game.next_state()
                    else:
                        move = new_game.possible_moves[
                            self.mapping[
                                (int_move + 3) % 3
                            ]
                        ]
                        if self.game.move(move):
                            self.game.next_state()

            if not self.game.is_possible():
                ended = True

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])

if __name__ == '__main__':

    trainer = Ann2048Tester()
    trainer.play()
