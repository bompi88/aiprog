from PyQt4.QtCore import QThread
from time import sleep

from src.puzzles.play_2048.play_2048_minimax import Play2048Minimax
from src.puzzles.play_2048.play_2048_minimax_state import Play2048MinimaxState


class Play2048Player(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.gui, self.game = gui, None

        self.minimax = Play2048Minimax()

    def play(self, game):
        self.game = game

        self.start()

    def run(self):
        ended = False

        while not ended:
            move = self.minimax.minimax_decision(Play2048MinimaxState(self.game))
            did_move = self.game.move(move)
            if did_move:
                self.game.next_state()

            print self

            if self.gui:
                sleep(self.gui.delay / 1000.0)

            self.gui.score_message.emit('Score: {}'.format(self.game.score))
            self.gui.update()

            if not self.game.is_possible():
                ended = True

        self.gui.status_message.emit('Finished')

    def end_player(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Search killed')

    def __del__(self):
        self.gui.status_message.emit('Search destroyed')
        self.exiting = True
        self.wait()

    def __str__(self):
        return '\n'.join(
            [' - '.join(str(el) for el in row) for row in self.game.board]
        )
