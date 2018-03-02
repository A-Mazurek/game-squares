import Tkinter as tk
from random import randint
import time

matrix = [700, 700]


class MyForm:
    def __init__(self, main_window):
        self.start_time = None
        self.is_running = False
        self.new_game = False
        self.main_window = main_window
        self.canvas = tk.Canvas(
            self.main_window,
            width=matrix[0],
            height=matrix[1],
            bg='#afeeee'
        )

        self.canvas.pack()

        self.main_window = main_window
        main_window.title('Game')

        self.label_value = tk.StringVar()
        label = tk.Label(
            self.main_window,
            textvariable=self.label_value,
            font=("Helvetica", 17)
        )
        label.pack()

        self.game_time_label_value = tk.StringVar()
        time_label = tk.Label(
            self.main_window,
            textvariable=self.game_time_label_value,
            font=("Helvetica", 17)
        )
        time_label.pack()

        self.update_score(0)

        self.close_button = tk.Button(
            main_window, text="close",
            command=self.main_window.destroy,
            font=("Helvetica", 15))
        self.close_button.pack()

        self.start_button = tk.Button(
            main_window,
            text="start",
            command=self.start,
            font=("Helvetica", 15)
        )
        self.start_button.pack()

    def update_score(self, score):
        self.label_value.set('Score: ' + str(score))

    def update_time(self):
        now = time.time()
        game_time = int(now - self.start_time)
        self.game_time_label_value.set('Time: ' + str(game_time) + ' s')

    def start(self):
        self.is_running = True
        self.start_time = time.time()
        self.new_game = True

    def draw_object(self, object_to_draw):
        object_to_draw._print_(self.canvas)


class Square(object):
    def __init__(self, x0=300, y0=650, x1=350, y1=700, color='grey'):
        self.color = color
        self.step = 50
        self.point_start = [x0, y0]
        self.point_end = [x1, y1]

    def _get_position(self):
        return (
            self.point_start[0],
            self.point_start[1],
            self.point_end[0],
            self.point_end[1]
        )

    def create_square(self, squer=0):
        self.squer = squer
        self.point_start = [self.squer, 0]
        self.point_end = [
            self.point_start[0] + self.step,
            self.point_start[1] + self.step
        ]

    def _print_(self, canvas):
        self.my_square = canvas.create_rectangle(
            self._get_position(),
            fill=self.color
        )

    def keep_in_range(func):
        def func_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if self.point_start[0] < 0:
                self.point_start[0] = 0
                self.point_end[0] = self.step

            if self.point_start[1] < 0:
                self.point_start[1] = 0
                self.point_end[1] = self.step

            if self.point_start[0] > matrix[0] - self.step:
                self.point_start[0] = matrix[0] - self.step
                self.point_end[0] = matrix[0]

            if self.point_start[1] > matrix[0] - self.step:
                self.point_start[1] = matrix[0] - self.step
                self.point_end[1] = matrix[0]
            return result
        return func_wrapper

    @keep_in_range
    def turn_left(self, event=None):
        self.point_start[0] = self.point_start[0] - self.step
        self.point_end[0] = self.point_end[0] - self.step

    @keep_in_range
    def turn_right(self, event=None):
        self.point_start[0] = self.point_start[0] + self.step
        self.point_end[0] = self.point_end[0] + self.step

    @keep_in_range
    def turn_up(self, event=None):
        self.point_start[1] = self.point_start[1] - self.step
        self.point_end[1] = self.point_end[1] - self.step

    @keep_in_range
    def turn_down(self, event=None):
        self.point_start[1] = self.point_start[1] + self.step
        self.point_end[1] = self.point_end[1] + self.step


def game():

    main_window = tk.Tk()

    MyGameForm = MyForm(main_window)
    MyGameForm.canvas.delete('all')

    Green_square = Square(color='green')

    main_window.bind_all("<KeyPress-Left>", Green_square.turn_left)
    main_window.bind_all("<KeyPress-Right>", Green_square.turn_right)
    main_window.bind_all("<KeyPress-Up>", Green_square.turn_up)
    main_window.bind_all("<KeyPress-Down>", Green_square.turn_down)

    while True:

        if MyGameForm.new_game:
            exec_when = 0
            interval = 1
            squares_all = []
            game_score = 0
            Green_square.point_start = [300, 650]
            Green_square.point_end = [350, 700]
            MyGameForm.new_game = False

        if MyGameForm.is_running:
            MyGameForm.canvas.delete('all')

            now = time.time()

            for square in squares_all:
                MyGameForm.draw_object(square)

            if now > exec_when:
                squares_to_delate = []

                for s in squares_all:
                    if s._get_position()[1] == 650:
                        squares_to_delate.append(s)
                    s.turn_down()

                for x in squares_to_delate:
                    squares_all.remove(x)

                for i in range(randint(0, 6)):
                    w = randint(0, 13) * 50
                    sk = Square(color='red')
                    sk.create_square(w)
                    squares_all.append(sk)

                exec_when = time.time() + interval

                if interval > 0.4:
                    interval = interval * 0.99
                else:
                    interval = 0.4

                game_score = game_score + 1

            MyGameForm.draw_object(Green_square)
            MyGameForm.update_score(game_score)
            MyGameForm.update_time()

            for squ in squares_all:
                if squ._get_position() == Green_square._get_position():
                    MyGameForm.is_running = False

        main_window.update_idletasks()
        main_window.update()


game()
