from src.puzzles.play_2048.play_2048_state import Play2048State


class Play2048Manual(object):
    def __init__(self, gui):
        self.gui = gui
        self.game = Play2048State(None)

    def do_move(self, move):
        if not self.gui.started:
            return

        if self.game.move(move):
            self.game.next_state()

        if self.gui.take_screenshots:
            self.gui.screenshot.emit()

        self.gui.score_message.emit('Score: {}'.format(self.game.score))

        if not self.game.is_possible():
            self.gui.status_message.emit('Finished')
        self.gui.update()

    def board(self):
        return self.game.board
