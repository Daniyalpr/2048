import os
def read_highscore(file_name="highscore.txt"):
    try:
        with open(file_name, "r") as f:
            return int(f.read())
    except:
        return 0
def write_highscore(score, file_name="highscore.txt"):
    with open(file_name, "w") as f:
        f.write(str(score))


