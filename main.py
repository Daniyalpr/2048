import file_utils
import random
import tkinter as tk
import numpy as np
root = tk.Tk()
SIZE = 4
TILE_SIZE = 100
class Game():
    def __init__(self, root, nums:list=None):
        """
        nums: A 2d list conataining numbers in string. Note that 0 means empty tile.
        """
        self.can_play = True
        self.score = 0
        self.nums = np.array(nums) or np.full((SIZE, SIZE), 0)
        self.prev1_nums = None
        self.prev2_nums = None
        self.root = root
        self.root.bind("<Key>", self.key_hand)
        self.score_frame = tk.Frame(root)
        self.score_frame.pack(pady=5)
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


        self.reset_button = tk.Button(root,
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
        self.frame = tk.Frame(root, bg="gray")
        self.frame.pack()
        self.tiles = []
        self.score = 0
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

    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]
    def reverse(self, mat):
        new_mat = []
        for row in mat:
            new_mat.append(row[::-1])
        return new_mat

    def restart_game(self):
        self.score = 0
        self.nums = np.full((SIZE, SIZE), 0)
        self.can_play = True
        self.spawn()
        self.spawn()
        self.reset_button.pack_forget()
        self.update_ui()
    def update(self):
        self.update_ui()
        if self.game_over():
            self.can_play = False
            print("Game Over")
            if self.score > file_utils.read_highscore():
                file_utils.write_highscore(self.score)
            self.reset_button.pack(pady=5)
    def update_ui(self):
        self.score_board["text"] = f"SCORE\n{self.score}"
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                num = self.nums[i, j]
                st = str(num) if num != 0 else ""
                if tile["text"] != st:
                    backg, foreg = self.get_color(num)
                    tile.config(text=st, bg=backg, fg=foreg)
    def _combine(self):
        """
        Note: the function assumes that your move direction is Left.
        """
        for i, row in enumerate(self.nums):
            for idx in range(len(row)-1):
                if row[idx] == row[idx+1]:
                    self.score += 2 * row[idx]
                    self.nums[i, idx] = 2 * row[idx]
                    self.nums[i, idx+1] = 0


    def move_rows_left(self):
        new_mat = np.full((SIZE, SIZE), None)
        for idx, row in enumerate(self.nums):
          new_row = row[row != 0]
          new_row = np.append(new_row, [0] * (len(row) - len(new_row)))
          new_mat[idx] = new_row
        self.nums = new_mat
        
    def move(self, dire:str):
        if dire == "Left" or dire.lower() == "a":
            nums_copy = self.nums.copy()
            self.move_rows_left()
            self._combine()
            self.move_rows_left()
            if not np.array_equal(nums_copy, self.nums):
                self.spawn()
        elif dire == "Right" or dire.lower() == "d":
            self.nums = self.nums[:, ::-1]
            self.move("Left")
            self.nums = self.nums[:, ::-1]
        elif dire == "Up" or dire.lower() == "w":
            self.nums = self.nums.T
            self.move("Left")
            self.nums = self.nums.T
        elif dire == "Down" or dire.lower() == "s":
            self.nums = self.nums.T
            self.move("Right")
            self.nums = self.nums.T


    def key_hand(self, key):
        key_name = key.keysym
        if key_name in ["Right", "Left", "Down", "Up", "d", "a", "s", "w", "D", "A", "S", "W"] and self.can_play:
            self.move(key_name)
            self.update()
        if key_name == "Return" and not self.can_play:
            self.restart_game()

    def game_over(self):
        return (self.nums == 0).sum() == 0
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
