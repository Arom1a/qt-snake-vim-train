import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
import random


class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake with Vim Motion")

        # grid and window
        self.grid_size = 20
        self.cell_size = 20
        self.width = self.grid_size * self.cell_size
        self.height = self.grid_size * self.cell_size

        self.setFixedSize(self.width, self.height)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # game state
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = (0, -1)
        self.new_direction = self.direction
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.speed = 300

        # timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(self.speed)

    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_H:  # h -> left
            if self.direction[0] != 1:  # prevent reversing
                self.new_direction = (-1, 0)
        elif key == Qt.Key.Key_L:  # l -> right
            if self.direction[0] != -1:
                self.new_direction = (1, 0)
        elif key == Qt.Key.Key_K:  # k -> up
            if self.direction[1] != 1:
                self.new_direction = (0, -1)
        elif key == Qt.Key.Key_J:  # j -> down
            if self.direction[1] != -1:
                self.new_direction = (0, 1)
        elif key == Qt.Key.Key_R:  # restart
            self.reset_game()
        elif key == Qt.Key.Key_Space:  # speed up
            self.speed = 100 if self.speed == 300 else 300
            self.timer.setInterval(self.speed)
        elif key == Qt.Key.Key_Q:  # quit
            quit(0)

    def update_game(self):
        if self.game_over:
            return

        head = self.snake[0]
        self.direction = self.new_direction
        new_head = (
            (head[0] + self.direction[0]) % self.grid_size,
            (head[1] + self.direction[1]) % self.grid_size
        )

        if new_head in self.snake:
            self.game_over = True
            self.timer.stop()
            self.update()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.update()

    def reset_game(self):
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = (0, -1)
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.timer.setInterval(300)
        self.timer.start()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(0, 0, self.width, self.height, QColor(0, 0, 0))

        painter.fillRect(self.snake[0][0] * self.cell_size,
                         self.snake[0][1] * self.cell_size,
                         self.cell_size,
                         self.cell_size, QColor(200, 200, 255))

        for segment in self.snake[1:]:
            x = segment[0] * self.cell_size
            y = segment[1] * self.cell_size
            painter.fillRect(x, y, self.cell_size,
                             self.cell_size, QColor(230, 230, 250))

        x = self.food[0] * self.cell_size
        y = self.food[1] * self.cell_size
        painter.fillRect(x, y, self.cell_size, self.cell_size,
                         QColor(181, 126, 220))

        if self.game_over:
            painter.setPen(QColor(221, 160, 221))
            painter.drawText(
                0, 0, self.width, self.height,
                Qt.AlignmentFlag.AlignCenter,
                f"Game Over! Score: {self.score}\n" +
                "Press `r` to restart\n" +
                "Press `q` to quit"
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())
