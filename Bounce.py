import asyncio
from tkinter import *
import random
import time
import tkinter.colorchooser as colorchooser


class Ball:
    def __init__(self, canvas, paddle, color, score, speed):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.speed = speed
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -self.speed
        self.canvas_height = None
        self.canvas_width = None
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if (pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2] and
                pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]):
            self.score.increment()
            return True
        return False

    def set_canvas_dimensions(self):
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = self.speed
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -self.speed
        if pos[0] <= 0:
            self.x = self.speed
        if pos[2] >= self.canvas_width:
            self.x = -self.speed

    def delete(self):
        self.canvas.delete(self.id)


class Paddle:
    def __init__(self, canvas, color, speed):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.speed = speed
        self.x = 0
        self.canvas_width = None
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def set_canvas_dimensions(self):
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed

    def delete(self):
        self.canvas.delete(self.id)


class Score:
    def __init__(self, canvas):
        self.value = 0
        self.canvas = canvas
        self.id = canvas.create_text(
            260, 80, text="0", font=("Arial Rounded MT Bold", 25), fill='black')

    def increment(self):
        self.value += 1
        self.canvas.itemconfig(self.id, text="{}".format(self.value))

    def reset(self):
        self.value = 0
        self.canvas.itemconfig(self.id, text="0")


class Game:
    def __init__(self, canvas, tk, speed_ball, speed_paddle,
                 main_menu_remover, main_menu):
        self.canvas = canvas
        self.tk = tk
        self.color_of_ball = 'red'
        self.color_of_paddle = 'blue'
        self.speed_paddle = speed_paddle
        self.speed_ball = speed_ball
        self.score = None
        self.paddle = None
        self.ball = None
        self.restart_message = None
        self.previous_score = 0
        self.start_message = None
        self.level = 1
        self.main_menu_remover = main_menu_remover
        self.main_menu = main_menu
        self.restart_button = Button(
            tk, text="Restart", font=("Arial Rounded MT Bold", 20),
            relief=GROOVE, command=self.restart_game)
        self.main_menu_button = Button(
            tk, text="Main Menu", font=("Copperplate Gothic Bold", 10),
            relief=GROOVE, command=self.main_menu)

    def enter_game(self):
        self.score = Score(canvas)
        self.paddle = Paddle(
            canvas, self.color_of_paddle, self.speed_paddle)
        self.ball = Ball(
            canvas, self.paddle, self.color_of_ball,
            self.score, self.speed_ball)
        self.main_menu_button.place(x=10, y=10)
        self.canvas.delete(self.restart_message)
        self.main_menu_remover()
        self.start_game_message()

    def start_game_message(self):
        self.start_message = canvas.create_text(
            250, 240, text="Space to Start",
            font=("Arial Rounded MT Bold", 30), fill='black')

    def start_game(self):
        self.canvas.delete(self.start_message)
        self.canvas.delete(self.restart_message)
        self.game_loop()

    def game_loop(self):
        self.ball.set_canvas_dimensions()
        self.paddle.set_canvas_dimensions()
        while not self.ball.hit_bottom:
            self.leveler()
            self.ball.draw()
            self.paddle.draw()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
        self.game_over()

    def leveler(self):
        if self.score.value >= self.previous_score + 5:
            self.level += 1
            text = canvas.create_text(
                250, 190, text=f"Level {self.level}",
                font=("Arial Rounded MT Bold", 40), fill='blue')
            tk.after(450, lambda: canvas.delete(text))
            self.ball.speed *= 1.10
            self.paddle.speed *= 1.05
            self.previous_score += 5

    def game_over(self):
        self.game_over_message = self.canvas.create_text(
            260, 150, text="Game Over",
            font=("Arial Rounded MT Bold", 50), fill='red')
        self.restart_button.place(x=190, y=200)

    def restart_game(self, event=None):
        self.ball.delete()
        self.paddle.delete()
        self.canvas.delete(self.game_over_message)
        self.canvas.delete(self.score.id)
        self.restart_message = canvas.create_text(
            250, 240, text="Space to Try Again",
            font=("Arial Rounded MT Bold", 30), fill='black')
        self.paddle = Paddle(
            canvas, self.color_of_paddle, self.speed_paddle)
        self.score = Score(canvas)
        self.ball = Ball(
            canvas, self.paddle, self.color_of_ball,
            self.score, self.speed_ball)
        self.level = 1
        self.previous_score = 0
        self.restart_button.place_forget()

    def remover(self, text):
        self.canvas.delete(text)


