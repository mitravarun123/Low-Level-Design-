import random
from collections import deque
from enum import Enum


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, Cell) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Snake:
    def __init__(self, start):
        self.body = deque([start])
        self.body_set = {start}
        self.direction = Direction.RIGHT

    def get_head(self):
        return self.body[0]

    def move(self, next_cell, grow):
        tail = self.body[-1]

        # Allow moving into tail only if not growing
        if next_cell in self.body_set and not (next_cell == tail and not grow):
            return False

        self.body.appendleft(next_cell)
        self.body_set.add(next_cell)

        if not grow:
            removed = self.body.pop()
            self.body_set.remove(removed)

        return True


class Food:
    def __init__(self, rows, cols, occupied):
        while True:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            cell = Cell(r, c)
            if cell not in occupied:
                self.position = cell
                break


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def is_inside(self, cell):
        return 0 <= cell.row < self.rows and 0 <= cell.col < self.cols

    def display(self, snake, food, score):
        grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]

        for c in snake.body:
            grid[c.row][c.col] = 'S'

        head = snake.get_head()
        grid[head.row][head.col] = 'H'
        grid[food.position.row][food.position.col] = 'F'

        print(f"\nScore: {score}")
        for row in grid:
            print(" ".join(row))


class SnakeGame:
    ROWS = 10
    COLS = 10
    SCORE_PER_FOOD = 10

    @staticmethod
    def update_direction(snake, ch):
        if ch == 'w' and snake.direction != Direction.DOWN:
            snake.direction = Direction.UP
        elif ch == 's' and snake.direction != Direction.UP:
            snake.direction = Direction.DOWN
        elif ch == 'a' and snake.direction != Direction.RIGHT:
            snake.direction = Direction.LEFT
        elif ch == 'd' and snake.direction != Direction.LEFT:
            snake.direction = Direction.RIGHT

    @staticmethod
    def get_next_cell(head, direction):
        if direction == Direction.UP:
            return Cell(head.row - 1, head.col)
        if direction == Direction.DOWN:
            return Cell(head.row + 1, head.col)
        if direction == Direction.LEFT:
            return Cell(head.row, head.col - 1)
        if direction == Direction.RIGHT:
            return Cell(head.row, head.col + 1)

    @staticmethod
    def run():
        board = Board(SnakeGame.ROWS, SnakeGame.COLS)
        snake = Snake(Cell(5, 5))
        food = Food(SnakeGame.ROWS, SnakeGame.COLS, snake.body_set)

        score = 0
        print("Controls: W A S D (press Enter)")

        while True:
            board.display(snake, food, score)
            move = input("Move: ").strip().lower()

            if not move:
                continue

            SnakeGame.update_direction(snake, move[0])

            head = snake.get_head()
            next_cell = SnakeGame.get_next_cell(head, snake.direction)

            if not board.is_inside(next_cell):
                print("Hit the wall 💥 Game Over")
                break

            grow = next_cell == food.position

            if not snake.move(next_cell, grow):
                print("Self collision 💀 Game Over")
                break

            if grow:
                score += SnakeGame.SCORE_PER_FOOD
                food = Food(SnakeGame.ROWS, SnakeGame.COLS, snake.body_set)


if __name__ == "__main__":
    SnakeGame.run()
