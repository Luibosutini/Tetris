import tkinter as tk
import random
import tkinter.messagebox as messagebox
import sys

# ミノを構成するブロックのクラス
class MinosBlock:
    COLORS = {
        'I': 'cyan',
        'O': 'yellow',
        'S': 'green',
        'Z': 'red',
        'J': 'blue',
        'L': 'orange',
        'T': 'purple',
        
        'I1': 'cyan',
        'I2': 'cyan',
        'O1': 'yellow',
        'S1': 'green',
        'S2': 'green',
        'Z1': 'red',
        'Z2': 'red',
        'J1': 'blue',
        'J2': 'blue',
        'J3': 'blue',
        'J4': 'blue',
        'L1': 'orange',
        'L2': 'orange',
        'L3': 'orange',
        'L4': 'orange',
        'T1': 'purple',
        'T2': 'purple',
        'T3': 'purple',
        'T4': 'purple',
        
        None: 'gray'
    }
    
    SHAPES = {
        'I': [(1, 1, 1, 1)],
        'O': [(1, 1), (1, 1)],
        'S': [(0, 1, 1), (1, 1, 0)],
        'Z': [(1, 1, 0), (0, 1, 1)],
        'J': [(1, 1, 1), (0, 0, 1)],
        'L': [(1, 1, 1), (1, 0, 0)],
        'T': [(1, 1, 1), (0, 1, 0)]
    }
    ALL_SHAPES = {
        'I1': [(1, 1, 1, 1)],
        'I2': [(1),(1),(1),(1)],
        'O1': [(1, 1), (1, 1)],
        'S1': [(0, 1, 1), (1, 1, 0)],
        'S2': [(1, 0), (1, 1),(0, 1)],
        'Z1': [(1, 1, 0), (0, 1, 1)],
        'Z2': [(0, 1), (1, 1), (1, 0)],
        'J1': [(1, 1, 1), (0, 0, 1)],
        'J2': [(1, 1), (1, 0), (1, 0)],
        'J3': [(1, 0, 0), (1, 1, 1)],
        'J4': [(0, 1), (0, 1), (1, 1)],
        'L1': [(1, 1, 1), (1, 0, 0)],
        'L2': [(1, 1), (0, 1), (0, 1)],
        'L3': [(0, 0, 1), (1, 1, 1)],
        'L4': [(1, 0), (1, 0), (1, 1)],
        'T1': [(1, 1, 1), (0, 1, 0)],
        'T2': [(0, 1), (1, 1), (0, 1)],
        'T3': [(0, 1, 0), (1, 1, 1)],
        'T4': [(1, 0), (1, 1), (1, 0)]
    }
    
    def __init__(self, shape):
        self.shape = shape
        #print(self.get_shape_name())
        self.color = self.COLORS[self.get_shape_name()]

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))

    def move_left(self):
        self.shape = [[row[i] for i in range(len(row) - 1, -1, -1)] for row in self.shape]

    def move_right(self):
        self.shape = [[row[i] for i in range(len(row))] for row in self.shape]

    def get_shape_name(self):
        ans = None
        i = 0
        for name, shape in self.ALL_SHAPES.items():
            i += 1
            if self.shape == shape:
                ans = name
        print(i)
        return ans

# ミノの生成を行うクラス
class GenerationMinos:
    def __init__(self):
        self.mino_queue = []

    def generate(self):
        if len(self.mino_queue) < 7:
            minos = [MinosBlock(shape) for shape in random.sample(list(MinosBlock.SHAPES.values()), 7)]
            self.mino_queue.extend(minos)

        return self.mino_queue.pop(0)

