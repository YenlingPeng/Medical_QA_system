from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from gensim.models import word2vec
import numpy as np
import pandas as pd
import plotly.express as px
from tqdm import tqdm, trange
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch import optim
import torch.nn.functional as F


"""## BOT API Class """

class LSTMDataset(Dataset):

    def __init__(self, sentences):  # __init__
        self.sentences = sentences
        self.n = len(self.sentences)

    def __len__(self):  # 要有一個len的method
        return self.n

    def __getitem__(self, idx):  # 要有一個getitem的method(不知道why)
        x, y = self.sentences[idx]
        x = torch.Tensor(x)
        y = torch.Tensor([y])
        return x, y  # LSTMDataset 會丟出 x, y 的tuple

class BOT(object):
  def __init__(self):
    
    self.ws = WS("./data", disable_cuda=False)
    self.wv_model = word2vec.Word2Vec.load('wiki_word2vec2.model')
    self.wiki_dict = [w for w in self.wv_model.wv.index_to_key]    
    
    self.lstm_model = nn.LSTM(input_size=100, hidden_size=1000, proj_size=26, batch_first=True)
    self.lstm_model.load_state_dict(torch.load('New_LSTM_model_0416_2.pt', map_location=torch.device('cpu')))
    self.department_list = ['血液腫瘤科', '胸腔內科', '心臟科', '肝膽腸胃科', '神經內科', '感染科', '腎臟內科', '新陳代謝科', '免疫風濕科', '乳房特診', '神經外科', '泌尿科', '骨科', '皮膚科', '眼科', '耳鼻喉科', '婦產科', '復健科', '家庭醫學科',
                   '放射腫瘤科', '兒科', '中醫科', '精神科', '牙科', '營養科', '整形外科']
    self.embeddings = np.load('embeddings_all_0415_concat.npy')
    self.df_all = pd.read_csv('all_web.csv', index_col=0)

  
  def run(self, msg):
    tokens = self.ws([msg])
    vectors = []

    for t in tokens[0]:
      if t in self.wiki_dict:
        vec = self.wv_model.wv.get_vector(t)
        vectors.append(vec.reshape(1, -1))
    vectors = np.concatenate(vectors, axis = 0)
    categories = self.suggested_categories(vectors)
    articles = self.suggested_articles(vectors)   # top 200 articles
           
    count = 0
    article_list = []
    for i in range(len(articles)):
      if articles.iloc[i][0] in (categories[_][0] for _ in range(len(categories))): # 文章的科別
        article_list.append([articles.iloc[i][1], articles.iloc[i][2]])
        count = count + 1
      if count == 5:
        break

    return categories, article_list # 科別,文章標題,url

  # Supervised
  def suggested_categories(self, vectors):
    vector_list = []
    vector_list.append((np.array(vectors), 0,))
    val_ds = LSTMDataset(vector_list)
    val_dl = DataLoader(val_ds, batch_size=1, shuffle=False)

    device = torch.device('cpu')
    self.lstm_model.to(device)
    self.lstm_model.eval()

    with torch.no_grad():
      for (x, y) in val_dl:
        x = x.to(device)
        y = y.to(device)
        outputs, (h, c) = self.lstm_model(x)
    scores = outputs[0, -1, : ]

    prob_list = [] #儲存各科的建議機率
    prob = F.softmax(scores, dim=0) # 利用softmax取得各科的機率
    for i in range(len(self.department_list)):
        prob_list.append((i, prob[i].item()))
    prob_rank = sorted(prob_list, key = lambda s: s[1], reverse=-1) #把prob_list依照機率的高->低排序成新的list

    top_category = []
    for i in range(5):
        top_category.append((self.department_list[prob_rank[i][0]] , round(prob_rank[i][1]*100, 2)))
    
    return top_category # lict of top 5 chinese categories

  # Un-supervised
  def suggested_articles(self, vectors):
    q_vector = np.mean(vectors, axis=0, keepdims=True)
    q_products = self.embeddings @ q_vector.T
    idxs = np.argsort(q_products, axis=0)
    idxs = idxs[::-1, 0]

    return self.df_all.iloc[idxs[:200]]


 
# 給API BOT用
bot = BOT()

# 數字label去找到科別 >> LSTM會去回答要看哪個科別 >> supervise training
id2cat = {i: bot.department_list[i] for i in range(len(bot.department_list))}

# 科別去找label >> 用於LSTM training >> supervise training
cat2id = {bot.department_list[i]: i for i in range(len(bot.department_list))}

#    question = input('您的問題:')
def qa_chatbot_api(msg):
    ans_list = []
    ans_list.append(f'您的問題: {msg}')

    answer = bot.run(msg)  

    if answer[0][0][1] >= 90:

      ans_list.append(f'建議您可以去看 {answer[0][0][0]}')
      
    elif answer[0][0][1] > 15:

      ans_list.append("建議您可以看以下科別:")
      for j in range(3):
        if answer[0][j][1] > 10:

          ans_list.append(f"推薦度: {answer[0][j][0]} {answer[0][j][1]}%")
        
    else:

      ans_list.append("我不清楚你的意思，您可以再說一次")

    if answer[0][0][1] > 15: 
        ans_list.append("請參考以下醫療資訊的文章")

        for k in range(5):
            if len(answer[1]) > k:
                ans_list.append(f'{answer[1][k][0]} {answer[1][k][1]}')

    return(ans_list)
