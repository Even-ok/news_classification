from time import sleep
import os
import pandas as pd
import re
import jieba
from itertools import chain
from collections import Counter
import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer  

def predict(title,text,model):
    type=[]
    for i in range(len(text)):
        res=sentencePredict(title[i],text[i],model)
        res = res[0]
        type.append(res)
    return type

def trans_number(type):
    classes = ['财经', '房产', '教育', '科技', '军事', '汽车', '体育', '游戏', '娱乐', '互联网', '政治']
    res=[]
    for i in range(len(type)):
        index=type[i]
        index=int(index)
        print(index)
        res.append(classes[index])
        print(res[i])
    return res

def get_news_from_file(type):
    if(type==1):
        file_path = os.path.join('static/Uploads', 'news.xlsx')
        df = pd.read_excel(file_path, usecols='A:B')  # sheet_name不指定时默认返回全表数
    else:
        file_path = os.path.join('static/Uploads', 'news.csv')
        df = pd.read_csv(file_path, usecols='A:B')  # sheet_name不指定时默认返回全表数
    title=df.iloc[:,0]
    text = df.iloc[:, 1]
    return title,text

def store_file(title,text,type):
    file = "news_predicted"
    paper_source_data = pd.DataFrame({'title': title, 'text': text, 'class': type})
    try:
        paper_source_data.to_excel("static\\Uploads\\" + file + ".xlsx")
        paper_source_data.to_csv("static\\Uploads\\" + file + ".csv")
        print("成功输出到文件到" + file)
        return "输出文件成功"
    except:
        print("输出到文件失败")
        return "输出文件成功"

def clear(text):
    re_obj = re.compile(
        r"[!\"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~—！，。？、￥…（）：【】《》‘’“”\s]+")
    re_obj2 = re.compile(
        r'[a-zA-Z0-9’!"#$%&\'()*+,-.<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+')
    res = re_obj.sub('', text)
    res = re.sub('[^\u4e00-\u9fa5]+', '', text)
    return res

def get_stopword():
    s = set()
    with open('all_stopwords.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            s.add(line.strip())
    return s


def remove_stopword(words):
    stopword = get_stopword()
    return [word for word in words if word not in stopword]


def sentencePredict(title, sentence, model="MLP"):
    classes = ['财经', '房产', '教育', '科技', '军事', '汽车', '体育', '游戏', '娱乐', '互联网', '政治']
    # 输入为一段话

    content = str(sentence).strip().replace(" ", '')
    content = clear(content)
    content = jieba.cut(content)
    content = remove_stopword(content)

    # li_2d = content
    # li_1d = list(chain.from_iterable(li_2d))

    content = " ".join(content)

    f1 = open('model/vec_bag.pkl', 'rb')
    vec = joblib.load(f1)
    f2 = open('model/selector.pkl', 'rb')
    selector = joblib.load(f2)
    f1.close()
    f2.close()
    # print(content)
    #     content_1.append('小朋友')
    #     content.append('小朋友')

    content_1 = [content]

    # print(content_1)
    news_tran = vec.transform(content_1)
    news_tran = selector.transform(news_tran)

    if model == 'softmax':
        model_softmax_regression = joblib.load('./model/softmax_regression.pkl')
        y_predict = model_softmax_regression.predict(news_tran)

    elif model == 'KNN':
        KNN = joblib.load('./model/KNN_5.pkl')
        y_predict = KNN.predict(news_tran)

    elif model == 'dicisionTree':
        dt = joblib.load('./model/dicisionTree.pkl')
        y_predict = dt.predict(news_tran)

    elif model == 'MLP':
        mlp = joblib.load('./model/MLPClassifier.pkl')
        y_predict = mlp.predict(news_tran)

    # elif model == 'ComplementNB':
    #     nb = joblib.load('./model/NaiveBayes.pkl')
    #     y_predict = nb.predict(news_tran)

    return y_predict