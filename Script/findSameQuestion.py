import json
from collections import Counter

# 读取文件
file_path = 'question.txt'

# 加载JSON数据
with open(file_path, 'r', encoding='utf-8') as file:
    questions = json.load(file)

# 创建一个列表存储题目文本
question_texts = [q['question'] for q in questions]

# 使用Counter找到重复题目
duplicates = [item for item, count in Counter(question_texts).items() if count > 1]

# 打印重复题目
print("重复的题目：")
for dup in duplicates:
    print(dup)
