from src.puzzles.play_2048.play_2048_state import Play2048State
from src.puzzles.play_2048.play_2048_player import Play2048Player


class Play2048Manual(object):
    def __init__(self, gui):
        self.gui = gui
        self.game = Play2048State()

        self.states = []

    def do_move(self, move):
        if not self.gui.started:
            return

        state = (Play2048Player.move_id(move), list(self.game.board))

        if self.gui.pickle_states:
            self.states.append(state)

        if self.game.move(move):
            self.game.next_state()

        if self.gui.take_screenshots:
            self.gui.screenshot.emit()

        self.gui.score_message.emit('Score: {}'.format(self.game.score))

        if not self.game.is_possible():
            self.gui.game_ended()

        self.gui.update()

    def board(self):
        return self.game.board
