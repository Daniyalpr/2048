import os
import numpy as np
def read_highscore(file_name="highscore.txt"):
    try:
        with open(file_name, "r") as f:
            return int(f.read())
    except:
        return 0
def write_highscore(score, file_name="highscore.txt"):
    with open(file_name, "w") as f:
        f.write(str(score))
def save_game(tiles, score, file_name="save.txt"):
    txt = ""
    for row in tiles:
        txt += " ".join(map(str, row)) + "\n"
    txt += "score: " + str(score)
    with open(file_name, "w") as f:
        f.write(txt)
    print("Save:\n" + txt)
def load_game(file_name="save.txt"):
    """
    The function returns a tuple which the first elment is
    a grid of numbers and second element is score.
    """
    grid = np.full((4, 4), None)
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            score_line = lines.pop()
            score = score_line.strip().split()[1]
            score = int(score)
            for idx, line in enumerate(lines):
                row = line[:-1].split()
                row = [int(i) for i in row]
                grid[idx] = row
    except:
        print("Error: The file is invalid")
        return None
    return (grid, score)

