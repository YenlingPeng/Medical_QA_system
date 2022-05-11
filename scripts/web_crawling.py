# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm.notebook import tqdm, trange


def main():

  commonhealth()
  nowhealth()
  udn()
  jah()
  ca2()
  cmh()
  kenkon()

def commonhealth():
  categories = []
  data = []
  
  url_1 = "https://kb.commonhealth.com.tw/library"
  r = requests.get(url_1)
  soup = BeautifulSoup(r.content)

  # 百科分類  
  for c in soup.find("div", id="body-organs").find_all("a"):
    label = c.p.string
    link = c.attrs["href"]
    categories.append((label, link))


  # 婦女常見疾病
  url_2 = 'https://kb.commonhealth.com.tw/library/tag/'
  r = requests.get(url_2)
  soup = BeautifulSoup(r.content)
  soup.find("div", class_="topics-box")

  for c1 in soup.find("div", class_="topics-box").find_all("a"):
    link = c1.attrs["href"]
    label = c1.h3.string
    categories.append((label, link))

    # The outer loop is to process each 'category'
    for c1 in categories:
      r = requests.get(c1[1])
      soup = BeautifulSoup(r.content)
      # The inner loop is to process each 'disease'
      for c2 in soup.find_all("div", class_="result-item"):
        label = c2.h3.string
        if label is not None:
          link = c2.a.attrs["href"]
          data.append(
              dict(
                  category = c1[0],
                  disease = label,
                  url = link
              )
          )
  # Create csv file
  df = pd.DataFrame(data, 
                    columns =['category', 'disease', 'url'])

  # Set index on a Dataframe
  df.set_index("category", inplace = True)

  # Normalize label names
  df.rename(index={'心臟':'心臟科', 
                  '肝臟':'肝膽腸胃科', 
                  '肺臟':'肝膽腸胃科',
                  '腸胃':'肝膽腸胃科',
                  '腎臟':'腎臟內科',
                  '婦科':'婦產科',
                  '骨、關節':'骨科',
                  '腦神經':'神經內科', 
                  '牙齒、口腔':'牙科', 
                  '眼睛':'眼科',
                  '耳鼻喉':'耳鼻喉科',
                  '皮膚':'皮膚科',
                  '身心':'精神科',
                  '泌尿道':'泌尿科',
                  '症狀百科':'家庭醫學科',
                  '飲食百科':'營養科',
                  '運動百科':'復健科',
                  '營養百科':'營養科',
                  '乳房相關問題':'乳房特診',
                  '子宮相關問題':'婦產科',
                  '卵巢相關問題':'婦產科',
                  '羞羞病（性病）':'感染科',
                  }, inplace=True)


def nowhealth():
  categories = []
  data = []
  
  url = "https://gooddoctorweb.com"
  r = requests.get(url)
  soup = BeautifulSoup(r.content)

  for c in soup.find("div", id="navbarSupportedContent").find_all('a'):
    if c.string != None:  # None的問題
      categories.append((c.string, "https://gooddoctorweb.com"+c.attrs["href"]))

  for c1 in tqdm(categories):
    r = requests.get(c1[1])
    soup = BeautifulSoup(r.content)
  
    for c2 in soup.find_all("div", class_="col-12 col-lg-7"):
      if c2.find("h1"):       
        link = url + c2.a.attrs["href"]
        data.append(
            dict(
                category=c1[0],
                disease=c2.h1.string, 
                url = link
                )
            )
  # Create csv file
  df = pd.DataFrame(data, 
                    columns =['category', 'disease', 'url'])

  # Set index on a Dataframe
  df.set_index("category", inplace = True)

  # Remove unused categories
  df = df.loc[['癌症專題', '心血管專題', '耳鼻喉專題', '腸胃道專題', '肝膽胰專題', '泌尿道專題', '慢性病專題', '小細胞肺癌專題', 
              '飲食養生', '運動養生', '姿勢養生', '中醫養生', '瘦身飲食', '瘦身運動', '防癌生活', '健康生活']]



  # Normalize label names
  df.rename(index={'癌症專題':'血液腫瘤科',
                  '心血管專題':'心臟科',
                  '耳鼻喉專題':'耳鼻喉科', 
                  '腸胃道專題':'肝膽腸胃科',
                  '肝膽胰專題':'肝膽腸胃科',
                  '泌尿道專題':'泌尿科', 
                  '慢性病專題':'家庭醫學科',
                  '小細胞肺癌專題':'血液腫瘤科',
                  '飲食養生': '營養科',
                  '運動養生':'復健科',
                  '姿勢養生':'復健科',
                  '中醫養生':'中醫科',
                  '瘦身飲食':'營養科',
                  '瘦身運動':'營養科',
                  '防癌生活':'家庭醫學科',
                  '健康生活':'家庭醫學科'
                  }, inplace=True)


