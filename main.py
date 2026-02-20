import file_utils
import random
import tkinter as tk
from tkinter import filedialog
import numpy as np
root = tk.Tk()
SIZE = 4
TILE_SIZE = 100
class Game():
    str_colors = {
            "green": "#2a9d8f",
            "red": "#e63946"
            }
    def __init__(self, root, nums:list=None):
        """
        nums: A 2d list conataining numbers in string. Note that 0 means empty tile.
        """
        self.can_play = True
        self.score = 0
        self.nums = np.array(nums) or np.full((SIZE, SIZE), 0)
        self.prev1_nums = None
        self.prev2_nums = None
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, padx=3) 
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0)
        self.root = root
        self.root.bind("<Key>", self.key_hand)
        self.score_frame = tk.Frame(self.left_frame)
        self.score_frame.grid(row=0, column=0 , pady=5)
        self.score_board = tk.Label(self.score_frame, width=14, height=2, text=f"SCORE\n{self.score}", bg=self.get_color(4)[0], fg=self.get_color(4)[1], font=("Arial", 15, "bold"))
        self.score_board.grid(row=1, column=1, padx=5)

        # max score board
        highscore = file_utils.read_highscore()
        self.highscore_board = tk.Label(self.score_frame,
                                        width=14,
                                        height=2,
                                        text=f"BEST\n{highscore}",
                                        bg=self.get_color(2)[0], 
                                        fg=self.get_color(2)[1], 
                                        font=("Arial", 15, "bold"), 
                                        highlightthickness=2, 
                                        highlightcolor=self.get_color(2)[1], 
                                        highlightbackground=self.get_color(2)[1], 
                                       )
        self.highscore_board.grid(row=1, column=2, padx=5)
        self.status_txt = tk.Label(self.right_frame, text="PLAY!",
                                 font=("Arial", 20, "bold"),
                                 fg=self.str_colors["green"],
                                 )
        self.status_txt.pack()
        load_button = tk.Button(self.right_frame,
                                       width=14,
                                       height=2, 
                                       text="LOAD", 
                                       bg=self.get_color(2)[0], 
                                       fg=self.get_color(2)[1], 
                                       font=("Arial", 15, "bold"),
                                        highlightthickness=2, 
                                        highlightcolor=self.get_color(2)[1], 
                                        highlightbackground=self.get_color(2)[1], 
                                       command=self.load
                                       )
        save_button = tk.Button(self.right_frame,
                                       width=14,
                                       height=2, 
                                       text="SAVE", 
                                       bg=self.get_color(2)[0], 
                                       fg=self.get_color(2)[1], 
                                       font=("Arial", 15, "bold"),
                                        highlightthickness=2, 
                                        highlightcolor=self.get_color(2)[1], 
                                        highlightbackground=self.get_color(2)[1], 
                                       command=self.save
                                       )
        self.reset_button = tk.Button(self.right_frame,
                                       width=14,
                                       height=2, 
                                       text="NEW GAME", 
                                       bg=self.get_color(2)[0], 
                                       fg=self.get_color(2)[1], 
                                       font=("Arial", 15, "bold"),
                                        highlightthickness=2, 
                                        highlightcolor=self.get_color(2)[1], 
                                        highlightbackground=self.get_color(2)[1], 
                                       command=self.restart_game
                                       )
        self.undo_left=2
        self.undo_button = tk.Button(
                self.right_frame,
                width=5,
                height=1,
                text=f"undo {self.undo_left}",
                bg=self.get_color(4)[0],
                fg=self.get_color(4)[1],
                font=("Arial", 12, "bold"),
                highlightthickness=2,
                highlightcolor=self.get_color(4)[1],
                highlightbackground=self.get_color(4)[1],
                command=self.undo
                )
        load_button.pack(pady=(20, 0))
        save_button.pack(pady=4)
        self.reset_button.pack(pady=4)
        self.undo_button.pack()
        self.undo_button_changed = False
        self.frame = tk.Frame(self.left_frame, bg="gray")
        self.frame.grid(row=1, column=0)
        self.tiles = []
        self.score = 0

        self.greet_txt = tk.Label(self.right_frame, text="...",
                                 font=("Arial", 9, "bold"),
                                 fg=self.get_color(2)[1],
                                 )
        self.status_txt.pack(pady=2)
        self.greet_txt.pack(pady=(4, 0))
        # Const UI elemnts
        copyright_txt = tk.Label(self.right_frame, text="© 2026 github.com/Daniyalpr.\nAll rights reserved :)",
                                 font=("Arial", 7, "bold"),
                                 fg=self.get_color(2)[1],
                                 )
        copyright_txt.pack(pady=(30, 0))
        # Creating tiles
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                num = self.nums[i][j]
                label = tk.Label(
                        self.frame,
                        width=4,
                        height=2,
                        bg=self.get_color(num)[0],
                        fg=self.get_color(num)[1],
                        text = num if num != 0 else "",
                        font=("Arial", 24, "bold")
                        )
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.tiles.append(row)

        self.spawn()
        self.spawn()
        self.update_ui()

    def load(self):
        file_path = filedialog.askopenfilename(
                filetypes=[("Game Save Files", "*.txt")]
                )
        if not file_path:
            return
        grid, score = file_utils.load_game(file_path)
        self.restart_game()
        self.nums = grid
        self.score = score
        self.update()
    def save(self):
        file_path = filedialog.asksaveasfilename(
                filetypes=[("Game Save Files", "*.txt")]
                )
        if not file_path:
            return
        file_utils.save_game(self.nums, self.score, file_path)
    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]
    def reverse(self, mat):
        new_mat = []
        for row in mat:
            new_mat.append(row[::-1])
        return new_mat

    def undo(self):
        if self.undo_left <= 0 or self.prev1_nums is None or not self.can_play:
            return 
        self.undo_left -= 1
        self.nums, self.prev1_nums, self.prev2_nums = self.prev1_nums, self.prev2_nums, None
        self.undo_button_changed = True
        self.update_ui()
        print("undo")

    def restart_game(self):
        self.score = 0
        self.nums = np.full((SIZE, SIZE), 0)
        self.can_play = True
        self.undo_left = 2
        self.undo_button_changed = True
        self.status_txt.config(text="PLAY!", fg=self.str_colors["green"])
        self.greet_txt.config(text="...")
        self.spawn()
        self.spawn()
        self.update_ui()
    def update(self):
        self.update_ui()
        if self.game_over():
            self.can_play = False
            print("Game Over")
            if self.score > file_utils.read_highscore():
                file_utils.write_highscore(self.score)
        self.update_ui()
    def get_greeting(self):
        high_score = [
                "LEGEND STATUS UNLOCKED 🏆",
                "New high score!! You're unstoppable 🚀",
                "Board destroyed. Absolute domination 👑",
                "You cooked. And it was gourmet ✨",
                "Tiles trembling right now 🎯",
                "Brain = 200 IQ 🧠",
                "That was elite gameplay 🔥",
                "You didn’t win… you conquered ⚔️"
                ]
        med_score = [
                "Solid run! 👏",
                "Nice moves there ✨",
                "You're improving! 🚀",
                "That was smooth 😌",
                "Almost legendary 👀",
                "Keep going — you're close ⚡",
                "Progress detected 📈",
                "Next round is yours 😎"
                ]

        low_score = [
                "The tiles said 'not today' 😭",
                "Warm-up round? 👀",
                "Plot twist: the board fought back 😤",
                "Oops 😅 Try again!",
                "That was just practice mode 🎮",
                "Shake it off and run it back 💪",
                "Every legend has a backstory 📖",
                "Redemption arc loading... ⏳"
                ]

        if self.score == int(file_utils.read_highscore()):
            return "Congrats, that's a new high score!"   
        if self.score >= 2800:
            return random.choice(high_score)
        elif 1800 <= self.score:
            return random.choice(med_score)
        else: 
            return random.choice(low_score)

    def update_ui(self):
        self.score_board["text"] = f"SCORE\n{self.score}"
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                num = self.nums[i, j]
                st = str(num) if num != 0 else ""
                if tile["text"] != st:
                    backg, foreg = self.get_color(num)
                    tile.config(text=st, bg=backg, fg=foreg)
        # Updating undo button
        if self.undo_button_changed:
            backg, foreg = self.get_color(4) if self.undo_left > 0 else self.get_color(0)
            self.undo_button.config(text=f"undo {self.undo_left}", bg=backg, fg=foreg, 
                       highlightcolor=foreg, 
                       highlightbackground=foreg, 
                        )
            self.undo_button_changed = False
        if not self.can_play:
            self.status_txt.config(fg=self.str_colors["red"], text="GAME OVER")
            self.greet_txt.config(text=self.get_greeting())
            self.update_status = False

    def _combine(self, mat):
        """
        Note: the function assumes that your move direction is Left.
        """
        for i, row in enumerate(mat):
            for idx in range(len(row)-1):
                if row[idx] == row[idx+1]:
                    self.score += 2 * row[idx]
                    mat[i, idx] = 2 * row[idx]
                    mat[i, idx+1] = 0
        return mat


    def move_rows_left(self, mat):
        new_mat = np.full((SIZE, SIZE), None)
        for idx, row in enumerate(mat):
          new_row = row[row != 0]
          new_row = np.append(new_row, [0] * (len(row) - len(new_row)))
          new_mat[idx] = new_row
        return new_mat
        
    def move(self, dire:str, mat):
        if dire == "Left" or dire.lower() == "a":
            mat = self.move_rows_left(mat)
            mat = self._combine(mat)
            mat = self.move_rows_left(mat)
            return mat
        elif dire == "Right" or dire.lower() == "d":
            mat = mat[:, ::-1]
            mat = self.move("Left", mat)
            mat = mat[:, ::-1]
        elif dire == "Up" or dire.lower() == "w":
            mat = mat.T
            mat = self.move("Left", mat)
            mat = mat.T
        elif dire == "Down" or dire.lower() == "s":
            mat = mat.T
            mat = self.move("Right", mat)
            mat = mat.T
        return mat
    def key_hand(self, key):
        key_name = key.keysym
        if key_name in ["Right", "Left", "Down", "Up", "d", "a", "s", "w", "D", "A", "S", "W"] and self.can_play:
            nums_copy = self.nums.copy()
            self.nums = self.move(key_name, self.nums)
            if not np.array_equal(nums_copy, self.nums):
                self.prev1_nums, self.prev2_nums = nums_copy, self.prev1_nums
                self.spawn()
                self.update()
        if key_name == "Return" and not self.can_play:
            self.restart_game()

    def game_over(self):
        if (self.nums == 0).sum() != 0:
            return False
        nums_copy = self.nums.copy()
        for move in ["Right", "Left", "Up", "Down"]:
            new_nums = self.move(move, nums_copy)
            if not np.array_equal(nums_copy, new_nums):
                return False
        return True
    def spawn(self):
        rand = random.random()
        spawn_num = 2 if rand <= 0.9 else 4
        emp = list(zip(*(np.where(self.nums == 0))))
        x, y = random.choice(emp)
        self.nums[x, y] = spawn_num

    def get_color(self, num:int):
        """
        The function will return a tuple which the first
        element corrosponds to background color and the second
        one is foreground color.

        num: the number that you want to get color of.
        """
        colors = {
            0: ("#cdc1b4", "#776e65"),      
            2: ("#eee4da", "#776e65"),
            4: ("#ede0c8", "#776e65"),
            8: ("#f2b179", "white"),
            16: ("#f59563", "white"),
            32: ("#f67c5f", "white"),
            64: ("#f65e3b", "white"),
            128: ("#edcf72", "white"),
            256: ("#edcc61", "white"),
            512: ("#edc850", "white"),
            1024: ("#edc53f", "white"),
            2048: ("#edc22e", "white"),
        }
        return colors[num]

game = Game(root)
root.title("2048 Game")
root.mainloop()
