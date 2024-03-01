from dict_sentiment import single_sentiment_score
import pandas as pd
import re
from tqdm.auto import tqdm

# 读取数据集
data = pd.read_csv("data_1.csv")  # 使用了正确的路径

# 读取属性词典，假设属性词典的CSV格式是每个属性占一列，属性名为列名，词汇按行排列
attr_dict = pd.read_csv("属性词典.csv")  # 使用了正确的路径

# 为数据集添加22列，对应每个属性的正向和负向情感得分
for attr in attr_dict.columns:
    data[attr + "_pos"] = 0
    data[attr + "_neg"] = 0

# 处理每个属性词对应的评论情感分析
for attr in attr_dict.columns:
    words = attr_dict[attr].dropna().tolist()  # 保证属性词非空
    words = [word.strip() for word in words if isinstance(word, str)]  # 去除空格，确保为字符串
    for word in words:
        # 使用tqdm显示进度条
        for i in tqdm(range(len(data)), desc=f"Processing {attr}: {word}"):
            comment = data.at[i, '评论']
            if pd.isnull(comment):
                continue  # 如果评论为空，则跳过
            sentences = re.split(r'[。！？]', comment)
            for sentence in sentences:
                if word in sentence:
                    sentiment = single_sentiment_score(sentence)
                    adjusted_sentiment_pos = (sentiment/10) if sentiment >= 0 else 0
                    adjusted_sentiment_neg = (sentiment/10) if sentiment < 0 else 0
                    data.at[i, attr + "_pos"] += adjusted_sentiment_pos
                    data.at[i, attr + "_neg"] += abs(adjusted_sentiment_neg)
                    break  # 一旦找到匹配的词语，就不再继续搜索当前评论的其它句子

# 输出处理后的数据查看
data.to_csv("data_2.csv", encoding="utf-8-sig")
