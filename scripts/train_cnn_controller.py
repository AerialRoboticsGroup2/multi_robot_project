import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

# ======================================
# Dataset
# ======================================

class RobotDataset(Dataset):
    def __init__(self):

        self.X = np.load('training_inputs.npy')
        self.Y = np.load('training_outputs.npy')

        self.X = torch.tensor(self.X, dtype=torch.float32)
        self.Y = torch.tensor(self.Y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]

# ======================================
# CNN Model
# ======================================

class CNNController(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv1d(1, 16, kernel_size=5)
        self.conv2 = nn.Conv1d(16, 32, kernel_size=5)

        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(32 * 24, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 2)

    def forward(self, x):

        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))

        x = x.view(x.size(0), -1)

        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))

        return self.fc3(x)

# ======================================
# Training
# ======================================


def train():

    dataset = RobotDataset()
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = CNNController()

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 20

    for epoch in range(epochs):

        total_loss = 0

        for X, Y in loader:

            optimizer.zero_grad()

            pred = model(X)

            loss = criterion(pred, Y)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f'Epoch {epoch}: Loss = {total_loss}')

    torch.save(model.state_dict(), 'cnn_controller.pth')

    print('Model saved.')

if __name__ == '__main__':
    train()