def udn():
  categories = []
  data = []
  
  url = "https://health.udn.com/"
  r = requests.get(url) 
  soup = BeautifulSoup(r.content)

  for c1 in soup.find("div", id="diagnosis_body").ul.children:
   categories = c1.span.contents[0]
   for c2 in c1.ul.children:
      label = c2.a.string
      link = url + c2.a.attrs["href"].lstrip("/")
      data.append(
          dict(
              category=categories,
              disease=label,
              url=link,
          )
      )

  # Create csv file
  df = pd.DataFrame(data, 
                  columns =['category', 'disease', 'url'])

  # Set index on a Dataframe
  df.set_index("category", inplace = True)

  # Remove unused categories
  df.drop(index=['其他'], inplace = True)

  # Normalize label names
  df.rename(index={'婦產兒科':'婦產科', 
                  '血液腫瘤':'血液腫瘤科',
                  '皮膚':'皮膚科', 
                  '胃腸肝膽':'肝膽腸胃科',
                  '泌尿腎臟':'腎臟內科', 
                  '心血管':'心臟科', 
                  '骨科・復建':'骨科',
                  '神經':'神經內科',
                  '耳鼻喉':'耳鼻喉科',
                  '過敏・免疫':'免疫風濕科',
                  '身心精神':'精神科',
                  '呼吸胸腔':'胸腔內科',
                  '新陳代謝・內分泌':'新陳代謝科'
                  }, inplace=True)


def jah():
  categories_1 = []
  categories_2 = []
  data = []

  url = 'https://www.jah.org.tw/form/indexS.asp?m=3&m1=8&m2=362&gp=361'
  r = requests.get(url)
  soup = BeautifulSoup(r.content)
  root_url_1 = 'https://www.jah.org.tw'

  for c in soup.find("div", id="collapse0").find_all('a'):
    label_1 = c.string.lstrip("▪")
    url_1 = root_url_1 + c.attrs["href"].lstrip(".")
    categories_1.append((label_1, url_1))

  root_url2 = 'https://www.jah.org.tw/form/'

  for c1 in categories_1:
    r = requests.get(c1[1])
    soup = BeautifulSoup(r.content)
    for c2 in soup.find("select", id="types001").find_all("option"):
        label_2 = c2.text
        print(label_2)
        url_2 = root_url2 + c2['value']
        print(url_2)
        if label_2 != '全部分類':
          categories_2.append((label_2, url_2))
        
        for c3 in tqdm(categories_2):
          r = requests.get(c3[1])
          soup = BeautifulSoup(r.content)
          for c4 in soup.find_all("div", class_="date form_list"):
            label_3 = c4.a.string
            print(label_3)
            url_3 = root_url2 + c4.a.attrs["href"]
            print(url_3)
            data.append(
                dict(
                    category=c3[0],
                    disease=label_3,
                    url=url_3,
                )
            )


    # Create csv file
    df = pd.DataFrame(data,
                      columns =['category', 'disease', 'url'])

    # Set index on a Dataframe
    df.set_index("category", inplace = True)

    # Remove unused categories
    df.drop(index=['麻醉科', '急診醫學部', '檢驗科', '藥劑部', '居家護理', '社區醫學部', '健康檢查中心', '核子醫學科', '安寧緩和醫療科', '護理部', '疼痛科'], inplace = True)

    # Normalize label names
    df.rename(index={'心臟內科':'心臟科', 
                    '消化內科':'肝膽腸胃科', 
                    '內分泌新陳代謝科':'新陳代謝科',
                    '風濕免疫科':'免疫風濕科',
                    '腫瘤治療科':'放射腫瘤科',
                    '身心內科':'精神科',
                    '血液科暨腫瘤內科':'血液腫瘤科',
                    '一般外科':'外科',
                    '人工關節中心':'骨科',
                    '大腸直腸外科':'肝膽腸胃科',
                    '心臟血管外科':'心臟科',
                    '整形美容外科':'整形外科',
                    '脊椎外科':'復健科',
                    '乳房中心特別門診':'乳房特診',
                    '乳房醫學中心':'乳房特診',
                    '小兒科':'兒科',
                    '中醫':'中醫科',
                    '肥胖綜合門診':'新陳代謝科',
                    '營養治療科':'營養科',
                    '放射線診療科':'放射腫瘤科'
                    }, inplace=True)


