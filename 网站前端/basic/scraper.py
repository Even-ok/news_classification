## 用Article爬取单条新闻
import newspaper
import re
import pandas as pd         # 导入pandas库
import copy as cp
from time import sleep

global i_process
global j_process

def get_iprocess():
    global i_process
    global j_process
    print(i_process)
    return i_process, j_process

def get_news(news_source,memorize_type):
    global i_process
    global j_process
    i_process=0#初始值设为0
    j_process=0
    url=news_source
    paper_source = newspaper.build(url, language='zh', memoize_articles=memorize_type)  # 构建新闻源
    articles_select = []
    for article in paper_source.articles:
        if len(re.findall("https://www.163.com/", str(article.url))) > 0:
            print(article.url)
            articles_select.append(article)
    return articles_select

def parse_news(articles):
    global i_process
    global j_process
    news_title = []
    news_text = []
    news_type = []
    news = articles
    j_process=str(len(news))
    print("总共需要爬取的文件数目为：" + str(len(news)))
    for i in range(10):  # 以新闻链接的长度为循环次数  len(news)
        i_process=i
        paper = news[i]
        try:
            print("当前爬取进度：" + str(i) + "/" + str(len(news)))
            paper.download()
            paper.parse()
            news_title.append(paper.title)  # 将新闻题目以列表形式逐一储存
            news_text.append(paper.text)  # 将新闻正文以列表形式逐一储存
            news_type.append(paper.url)
        except:
            print("第"+str(i)+"个爬取失败")
            news_title.append('NULL')  # 如果无法访问，以NULL替代
            news_text.append('NULL')
            news_type.append('NULL')
            continue
    return news_title,news_text,news_type

def trans_class(news_type):
    new_type = cp.deepcopy(news_type)  # 先进行一次拷贝，避免之后出问题
    for i in range(len(news_type)):
        new_type[i] = str(re.findall("https://www.163.com/(.*?)/article", new_type[i]))
        if new_type[i] == "['news']":
            new_type[i] = " else"
        elif new_type[i] == "['finance']" or new_type[i] == "['economy']" or new_type[i] == "['money']":
            new_type[i] = "财经"
        elif new_type[i] == "['house']" or new_type[i] == "['home']":  # 这个没有
            new_type[i] = "房产"
        elif new_type[i] == "['car']" or new_type[i] == "['auto']":
            new_type[i] = "汽车"
        elif new_type[i] == "['edu']":
            new_type[i] = "教育"
        elif new_type[i] == "['theory']" or new_type[i] == "['tech']" or new_type[i] == "['it']" or new_type[
            i] == "['digi']" or new_type[i] == "['mobile']":
            new_type[i] = "科技"
        elif new_type[i] == "['sports']":
            new_type[i] = "体育"
        elif new_type[i] == "['war']":
            new_type[i] = "军事"
        elif new_type[i] == "['ent']":
            new_type[i] = "娱乐"
        elif new_type[i] == "['travel']":
            new_type[i] = "旅游"
        else:
            new_type[i] = new_type[i]
    return new_type

def out_file(news_title,news_text,news_type,file):
    file="news"
    paper_source_data = pd.DataFrame({'title': news_title, 'text': news_text, 'class': news_type})
    try:
        # paper_source_data.to_excel("static\\Downloads\\"+file+".xlsx")
        # paper_source_data.to_csv("static\\Downloads\\"+file+".csv")
        print("成功输出到文件到"+file)
        return "爬取成功"
    except:
        print("输出到文件失败")
        return "爬取失败"

# if __name__ == "__main__":
def scrap():
    news_source="https://www.163.com/"
    print("开始提取网站为" + news_source + "中的文章")
    articles=get_news(news_source, False)
    print("提取文章类，共"+str(len(articles))+"个")
    title,text,type=parse_news(articles)
    print("有效信息分类为title,text,type三类")
    newtype=trans_class(type)
    print("将type按照分配要求进行分类结束")
    return out_file(title,text,newtype,"新闻文本分类_网易_筛版")

def scrap_test():
    sleep(5)
    return "爬取成功"