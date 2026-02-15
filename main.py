import tkinter as tk
root = tk.Tk()
SIZE = 4
TILE_SIZE = 100
class Game():
    def __init__(self, root, nums:list=None):
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

game = Game(root)
root.mainloop()
