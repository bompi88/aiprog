from time import sleep
from PyQt4.QtCore import QThread

from src.puzzles.play_2048.play_2048_player import Play2048Player


class Play2048Worker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.player = Play2048Player(gui.search, gui.depth, self)

    def run(self):
        self.player.play()

        self.gui.game_ended()

    def move_completed(self):
        if self.gui.take_screenshots:
            self.gui.screenshot.emit()

        sleep(self.gui.delay / 1000.0)
        self.gui.score_message.emit('Score: {}'.format(self.player.game.score))
        self.gui.update()

    def end_worker(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Search killed')

    def board(self):
        return self.player.game.board

    def __del__(self):
        self.exiting = True
        self.wait()

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])
