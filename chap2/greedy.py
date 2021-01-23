import numpy as np
from scipy import stats
import random
import matplotlib.pyplot as plt

n = 10
probs = np.random.rand(n)
eps = 0.2

def get_reward(prob, n=10):
    reward = 0
    for i in range(n):
        if random.random() < prob:
            reward += 1
    return reward
ys = [get_reward(0.7) for _ in range(2000)];
xs = np.arange(len(ys))
plt.plot(xs, ys)
plt.show()
print(np.mean([get_reward(0.7) for _ in range(2000)]))

