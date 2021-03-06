from src.puzzles.play_2048.play_2048_state import Play2048State


class Play2048Player(object):
    def __init__(self, search, depth, heuristic=0, gui_worker=None):
        self.game = Play2048State()

        self.search = search(depth, heuristic)

        self.gui_worker = gui_worker

    @classmethod
    def actions(cls):
        return {'left': [-1, 0], 'up': [0, -1], 'right': [1, 0], 'down': [0, 1]}

    @classmethod
    def move_id(cls, move):
        for i, action in enumerate(cls.actions().values()):
            if move == action:
                return i

    def play(self):
        ended = False

        while not ended:
            new_game = self.game.copy_with_board(self.game.board)
            move = self.search.decision(new_game)

            state = (self.move_id(move), list(self.game.board))

            if self.game.move(move):
                self.game.next_state()

                if self.gui_worker:
                    self.gui_worker.move_completed(state)

            if not self.game.is_possible():
                ended = True

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])
