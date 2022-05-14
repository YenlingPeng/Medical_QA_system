# This python file aims to visualize the vocabulary learned from wikipedia and the confusion matrix of validation data in LSTM training

import numpy as np
from gensim.models import word2vec
from sklearn.decomposition import PCA
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import confusion_matrix
import seaborn as sns


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


class PREPARE(object):
  def __init__(self):
    self.model_wv = word2vec.Word2Vec.load('wiki_word2vec2.model')
    self.model_lstm = nn.LSTM(input_size=100, hidden_size=1000, proj_size=26, batch_first=True)
    self.model_lstm.load_state_dict(torch.load('New_LSTM_model_0416_2.pt'))
    self.department_list = ['血液腫瘤科', '胸腔內科', '心臟科', '肝膽腸胃科', '神經內科', '感染科', '腎臟內科', '新陳代謝科', '免疫風濕科',
                   '乳房特診', '神經外科', '泌尿科', '骨科', '皮膚科', '眼科', '耳鼻喉科', '婦產科', '復健科', '家庭醫學科',
                   '放射腫瘤科', '兒科', '中醫科', '精神科', '牙科', '營養科', '整形外科']
    self.id2cat = {i: self.department_list[i] for i in range(len(self.department_list))}
    self.vectorized_data = np.load('LSTM_test_vectorized_data_0415.npy', allow_pickle=True).tolist()
    self.val_data = self.vectorized_data[0::100]
    self.val_ds = LSTMDataset(self.val_data)
    self.val_dl = DataLoader(self.val_ds, batch_size=1, shuffle=False)


def main():
  pre = PREPARE()
  # Visualizing with PCA & matplotlib
  display_pca_scatterplot(pre.model_wv, input("請輸入主要想查詢的詞: "), topn=20)

  # Visualizing with confusion matrix
  fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
  mpl.rc('font', family='Taipei Sans TC Beta')
  visualize_con(pre.model_lstm, pre.val_ds, pre.val_dl, pre.id2cat)


def display_pca_scatterplot(model_wv, target_word, topn=20):
  w = model_wv.wv.most_similar(f'{target_word}', topn=topn)
  words = []
  words.append(f'{target_word}')
  for i in range(len(w)):
    words.append(w[i][0])
  word_vectors = np.array([model_wv[word] for word in words])
  two_dim = PCA().fit_transform(word_vectors)[:, :2]

  plt.figure(figsize=(16, 16))
  plt.scatter(two_dim[:, 0], two_dim[:, 1], c='#88c999', s=600)
  plt.xlabel("PCA1", fontsize=20)
  plt.ylabel("PCA2", fontsize=20)
  plt.xticks(fontsize=18)
  plt.yticks(fontsize=18)

  for word, (x, y) in zip(words, two_dim):
    plt.text(x + 0.05, y + 0.05, word, fontproperties=mpl.font_manager.FontProperties(fname='TaipeiSansTCBeta-Regular.ttf'), fontsize=30)



def visualize_con(model_lstm, val_ds, val_dl, id2cat):
  device = torch.device("cuda")
  model_lstm.to(device)
  model_lstm.eval()
  predictions = []
  with torch.no_grad():
    for (x, y) in val_dl:
      x = x.to(device)
      y = y.to(device)
      outputs, (h, c) = model_lstm(x)
      predictions.append(outputs)
  predictions_ = torch.cat([p[:, -1, :] for p in predictions], dim=0)
  preds = torch.argmax(predictions_, dim=1).cpu().numpy()
  labels = np.array([int(xy[1]) for xy in val_ds])
  cf_matrix = confusion_matrix(labels, preds)

  fig = plt.figure(figsize=(18, 18))
  ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')
  ax.set_xlabel('預測科別', fontsize=25)
  ax.set_ylabel('輸入科別', fontsize=25)
  plt.xticks(np.arange(26) + 1, [id2cat[i] for i in range(26)], fontsize=20)
  plt.yticks(np.arange(26) +0.5, [id2cat[i] for i in range(26)], fontsize=20, rotation = 360)

  fig.autofmt_xdate(rotation = 45) # 旋轉 Xticks標籤文字
  plt.show()


if __name__ == "__main__":
  main()
