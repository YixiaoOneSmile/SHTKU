import os
import json
import re

# 定义要读取的.md文件所在目录路径
md_directory = 'SHTKU题库'  # 替换为你的文件夹路径

# JSON输出列表
output = []
id_counter = 1

# 获取目录下所有.md文件，并手动按照自然顺序排序
files = [f for f in os.listdir(md_directory) if f.endswith('.md')]

# 按照自然顺序排序文件名（处理类似'1.1'、'1.2'、'2.1'这样的顺序）
files.sort(key=lambda f: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', f)])

# 遍历排序后的.md文件
for filename in files:
    file_path = os.path.join(md_directory, filename)

    # 打开.md文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 提取每个文件中的题目信息
    question = None
    answers = []
    right_answer = None
    title = None

    for i, line in enumerate(lines):
        line = line.strip()

        # 识别题目标题（以###开头）
        if line.startswith("###"):
            title = re.sub(r"^\d+(\.\d+)?\s*", "", line.lstrip("# ").replace("**", "").replace(". ", "").strip())

        # 识别题干（以"- "开头的下一行）
        elif line.startswith("- ") and title:
            # 合并标题和题干
            question = f"{title}: {line[2:].strip()}"
            answers = []
            right_answer = None
            title = None  # 重置标题

        # 识别选项（以 "- A."、"- B." 等开头）
        elif re.match(r"- [A-D]\.", line):
            label = line[2]  # 获取选项标签（A, B, C, D）
            text = line[5:].strip()  # 获取选项文本
            answers.append({"label": label, "text": text})

        # 识别正确答案（以 "**正确答案：" 开头）
        elif line.startswith("- **正确答案："):
            right_answer = line.split("：")[-1].replace("**", "").strip()

        # 如果当前行为空且已有完整题目，则保存题目信息
        if line == "" and question:
            output.append({
                "id": id_counter,
                "question": question,
                "answers": answers,
                "rightanswer": right_answer
            })
            id_counter += 1
            question = None

    # 处理文件中的最后一个题目
    if question:
        output.append({
            "id": id_counter,
            "question": question,
            "answers": answers,
            "rightanswer": right_answer
        })

# 转换为JSON格式
json_output = json.dumps(output, indent=4, ensure_ascii=False)

# 打印或保存为JSON文件
output_file = os.path.join(md_directory, 'question_bank.json')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(json_output)

print(f"JSON文件已生成：{output_file}")
