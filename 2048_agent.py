import random
import gym
from gym import spaces
import numpy as np
SIZE = 4
class Game2048Agent(gym.Env):
    
    def __init__(self, render=False):
        self.render = render
        self.observation_space = spaces.Box(
            low=0, high=16, shape=(SIZE, SIZE), dtype=np.float32
        )

        # Action: 0=up, 1=down, 2=left, 3=right
        self.action_space = spaces.Discrete(4)
        self.reset()
        if render:
            self.update_gui()

    def _move_rows_left(self, mat):
        new_mat = np.zeros((SIZE, SIZE), dtype=np.float32)
        for idx, row in enumerate(mat):
          new_row = row[row != 0]
          new_row = np.append(new_row, [0] * (len(row) - len(new_row)))
          new_mat[idx] = new_row
        return new_mat

    def spawn(self, mat):
        rand = random.random()
        spawn_num = 2 if rand <= 0.9 else 4
        emp = list(zip(*(np.where(mat == 0))))
        x, y = random.choice(emp)
        mat[x, y] = spawn_num
        return mat

    def _combine(self, mat):
        """
        Note: the function assumes that your move direction is Left.
        it'll return new mat and reward as a tuple which first element
        of the tuple is new mat and second is the reward
        """
        reward = 0
        for i, row in enumerate(mat):
            for idx in range(len(row)-1):
                if row[idx] == row[idx+1]:
                    reward += 2 * row[idx]
                    mat[i, idx] = 2 * row[idx]
                    mat[i, idx+1] = 0
        return mat, reward
    def get_observation(self):
        obs = np.where(self.board == 0, 0, np.log2(self.board))
        return obs.astype(np.float32)

    def step(self, action):
        # Action: 0=up, 1=down, 2=left, 3=right
        mp = {0:"w", 1:"s", 2:"a", 3:"d"}
        reward = self.move(mp[action])
        done = self.game_over(self.board)
        return self.get_observation(), reward, done, {}

    def reset(self):
        self.score = 0
        self.board = np.zeros((4, 4), dtype=np.float32)
        self.spawn(self.board)
        self.spawn(self.board)
        return self.get_observation()
    def game_over(self, mat):
        if 2048 in mat:
            return True
        if (mat == 0).any():
            return False
        for dire in ["Right", "Left", "Up", "Down"]:
            new_nums, _ = self._move(dire, mat)
            if not np.array_equal(mat, new_nums):
                return False
        return True

    def move(self, dire:str):
        """
        it'll return reward
        """
        board_copy = self.board.copy()
        board_copy, reward = self._move(dire, board_copy)
        if not np.array_equal(board_copy, self.board):
            self.score += reward
            self.board = board_copy
            self.board = self.spawn(self.board)
        else:
            # Give punshiment if the agent did invalid move
            reward -= 1
        if self.render:
            self.update_gui()
        return reward
    def _move(self, dire:str, mat):
        new_mat = mat.copy()
        if dire == "Left" or dire.lower() == "a":
            new_mat = self._move_rows_left(new_mat)
            new_mat, reward = self._combine(new_mat)
            new_mat = self._move_rows_left(new_mat)
            return new_mat, reward
        elif dire == "Right" or dire.lower() == "d":
            new_mat = new_mat[:, ::-1]
            new_mat, reward = self._move("Left", new_mat)
            new_mat = new_mat[:, ::-1]
        elif dire == "Up" or dire.lower() == "w":
            new_mat = new_mat.T
            new_mat, reward = self._move("Left", new_mat)
            new_mat = new_mat.T
        elif dire == "Down" or dire.lower() == "s":
            new_mat = new_mat.T
            new_mat, reward = self._move("Right", new_mat)
            new_mat = new_mat.T
        return new_mat, reward
    def update_gui(self):
        print(self.board)
game = Game2048Agent(True)
while True:
    do = input("Give input: ").strip()
    if do == "exit":
        break
    game.move(do)