# Function Definitions
def display_instructions():
    instructions_canvas = Canvas(
        tk, width=500, height=400, bd=0,
        highlightthickness=1, highlightbackground="black")
    instructions_canvas.pack()
    instructions_canvas.create_text(
        250, 195, text="Instructions:\n\n1. Select your level from the main menu \n\n2. Click the space bar to begin the game \n\n3. Use left and right arrow keys to move the paddle.\n\n4. Bounce the ball off the paddle to score points. \n\n5. Every 5 points you will level up increasing \n   ball speed by 10%. \n\n5. Click restart to try again \n\n\n\n **DON'T PRESS SPACE BEFORE \n HITTING THE RESTART BUTTON",
        font=("Arial Rounded MT Bold", 10))
    close_instruction_button = Button(
        tk, text="Close Instructions",
        command=lambda: remove_instructions(instructions_canvas,
                                            close_instruction_button))
    close_instruction_button.pack()


def remove_instructions(canvas, button):
    canvas.pack_forget()
    button.pack_forget()


def level_menu():
    global easy_button, medium_button, hard_button
    game.canvas.delete('all')
    difficulty_button.place_forget()
    difficulty_message = canvas.create_text(
        250, 90, text="Difficulty",
        font=("Copperplate Gothic Bold", 40), fill='black')
    easy_button = Button(
        tk, text="Easy", font=("Eras Bold ITC", 20),
        width=10, height=1, relief=GROOVE, command=start_easy_game)
    easy_button.place(x=150, y=135)
    medium_button = Button(
        tk, text="Medium", font=("Eras Bold ITC", 20),
        width=10, height=1, relief=GROOVE, command=start_medium_game)
    medium_button.place(x=150, y=185)
    hard_button = Button(
        tk, text="Hard", font=("Eras Bold ITC", 20),
        width=10, height=1, relief=GROOVE, command=start_hard_game)
    hard_button.place(x=150, y=235)


def main_menu():
    global menu_message, difficulty_button, customize_button
    difficulty_button = Button(
        tk, text="Difficulty", font=("Eras Bold ITC", 20),
        width=10, height=1, relief=GROOVE, command=level_menu)
    difficulty_button.place(x=150, y=150)
    game.canvas.delete('all')
    game.main_menu_button.place_forget()
    menu_message = canvas.create_text(
        245, 90, text="Main Menu",
        font=("Copperplate Gothic Bold", 40), fill='black')


def main_menu_remover():
    canvas.delete(menu_message)
    easy_button.place_forget()
    medium_button.place_forget()
    hard_button.place_forget()


def start_easy_game():
    game.canvas.delete('all')
    text = canvas.create_text(
        430, 20, text="Difficulty: Easy",
        font=("Copperplate Gothic Bold", 10), fill='black')
    tk.after(100, text)
    game.speed_ball = 3
    game.speed_paddle = 3.5
    game.enter_game()


def start_medium_game():
    game.canvas.delete('all')
    text = canvas.create_text(
        420, 20, text="Difficulty: Medium",
        font=("Copperplate Gothic Bold", 10), fill='black')
    tk.after(100, text)
    game.speed_ball = 4
    game.speed_paddle = 4
    game.enter_game()


def start_hard_game():
    game.canvas.delete('all')
    text = canvas.create_text(
        430, 20, text="Difficulty: Hard",
        font=("Copperplate Gothic Bold", 10), fill='black')
    tk.after(100, text)
    game.speed_ball = 5.5
    game.speed_paddle = 5
    game.enter_game()


# Main Scriptzzz
tk = Tk()
click_count = 0
tk.title("Bounce: Roan Cowan")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0,
                highlightthickness=2, bg = 'yellow', highlightbackground="black")
canvas.pack()
game = Game(canvas, tk, 0, 0, main_menu_remover, main_menu)
main_menu()
tk.update()
canvas.bind('<space>', lambda event: game.start_game())
canvas.focus_set()
instruction_button = Button(
    tk, text="Instructions", command=display_instructions)
instruction_button.pack()
tk.mainloop()
