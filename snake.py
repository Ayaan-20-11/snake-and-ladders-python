import tkinter as tk
import random

class SnakeAndLadders:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladders")

        self.main_frame = tk.Frame(self.root, bg="lightblue")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Canvas(self.main_frame, bg="lightblue")
        self.v_scroll = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas_frame.yview)
        self.canvas_frame.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollable_frame = tk.Frame(self.canvas_frame, bg="lightblue")
        self.canvas_window = self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all")))
        self.canvas_frame.bind_all("<MouseWheel>", self._on_mousewheel)

        self.num_players = tk.IntVar()
        self.players = []
        self.positions = []
        self.current_player = 0
        self.ladders = {}
        self.snakes = {}
        self.finished_players = []
        self.game_started = [False] * 4

        self.ask_num_players()

    def _on_mousewheel(self, event):
        self.canvas_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ask_num_players(self):
        self.center_frame = tk.Frame(self.scrollable_frame, bg="lightblue")
        self.center_frame.pack(pady=20)

        label = tk.Label(self.center_frame, text="Enter number of players (2-4):", font=("Helvetica", 16), bg="lightblue")
        label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        entry = tk.Entry(self.center_frame, textvariable=self.num_players, font=("Helvetica", 16))
        entry.grid(row=1, column=0, columnspan=2, pady=(10, 20))

        button = tk.Button(self.center_frame, text="Start Game", command=self.ask_player_names, font=("Helvetica", 16), bg="lightgreen")
        button.grid(row=2, column=0, columnspan=2, pady=(10, 20))

    def ask_player_names(self):
        num_players = self.num_players.get()
        if 2 <= num_players <= 4:
            for widget in self.center_frame.winfo_children():
                widget.destroy()

            self.player_names = []
            for i in range(num_players):
                label = tk.Label(self.center_frame, text=f"Enter name for Player {i + 1}:", font=("Helvetica", 16), bg="lightblue")
                label.grid(row=i, column=0, pady=5)

                entry = tk.Entry(self.center_frame, font=("Helvetica", 16))
                entry.grid(row=i, column=1, pady=5)
                self.player_names.append(entry)

            button = tk.Button(self.center_frame, text="Show Rules", command=self.show_rules, font=("Helvetica", 16), bg="lightgreen")
            button.grid(row=num_players, column=0, columnspan=2, pady=(10, 20))
        else:
            label = tk.Label(self.center_frame, text="Please enter a number between 2 and 4", font=("Helvetica", 16), bg="lightblue")
            label.grid(row=3, column=0, columnspan=2, pady=(10, 20))

    def show_rules(self):
        self.player_names = [entry.get() for entry in self.player_names]
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        rules_text = (
            "Rules:\n"
            "- White lines = ladders (go up)\n"
            "- Black lines = snakes (go down)\n"
            "- Roll 1 or 6 to start\n"
            "- Roll 6 = extra turn\n"
            "- First to reach 100 wins!"
        )

        label = tk.Label(self.center_frame, text=rules_text, font=("Helvetica", 14), bg="lightblue", justify="left")
        label.pack(pady=20)

        button = tk.Button(self.center_frame, text="Start Game", command=self.start_game, font=("Helvetica", 16), bg="lightgreen")
        button.pack(pady=20)

    def start_game(self):
        self.current_player = random.randint(0, len(self.player_names) - 1)
        self.center_frame.pack_forget()
        self.create_board()

        self.colors = ["blue", "red", "green", "yellow"]
        for i in range(len(self.player_names)):
            token_x = -30
            token_y = 900 - (i * 30 + 30)
            player = self.canvas.create_oval(token_x, token_y, token_x + 30, token_y + 30, fill=self.colors[i], outline="black", width=2)
            self.players.append(player)
            self.positions.append(0)

        self.controls_frame = tk.Frame(self.scrollable_frame, bg="lightblue")
        self.controls_frame.pack(pady=10)

        self.dice_button = tk.Button(self.controls_frame, text="Roll Dice", command=self.roll_dice, font=("Helvetica", 16), bg="lightgreen")
        self.dice_button.pack(pady=5)

        self.dice_label = tk.Label(self.controls_frame, text="", font=("Helvetica", 16))
        self.dice_label.pack(pady=5)

        self.turn_label = tk.Label(self.controls_frame, text=f"{self.player_names[self.current_player]}'s turn", font=("Helvetica", 16))
        self.turn_label.pack(pady=5)

    def create_board(self):
        self.canvas = tk.Canvas(self.scrollable_frame, width=900, height=900, bg="lightblue")
        self.canvas.pack()

        box_colors = ["red", "green", "blue", "yellow", "orange", "purple"]
        for y in range(10):
            for x in range(10):
                color = random.choice(box_colors)
                self.canvas.create_rectangle(x * 90, y * 90, x * 90 + 90, y * 90 + 90, fill=color)
                number = (9 - y) * 10 + (x + 1) if (9 - y) % 2 == 0 else (9 - y) * 10 + (10 - x)
                self.canvas.create_text(x * 90 + 45, y * 90 + 45, text=str(number), font=("Helvetica", 16), fill="white")

        messages = {
            3: "i exercise",
            12: "i eat fruits",
            15: "homemade food",
            20: "drink water",
            27: "milk is magic",
            51: "love veggies",
            60: "candy craze",
            63: "care plants",
            87: "no brush",
            93: "maggi lover",
            99: "ate junk food"
        }
        for pos, text in messages.items():
            x, y = self.get_coordinates(pos)
            self.canvas.create_text(x, y - 25, text=text, font=("Helvetica", 7), fill="black")
            self.canvas.create_text(x, y, text=str(pos), font=("Helvetica", 16), fill="white")

        self.create_ladders()
        self.create_snakes()

    def create_ladders(self):
        ladder_positions = [(3, 22), (5, 8), (12, 29), (20, 35), (15, 36), (27, 56), (34, 44), (51, 67), (63, 81), (68, 88)]
        for start, end in ladder_positions:
            self.ladders[start] = end
            self.canvas.create_line(*self.get_coordinates(start), *self.get_coordinates(end), fill="white", width=5)

    def create_snakes(self):
        snake_positions = [(17, 7), (60, 18), (68, 49), (87, 24), (99, 46), (93, 73)]
        for start, end in snake_positions:
            self.snakes[start] = end
            self.draw_snake(start, end)

    def draw_snake(self, start, end):
        start_x, start_y = self.get_coordinates(start)
        end_x, end_y = self.get_coordinates(end)
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="black", width=5)
        self.canvas.create_line(start_x, start_y, start_x + 10, start_y - 10, fill="black", width=2)
        self.canvas.create_line(start_x, start_y, start_x - 10, start_y - 10, fill="black", width=2)

    def roll_dice(self):
        dice = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {dice}")

        if not self.game_started[self.current_player] and dice not in [1, 6]:
            self.turn_label.config(text=f"{self.player_names[self.current_player]} needs a 1 or 6 to start!")
        else:
            self.game_started[self.current_player] = True
            self.move_player(dice)

        self.turn_label.config(text=f"{self.player_names[self.current_player]}'s turn")

    def move_player(self, steps):
        new_position = self.positions[self.current_player] + steps
        if new_position > 100:
            new_position = self.positions[self.current_player]
        if new_position in self.ladders:
            new_position = self.ladders[new_position]
        elif new_position in self.snakes:
            new_position = self.snakes[new_position]
        self.positions[self.current_player] = new_position

        x, y = self.get_coordinates(new_position)
        self.canvas.coords(self.players[self.current_player], x - 15, y - 15, x + 15, y + 15)

        if new_position == 100:
            self.finished_players.append(self.player_names[self.current_player])
            self.canvas.coords(self.players[self.current_player], -100, -100, -80, -80)

            remaining = [i for i in range(len(self.players)) if self.player_names[i] not in self.finished_players]
            if len(remaining) == 0 or len(remaining) == 1:
                self.show_winner_summary()
                return

            self.current_player = remaining[0]
        else:
            if steps != 6:
                self.current_player = (self.current_player + 1) % len(self.players)
                while self.player_names[self.current_player] in self.finished_players:
                    self.current_player = (self.current_player + 1) % len(self.players)

    def show_winner_summary(self):
        self.root.destroy()
        summary_root = tk.Tk()
        summary_root.title("Game Over")
        summary_root.configure(bg="lightblue")

        label = tk.Label(summary_root, text="Winner Rankings:", font=("Helvetica", 20), bg="lightblue")
        label.pack(pady=20)

        for idx, name in enumerate(self.finished_players, start=1):
            tk.Label(summary_root, text=f"{idx}. {name}", font=("Helvetica", 16), bg="lightblue").pack(pady=5)

        tk.Button(summary_root, text="Play Again", font=("Helvetica", 16), bg="lightgreen",
                  command=summary_root.destroy).pack(pady=20)

        summary_root.mainloop()

    def get_coordinates(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        x = col * 90 + 45 if row % 2 == 0 else (9 - col) * 90 + 45
        y = (9 - row) * 90 + 45
        return x, y

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("950x700")
    game = SnakeAndLadders(root)
    root.mainloop()