def ca2():
  categories = []
  data = []

  url = "https://www.ca2-health.com/FrontEnd/SearchSymptom"
  r = requests.get(url)
  soup = BeautifulSoup(r.content)
  root_url = "https://www.ca2-health.com"

  for c1 in soup.find('div', class_='aside-web-menu').find_all('a'):
    if c1.p.string is not None:
      label = c1.p.string
      link = root_url + c1.attrs["href"]
      categories.append((label, link))

  for c1 in tqdm(categories):
    r = requests.get(c1[1])
    soup = BeautifulSoup(r.content)

    for c2 in soup.find("ul", class_="nav navbar-nav").find_all("a"):
      label = c2.string
      if label is not None:     
        link = root_url  + c2.attrs["href"]

        data.append(
            dict(
                category = c1[0],
                disease = c2.string,
                url = link
            )
        )

  # Create csv file
  df = pd.DataFrame(data, 
                    columns =['category', 'disease', 'url'])

  # Set index on a Dataframe
  df.set_index("category", inplace = True)

  # Remove unused categories
  df.drop(index=['優質老化', '兩性關係', '健康減重', '醫學美容', 'DryLab醫療新知'], inplace = True)

  # Normalize label names
  df.rename(index={'中醫養生':'中醫科', 
                  '婦女健康':'婦產科', 
                  '兒童健康':'兒科',
                  '癌症腫瘤':'放射腫瘤科',
                  '風濕免疫':'免疫風濕科',
                  '心臟血管':'心臟科',
                  '新陳代謝':'新陳代謝科',
                  '優生孕產':'婦產科',
                  '腦中風':'神經外科',
                  '整形重建':'整形外科',
                  '眼睛保健':'眼科',
                  '牙齒口腔':'牙科',
                  '腎利人生':'腎臟內科'
                  }, inplace=True)

  # Data clean
  df = df.astype(str)
  y = df[df['disease'].str.contains('影音|首頁|其他|相關|團隊|服務|資源')|df['url'].str.contains('java')]

  test1 = list(y.url)
  test2 = list(df.url)

  for java_url in test1:
    test2.remove(java_url)

  df_refined = df[df.url.isin(test2)]


def cmh():
  categories = []
  data = []

  url = "http://www.chimei.org.tw/main/cmh_department/59012/info/"
  r = requests.get(url)
  soup = BeautifulSoup(r.content)

  # The outer loop is to process each 'category'
  for c in soup.find("div", id="main-wrapper").find_all('a'):
      if c.string != None:
        categories.append((c.string, url + c.attrs["href"]))
 
  
  for c1 in tqdm(categories):
    r = requests.get(c1[1])
    soup = BeautifulSoup(r.content)
    
    # The inner loop is to process each 'disease'
    for c2 in soup.find("div", class_="card-body").find_all("a"):
      if c2.string is not None: # remove "None"
        link = url + c1[1].split("/")[-2] + "/" + c2.attrs["href"]

        data.append(
            dict(
                category = c1[0],
                disease = c2.string,
                url = link
            )
        )

  # Create csv file
  df = pd.DataFrame(data, 
                  columns =['category', 'disease', 'url'])

  # Set index on a Dataframe
  df.set_index("category", inplace = True)
  
  # Remove unused categories
  df.drop(index=['檢查室', '一般及消化系外科', '傷口照護中心', '病理中心', '高壓氧科', '麻醉部', '加護醫學部', 
                '癌症中心', '燙傷中心', '藥劑部', '護理部', '緩和病房', '居家護理', '醫療事務室', 
                '人體試驗委員會','健康管理中心', '印尼文', '英文', '越南文', '簡體中文', '核子醫學科', '急診醫學部'], inplace = True)

  # Normalize label names
  df.rename(index={'心臟血管內科':'心臟科', 
                  '腎臟科':'腎臟內科',
                  '胃腸肝膽科':'肝膽腸胃科', 
                  '內分泌新陳代謝科':'新陳代謝科',
                  '風濕免疫科':'免疫風濕科', 
                  '泌尿外科':'泌尿科', 
                  '骨科部':'骨科',
                  '心臟血管外科':'心臟科',
                  '泌尿外科':'泌尿科',
                  '兒科部':'兒科',
                  '婦產部':'婦產科',
                  '復健部(科)':'復健科',
                  '放射腫瘤部(科)':'放射腫瘤科',
                  '中醫部':'中醫科',
                  '牙醫部':'牙科',
                  '眼科(部)':'眼科',
                  '耳鼻喉科(部)':'耳鼻喉科',
                  '家庭醫學部(科)':'家庭醫學科',
                  '精神醫學部(科)':'精神科',
                  '放射診斷科':'放射腫瘤科'
                  }, inplace=True)


def kenkon():
  data={}
  data["category"]=[]
  data["disease"]=[]
  data["url"]=[]

  url = "http://www.kenkon.com.tw/health.php"
  r = requests.get(url)
  soup = BeautifulSoup(r.content)
  root="http://www.kenkon.com.tw/"

  for loop in range(1, 25):
    rq = requests.get(root+"/health.php?cid=" + str(loop))
    s = BeautifulSoup(rq.content)
    d=[]
    d.append("/health.php?cid=" + str(loop))
    for g in s.find_all("div", id="pageNum"):
      for z in g.find_all("a"):
        if z.attrs["href"] not in d and z.attrs["href"] != '':
          d.append(z.attrs["href"])

    for f in d:
      rq = requests.get(root+f)
      s = BeautifulSoup(rq.content)
      for i in s.find_all("div", class_="growthLink"):
        data["category"].append(s.find("div", class_="growthCate").string)
        data["disease"].append(i.a.attrs["title"])
        data["url"].append(root+i.a.attrs["href"])


if __name__ == "__main__":
  """ This is executed when run from the command line """
  main()
