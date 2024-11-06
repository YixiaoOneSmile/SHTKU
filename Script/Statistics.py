import os
import re
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 设置字体
plt.rcParams['font.sans-serif'] = ['Times New Roman', 'Heiti TC', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义要读取的.md文件所在目录路径
md_directory = 'SHTKU题库'  # 替换为你的文件夹路径

# 定义每个类别的缩写
category_abbreviations = {
    "热处理基础理论": "FT",
    "热处理工艺设计与优化": "PDO",
    "表面处理与物质扩散": "STMD",
    "热处理缺陷分析与解决": "DAR",
    "材料类型与选择": "MTS",
    "生产管理与安全": "PMS",
    "金属材料科学基础": "FMS"
}

# 初始化分类统计字典
category_count = {}

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

    # 识别大类（文件第一行包含大类信息）
    if lines:
        first_line = lines[0].strip()
        if first_line.startswith("#"):
            question_category = re.sub(r"^\d+\.\s*", "", first_line.replace("#", "").replace("*", "").strip())
            # 使用缩写初始化分类计数
            question_category_abbr = category_abbreviations.get(question_category, question_category)
            if question_category_abbr not in category_count:
                category_count[question_category_abbr] = 0

    # 累计题目数量
    for line in lines:
        if line.strip().startswith("###"):
            category_count[question_category_abbr] += 1

# 生成题目分类的饼图
labels = list(category_count.keys())
sizes = list(category_count.values())
colors = plt.get_cmap("tab20c").colors[:len(labels)]  # 美观的颜色调色板

# 绘制饼图
plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(
    sizes, 
    labels=labels,  # 将类别缩写显示在图上
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    wedgeprops=dict(edgecolor='w', width=0.3, linestyle='-', linewidth=1),
    explode=[0.05] * len(labels), 
    shadow=True
)

# 调整百分比和缩写文字的样式（加大字体）
for text in texts:
    text.set_size(14)  # 增加类别缩写的字体大小
    text.set_weight("bold")  # 设置为粗体

for autotext in autotexts:
    autotext.set_size(14)  # 更大字体的百分比数字
    autotext.set_color("black")  # 将百分比文本设置为黑色
    autotext.set_weight("bold")

# 在图表外右下角显示图例
plt.legend(wedges, labels, title="Categories", loc="lower right", bbox_to_anchor=(1.25, 0), fontsize=10, frameon=True)

# 居中标题
plt.title('SHTKU Question Distribution', fontsize=16, weight="bold", loc='center')

# 调整布局，确保图例不覆盖图表
plt.tight_layout(rect=[0, 0, 0.95, 1])  # 留出空间以便图例不覆盖图表

# 保存图像
output_path = os.path.join(md_directory, "SHTKU_Question_Distribution.png")
plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
print(f"图像已保存到：{output_path}")

# 显示图像
plt.show()
