import random
import tkinter as tk
root = tk.Tk()
SIZE = 4
TILE_SIZE = 100
class Game():
    def __init__(self, root, nums:list=None):
        """
        nums: A 2d list conataining numbers in string. Note that "" means empty tile.
        """
        self.nums = nums or [["" for _ in range(SIZE)] for _ in range(SIZE)]
        self.root = root
        self.frame = tk.Frame(root, bg="gray")
        self.frame.pack()
        self.tiles = []
        # Creating tiles
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                label = tk.Label(
                        self.frame,
                        width=4,
                        height=2,
                        bg="lightgray",
                        text = self.nums[i][j],
                        font=("Arial", 24, "bold")
                        )
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.tiles.append(row)

        self.spawn()
        self.spawn()
    def spawn(self):
        emp = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tiles[i][j].cget("text") == "":
                    emp.append((i, j))
        x, y = random.choice(emp)
        self.tiles[x][y].config(text=2)


game = Game(root)
root.mainloop()
