from PyQt4.QtCore import QThread

from src.puzzles.play_2048.play_2048_player import Play2048Player


class Play2048SaveWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, num_plays=100, min_tile=10):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.player = None
        self.num_plays = num_plays
        self.min_tile = min_tile
        self.played = 0
        self.depth = self.gui.depth
        self.search = self.gui.search
        self.states = {}

    def run(self):
        while self.played < self.num_plays:
            self.states = {}
            self.player = Play2048Player(self.search, self.depth, self)
            self.player.play()
            if self.player.game.max_tile() >= self.min_tile:
                self.played += 1
            self.gui.single_save_ended(self.player.game.max_tile())
            self.gui.status_message.emit(
                'Number of plays with a tile equal or greater than ' +
                str(2 ** self.min_tile) + ' saved: {}, Remaining: {}'.format(
                    self.played,
                    self.num_plays - self.played
                )
            )
        self.gui.save_ended()

    def move_completed(self, state):
        self.states[','.join(str(x) for x in state[1])] = state
        self.gui.score_message.emit('Score: {}'.format(self.player.game.score))
        self.gui.update()

    def end_worker(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Saving terminated')

    def board(self):
        return self.player.game.board

    def __del__(self):
        self.exiting = True
        self.wait()

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.board()])
