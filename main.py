import random
import tkinter as tk
root = tk.Tk()
SIZE = 4
TILE_SIZE = 100
class Game():
    def __init__(self, root, nums:list=None):
        """
        nums: A 2d list conataining numbers in string. Note that 0 means empty tile.
        """
        self.nums = nums or [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.root = root
        self.root.bind("<Key>", self.key_hand)
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

    def update_ui(self):
        tmp_tiles = []
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
            tmp_tiles.append(row)
        self.tiles = tmp_tiles
    def _combine(self):
        """
        Note: the function assumes that your move direction is Left.
        """
        for i, row in enumerate(self.nums):
            for idx in range(len(row)-1):
                if row[idx] == row[idx+1]:
                    self.nums[i][idx] = 2 * row[idx]
                    self.nums[i][idx+1] = 0



    def move_rows_left(self):
        for idx, row in enumerate(self.nums):
          new_row = [i for i in row if i != 0]
          new_row += [0] * (len(row) - len(new_row))
          self.nums[idx] = new_row
        
    def move(self, dire:str):
        if dire == "Left" or dire.lower() == "a":
            self.move_rows_left()
            self._combine()
            self.move_rows_left()
        if dire == "Right" or dire.lower() == "d":
            self.nums = self.reverse(self.nums)
            self.move("Left")
            self.nums = self.reverse(self.nums)
        if dire == "Up" or dire.lower() == "w":
            self.nums = self.transpose(self.nums)
            self.move("Left")
            self.nums = self.transpose(self.nums)
        if dire == "Down" or dire.lower() == "s":
            self.nums = self.transpose(self.nums)
            self.move("Right")
            self.nums = self.transpose(self.nums)


    def key_hand(self, key):
        key_name = key.keysym
        if key_name in ["Right", "Left", "Down", "Up", "d", "a", "s", "w", "D", "A", "S", "W"]:
            self.move(key_name)
            self.spawn()
        self.update_ui()

    def spawn(self):
        emp = []
        rand = random.random()
        spawn_num = 2 if rand <= 0.9 else 4
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tiles[i][j].cget("text") == "":
                    emp.append((i, j))
        x, y = random.choice(emp)
        self.nums[x][y] = spawn_num

    def get_color(self, num:int):
        """
        num: the number that you want to get color of.
        Note: the function will return a tuple which the first
        element corrosponds to background color and the second
        one is foreground color.
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
root.mainloop()
