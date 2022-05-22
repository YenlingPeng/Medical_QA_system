一問醫答 AI in Medical QA System
==
本專案旨在構建第一個中文醫療QA系統聊天機器人。透過蒐集繁體中文的相關衛教網站作為資料庫，通過聊天機器人，用戶可以輸入他們對症狀的主訴，機器人會推薦相關的看診科別與推薦參考的文章。
## web crawling 
本專案蒐集了來自7個台灣衛教網站的衛教文章作為我們資料庫，透過透過觀察每個衛教網站的原始碼，將衛教文章的網站與名稱給蒐集起來。
7個衛教網站分別來自[UDN元氣網](https://health.udn.com/health/index)、[康健知識庫](https://kb.commonhealth.com.tw/)、[奇美衛教資訊網](http://www.chimei.org.tw/main/cmh_department/59012/info/)、[kenkon健康網](http://www.kenkon.com.tw/)、[仁愛醫療材團法人全球資訊網](https://www.jah.org.tw/)、[今健康](https://gooddoctorweb.com/)、[中亞健康網](https://www.ca2-health.com/)，最後收集了4861篇文章。

**Project framework**
![Framework](https://user-images.githubusercontent.com/103913257/168462607-2bb4bf97-209b-4877-8946-222dedd06679.jpg)

## Data pre-processing
在4861篇文章，我們使用 [CkipTagger](https://github.com/ckiplab/ckiptagger) 進行繁體中文的斷詞，再使用
[stop word list](https://github.com/sb123456789sb/Machine-Learning-28/blob/master/data/%E5%81%9C%E7%94%A8%E8%A9%9E-%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87.txt) 除去停用詞，如你、我、他以及標點符號等。最後再以 [Word2Vec](https://code.google.com/archive/p/word2vec/) 去計算字詞之間的相似性。

## Unsupervised
透過使用 Embedding的方式，去計算各文章經過處理後的文字所對應的向量，經過 Cosine Similarity，去計算最適合的衛教文章。

## Supervised
透過對112條自然語言敘述的主訴，去標籤其對應的科別。接著使用LSTM的模型進行訓練，當使用者輸入主訴後，可以計算相關的看診科別。

## API 
將後端的資料處理、LSTM的模型、推薦相關的看診科別與參考文章的code整理成class的模式，掛到API上，使其可以跟chat bot做結合，整理成前端的模式。

## Visualize
- 使用PCA降低embedding的維度，並且使用2D的PCA已呈現文字間的相關性。

**PCA**

![PCA](https://github.com/sc201groupc/Medical_QA_system/blob/main/figures/pca_example_heart.png)


- 使用confusion matrix去看多分類型的預測結果，Y軸是我們標籤的科別，X軸是我們預測的科別。


**Confusion matrixs**
![Confusion matrixs](https://github.com/sc201groupc/Medical_QA_system/blob/main/figures/confusion_matrix.png)


<!---
sc201groupc/sc201groupc is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->





