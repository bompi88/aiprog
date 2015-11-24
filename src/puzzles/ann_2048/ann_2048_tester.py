from src.utils.ann2048_basics import process_states
from src.puzzles.play_2048.play_2048_player import Play2048Player
from src.puzzles.play_2048.play_2048_state import Play2048State
from copy import deepcopy
from random import randint
import res.play2048s.anns
import pickle
from src.utils.ai2048demo import welch


class Ann2048Tester(object):
    def __init__(self, path=None, ann=None, gui_worker=None):

        self.game = Play2048State()
        self.gui_worker = gui_worker
        self.mapping = ['left', 'up', 'right', 'down']

        if ann:
            self.net = ann
        else:
            print('----> Loading Neural net from file...')
            self.net = self.open(path)

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

    def welch_test(self):
        random_plays = []
        ann_plays = []

        for i in range(50):
            if self.gui_worker:
                self.gui_worker.gui.status_message.emit('Random test, ' + str(i + 1) + '/' + str(50))
            self.game = Play2048State()
            random_plays.append(2 ** self.play_random())

        for i in range(50):
            if self.gui_worker:
                self.gui_worker.gui.status_message.emit('Ann test, ' + str(i + 1) + '/' + str(50))
            self.game = Play2048State()
            ann_plays.append(2 ** self.play())

        text = welch(random_plays, ann_plays)

        print(text)
        if self.gui_worker:
            self.gui_worker.gui.status_message.emit(str(text))

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
            moves = deepcopy(self.net.play2048_test([new_game.board], normalize=process_states)[0])

            self.do_move(new_game, moves)

            if not self.game.is_possible():
                ended = True

        return max(self.game.board)

    def do_move(self, new_game, moves):
        if not moves or len(moves) == 0:
            return

        index_move = moves.index(max(moves))

        moves.pop(index_move)

        move = new_game.possible_moves[
            self.mapping[
                index_move
            ]
        ]

        state = (Play2048Player.move_id(move), list(self.game.board))

        if self.game.move(move):
            self.game.next_state()

            if self.gui_worker:
                self.gui_worker.move_completed(state)
        else:
            self.do_move(new_game, moves)

    def play_random(self):
        ended = False

        while not ended:
            new_game = self.game.copy_with_board(self.game.board)

            move = new_game.possible_moves[
                self.mapping[
                    randint(0, 3)
                ]
            ]

            state = (Play2048Player.move_id(move), list(self.game.board))

            if self.game.move(move):
                self.game.next_state()

                if self.gui_worker:
                    self.gui_worker.move_completed(state)
            if not self.game.is_possible():
                ended = True

        return max(self.game.board)

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])

if __name__ == '__main__':

    trainer = Ann2048Tester()
    trainer.play()
