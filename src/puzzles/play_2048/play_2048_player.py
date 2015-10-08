from time import sleep
from PyQt4.QtCore import QThread
from src.algorithms.minimax.minimax import Minimax

from src.puzzles.play_2048.play_2048_state import Play2048State


class Play2048Player(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, heuristic, depth):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.game = Play2048State(heuristic)

        self.minimax = Minimax(self.actions(), depth)

    @classmethod
    def actions(cls):
        return {'left': [-1, 0], 'up': [0, -1], 'right': [1, 0], 'down': [0, 1]}

    def run(self):
        ended = False

        while not ended:
            new_game = self.game.copy_with_board(self.game.board)
            move = self.minimax.alpha_beta_decision(new_game)

            if self.game.move(move):
                self.game.next_state()
                self.move_completed()

            if self.gui.take_screenshots:
                self.gui.screenshot.emit()

            if not self.game.is_possible():
                ended = True

        self.gui.status_message.emit('Game ended')

    def move_completed(self):
        sleep(self.gui.delay / 1000.0)
        self.gui.score_message.emit('Score: {}'.format(self.game.score))
        self.gui.update()

    def end_player(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Search killed')

    def __del__(self):
        self.exiting = True
        self.wait()

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])
