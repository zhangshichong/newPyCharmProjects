import numpy as np
import torch
from IPython.core.display import clear_output

from Gridworld import Gridworld
import random
import matplotlib.pyplot as plt

l1, l2, l3, l4 = 64, 150, 100, 4

model = torch.nn.Sequential(
    torch.nn.Linear(l1, l2),
    torch.nn.ReLU(),
    torch.nn.Linear(l2, l3),
    torch.nn.ReLU(),
    torch.nn.Linear(l3, l4)
)

loss_fn = torch.nn.MSELoss()
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
gamma = 0.9
epsilon = 1.0

action_set = {
    0: 'u',
    1: 'd',
    2: 'l',
    3: 'r',
}

epochs = 1000
losses = []  # A
for i in range(epochs):  # B
    game = Gridworld(size=4, mode='static')  # C
    state_ = game.board.render_np().reshape(1, 64) + np.random.rand(1, 64) / 10.0  # D
    state1 = torch.from_numpy(state_).float()  # E
    status = 1  # F
    while (status == 1):  # G
        qval = model(state1)  # H
        qval_ = qval.data.numpy()
        if (random.random() < epsilon):  # I
            action_ = np.random.randint(0, 4)
        else:
            action_ = np.argmax(qval_)

        action = action_set[action_]  # J
        game.makeMove(action)  # K
        state2_ = game.board.render_np().reshape(1, 64) + np.random.rand(1, 64) / 10.0
        state2 = torch.from_numpy(state2_).float()  # L
        reward = game.reward()
        with torch.no_grad():
            newQ = model(state2.reshape(1, 64))
        maxQ = torch.max(newQ)  # M
        if reward == -1:  # N
            Y = reward + (gamma * maxQ)
        else:
            Y = reward
        Y = torch.Tensor([Y]).detach()
        X = qval.squeeze()[action_]  # O
        loss = loss_fn(X, Y)  # P
        print(i, loss.item())
        clear_output(wait=True)
        optimizer.zero_grad()
        loss.backward()
        losses.append(loss.item())
        optimizer.step()
        state1 = state2
        if reward != -1:  # Q
            status = 0
    if epsilon > 0.1:  # R
        epsilon -= (1 / epochs)

