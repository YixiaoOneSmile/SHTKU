import os
import re
import json

# 定义Markdown文件目录
md_directory = 'SHTKU题库'  # 替换为你的.md文件路径

# 定义存储题目类别的列表
category_map = []
current_category = ""
question_count = 1

# 获取按自然顺序排列的Markdown文件
files = [f for f in os.listdir(md_directory) if f.endswith('.md')]
files.sort(key=lambda f: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', f)])

# 遍历每个文件，解析题目和类别
for filename in files:
    file_path = os.path.join(md_directory, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # 识别大类标题
        if re.match(r"^# \d+\. ", line):
            # 新的大类，记录当前类别名称
            current_category = re.sub(r"^# \d+\. ", "", line).strip()

        # 识别题目标题（以###开头，表示一个新题目）
        elif line.startswith("###"):
            category_map.append({
                "question_id": question_count,
                "category": current_category
            })
            question_count += 1

# 将类别映射写入JSON文件
with open('category_map.json', 'w', encoding='utf-8') as f:
    json.dump(category_map, f, ensure_ascii=False, indent=4)

print("题目分类文件已生成：category_map.json")