# ミノの描画を行うクラス
class MinosCanvas:
    BLOCK_SIZE = 30

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_mino(self, mino, x, y):
        for i, row in enumerate(mino.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    self.draw_block(x + j, y + i, mino.color)

    def draw_block(self, x, y, color):
        x1 = x * self.BLOCK_SIZE
        y1 = y * self.BLOCK_SIZE
        x2 = x1 + self.BLOCK_SIZE
        y2 = y1 + self.BLOCK_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')


# 積まれたミノを管理するクラス
class TetrisField:
    WIDTH = 10
    HEIGHT = 20
    EMPTY_CELL = 0

    def __init__(self):
        self.field = [[self.EMPTY_CELL] * self.WIDTH for _ in range(self.HEIGHT)]

    def is_collision(self, mino, x, y):
        for i, row in enumerate(mino.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    if (
                        x + j < 0
                        or x + j >= self.WIDTH
                        or y + i < 0
                        or y + i >= self.HEIGHT
                        or self.field[y + i][x + j] != self.EMPTY_CELL
                    ):
                        return True
        return False

    def place_mino(self, mino, x, y):
        for i, row in enumerate(mino.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    self.field[y + i][x + j] = mino

    def check_lines(self):
        full_lines = []
        for i in range(self.HEIGHT):
            if all(cell != self.EMPTY_CELL for cell in self.field[i]):
                full_lines.append(i)
        return full_lines

    def clear_lines(self, lines):
        for line in lines:
            self.field.pop(line)
        self.field = [[self.EMPTY_CELL] * self.WIDTH for _ in range(len(lines))] + self.field


# プレイ画面を作成するクラス
class CanvasField:
    BLOCK_SIZE = 30

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_field(self, field):
        self.canvas.delete('all')
        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                if cell != 0:
                    self.draw_block(j, i, cell.color)

    def draw_block(self, x, y, color):
        x1 = x * self.BLOCK_SIZE
        y1 = y * self.BLOCK_SIZE
        x2 = x1 + self.BLOCK_SIZE
        y2 = y1 + self.BLOCK_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')


# テトリスのイベントを受け付けてそのイベントに応じてテトリスを制御するクラス
class GameGeneral:
    def __init__(self, field, generation_minos, minos_canvas, canvas_field, game_over_callback):
        self.field = field
        self.generation_minos = generation_minos
        self.minos_canvas = minos_canvas
        self.canvas_field = canvas_field
        self.game_over_callback = game_over_callback
        self.current_mino = self.generation_minos.generate()
        self.x = field.WIDTH // 2 - len(self.current_mino.shape[0]) // 2
        self.y = 0
        self.canvas_field.draw_field(self.field.field)
        self.minos_canvas.draw_mino(self.current_mino, self.x, self.y)

    def move_left(self):
        if not self.field.is_collision(self.current_mino, self.x - 1, self.y):
            self.x -= 1
            self.minos_canvas.draw_mino(self.current_mino, self.x, self.y)

    def move_right(self):
        if not self.field.is_collision(self.current_mino, self.x + 1, self.y):
            self.x += 1
            self.minos_canvas.draw_mino(self.current_mino, self.x, self.y)

    def rotate(self):
        rotated_mino = MinosBlock(self.current_mino.shape)
        rotated_mino.rotate()
        if not self.field.is_collision(rotated_mino, self.x, self.y):
            self.current_mino = rotated_mino
            self.minos_canvas.draw_mino(self.current_mino, self.x, self.y)

    def hard_drop(self):
        while not self.field.is_collision(self.current_mino, self.x, self.y + 1):
            self.y += 1
        self.place_mino()

    def place_mino(self):
        self.field.place_mino(self.current_mino, self.x, self.y)
        full_lines = self.field.check_lines()
        if full_lines:
            self.field.clear_lines(full_lines)
        self.current_mino = self.generation_minos.generate()
        self.x = self.field.WIDTH // 2 - len(self.current_mino.shape[0]) // 2
        self.y = 0
        if self.field.is_collision(self.current_mino, self.x, self.y):
            self.game_over_callback()
            # Game over
        else:
            self.canvas_field.draw_field(self.field.field)
            self.minos_canvas.draw_mino(self.current_mino, self.x, self.y)

# ゲームオーバー
class GameOver:
    def __init__(self, game_general):
        self.game_general = game_general

    def show(self):
        messagebox.showinfo("Game Over", "Game Over")
        self.game_general.stop_game()  # ゲームの停止
        sys.exit()
        


# ゲーム、テトリス、generalを動かすクラス
class Application:
    WIDTH = 10
    HEIGHT = 20
    BLOCK_SIZE = 30

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(
            self.master,
            width=self.WIDTH * self.BLOCK_SIZE,
            height=self.HEIGHT * self.BLOCK_SIZE,
            bg='black'
        )
        self.canvas.pack()
        self.field = TetrisField()
        self.generation_minos = GenerationMinos()
        self.minos_canvas = MinosCanvas(self.canvas)
        self.canvas_field = CanvasField(self.canvas)
        self.game_over =GameOver(self)        
        self.game = GameGeneral(
                                self.field,
                                self.generation_minos,
                                self.minos_canvas,
                                self.canvas_field,
                                self.game_over.show
                                )


        self.master.bind('<Left>', self.move_left)
        self.master.bind('<Right>', self.move_right)
        self.master.bind('<Up>', self.rotate)
        self.master.bind('<space>', self.hard_drop)
        self.master.after(1000, self.game_loop)
        self.running = True

    def move_left(self, event):
        self.game.move_left()

    def move_right(self, event):
        self.game.move_right()

    def rotate(self, event):
        self.game.rotate()

    def hard_drop(self, event):
        self.game.hard_drop()

    def game_loop(self):
        if self.running and not self.field.is_collision(self.game.current_mino, self.game.x, self.game.y + 1):
            self.game.y += 1
        else:
            self.game.place_mino()
            self

        self.canvas_field.draw_field(self.field.field)
        self.minos_canvas.draw_mino(self.game.current_mino, self.game.x, self.game.y)
        self.master.after(1000, self.game_loop)

    def stop_game(self):
        self.running = False

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
