# This python file aims to train LSTM model and save it
import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch import optim


class LSTMDataset(Dataset):

    def __init__(self, sentences):
        self.sentences = sentences
        self.n = len(self.sentences)

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        x, y = self.sentences[idx]
        x = torch.Tensor(x)
        y = torch.Tensor([y])
        return x, y


def main():

    vectorized_data = np.load('LSTM_test_vectorized_data_0415.npy', allow_pickle=True).tolist()

    new_train = vectorized_data[0:19000]
    new_train.extend(vectorized_data[20000:39000])
    new_train.extend(vectorized_data[40000:59000])
    new_train.extend(vectorized_data[60000:71073])
    new_val = vectorized_data[19000:20000]
    new_val.extend(vectorized_data[39000:40000])
    new_val.extend(vectorized_data[59000:60000])
    new_val.extend(vectorized_data[71073:])

    n_epoch = 100
    train_ds = LSTMDataset(new_train)
    val_ds = LSTMDataset(new_val)
    model = nn.LSTM(input_size=100, hidden_size=1000, proj_size=26, batch_first=True, bidirectional=False)
    loss_fn = nn.CrossEntropyLoss()
    lr = 0.0005
    optimizer = optim.RMSprop(model.parameters(), lr=lr)

    device = torch.device('cuda')
    model.to(device)

    for i in range(n_epoch):
        # Training
        model.train()
        print(f'{i} Trains')
        train_dl = DataLoader(train_ds, batch_size=1, shuffle=True)

        for (x, y) in train_dl:
            optimizer.zero_grad()
            if x.size(0) < 1:
                continue
            x = x.to(device)
            y = y.to(device)
            outputs, (h, c) = model(x)
            loss = loss_fn(outputs[:, -1, :].view(1, -1).float(), y.view(-1).long())
            loss.backward()
            optimizer.step()

        # Validating
        model.eval()
        val_dl = DataLoader(val_ds, batch_size=1, shuffle=False)
        with torch.no_grad():
            for (x, y) in val_dl:
                x = x.to(device)
                y = y.to(device)
                outputs, (h, c) = model(x)
        torch.save(model.state_dict(), 'New_LSTM_model_0416_2.pt')


if __name__ == "__main__":
    main()
