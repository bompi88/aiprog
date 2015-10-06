from PyQt4.QtCore import QThread
from time import sleep
from random import randint


class Play2048Player(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.gui, self.game = gui, None

    def play(self, game):
        self.game = game

        self.start()

    def run(self):
        ended = False

        while not ended:
            did_move = self.move()
            if did_move:
                self.game.next_state()
            self.gui.update()

        self.gui.status_message.emit('Finished')

    def end_player(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Search killed')

    def __del__(self):
        self.exiting = True
        self.wait()

    def move(self, move=None):
        if not move:
            moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]

            move = moves[randint(0, 3)]

        did_move = False
        board = self.game.board
        for i in range(4):
            for j in range(4):
                if move[0] == 1:
                    x = 3 - j
                else:
                    x = j

                if move[1] == 1:
                    y = 3 - i
                else:
                    y = i

                move_to = (x + move[0], y + move[1])

                should_move = board[y][x] != 0

                if should_move and move[0] == 1:
                    for x_new in range(3, move_to[0] - 1, -1):
                        if x_new in range(4) and move_to[1] in range(4):
                            if board[move_to[1]][x_new] == 0:
                                board[move_to[1]][x_new] = board[y][x]
                                board[y][x] = 0
                                did_move = True
                                break
                elif should_move and move[0] == -1:
                    for x_new in range(4):
                        if x_new in range(4) and move_to[1] in range(4):
                            if board[move_to[1]][x_new] == 0:
                                board[move_to[1]][x_new] = board[y][x]
                                board[y][x] = 0
                                did_move = True
                                break
                elif should_move and move[1] == 1:
                    for y_new in range(3, move_to[1] - 1, -1):
                        if move_to[0] in range(4) and y_new in range(4):
                            if board[y_new][move_to[0]] == 0:
                                board[y_new][move_to[0]] = board[y][x]
                                board[y][x] = 0
                                did_move = True
                                break
                elif should_move and move[1] == -1:
                    for y_new in range(4):
                        if move_to[0] in range(4) and y_new in range(4):
                            if board[y_new][move_to[0]] == 0:
                                board[y_new][move_to[0]] = board[y][x]
                                board[y][x] = 0
                                did_move = True
                                break

        for i in range(4):
            for j in range(4):
                if move[0] == 1:
                    x = 3 - j
                else:
                    x = j

                if move[1] == 1:
                    y = 3 - i
                else:
                    y = i

                neighbour = (x - move[0], y - move[1])
                if neighbour[0] in range(4) and neighbour[1] in range(4):
                    if board[y][x] is 0:
                        continue
                    if board[neighbour[1]][neighbour[0]] == board[y][x]:
                        board[y][x] *= 2
                        board[neighbour[1]][neighbour[0]] = 0
                        did_move = True

        if self.gui:
            sleep(self.gui.delay / 1000.0)
        return did_move

    def __str__(self):
        return '\n'.join(
            [' - '.join(str(el) for el in row) for row in self.game.board]
        )
