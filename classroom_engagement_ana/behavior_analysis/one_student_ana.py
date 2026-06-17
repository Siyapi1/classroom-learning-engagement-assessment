import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
# 设置支持英文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei），您也可以选择其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 设置全局字体为 Times New Roman
#plt.rcParams['font.family'] = 'Times New Roman'
# 时间格式化函数：将秒数转换为 00:01 格式
def time_formatter(x, pos):
    return f'{int(x // 60):02}:{int(x % 60):02}'
# Step 1: 读取Excel文件
# 请根据你的文件路径修改文件名
file_path = 'F:/python-pycharm/classroom_engagement_ana/emotion_analysis/student4_behavior_emotion.xlsx'
df = pd.read_excel(file_path)

# Step 2: 数据预处理
# 假设数据结构为：
# 第一列：秒数
# 第二列：学习行为
# 第三列：学习情感状态

time_in_seconds = df.iloc[:, 0]  # 第一列：秒数
behavior = df.iloc[:, 1]         # 第二列：行为
emotion = df.iloc[:, 2]          # 第三列：情感状态

# Step 3: 每30秒为一组，按时间分组
time_interval = 4  # 时间间隔：30秒
df['time_group'] = (time_in_seconds // time_interval) * time_interval  # 计算每30秒的时间段

# Step 4: 按时间段统计每个时间段的主要行为和情感
# 使用多数投票法获取每个时间段的主要行为和情感
def most_frequent(lst):
    return lst.mode()[0]  # 获取出现次数最多的元素

# 每个时间段内的主要行为和情感
grouped = df.groupby('time_group').agg({
    'behavior': most_frequent,
    'emotion': most_frequent
}).reset_index()
#定义教学环节
teaching_phases = {
    "课堂引入": (0, 180, 'lightcoral'), # 时间区间：0到180秒
    "巩固练习": (180, 1260,'lightgreen'),
    "课堂讲授": (1260, 2280,'lightblue'),
    "课堂总结": (2280, 2460,'#D8B6E0')
}

# Step 5: 绘制图形
plt.figure(figsize=(10, 6))

# 绘制行为（实线）
plt.plot(grouped['time_group'], grouped['behavior'], label='行为投入', linestyle='-', color='#9271B1', linewidth=2)

# 绘制情感（虚线）
plt.plot(grouped['time_group'], grouped['emotion'], label='情感投入',linestyle='-', color='#C367A2', linewidth=2)

# 标注不同教学环节
# for phase, (start, end, color) in teaching_phases.items():
#     plt.axvspan(start, end, color=color, alpha=0.5)  # 用不同颜色的区域表示每个教学环节
#     # 在每个教学环节区域的中间添加文本标注
#     plt.text((start + end) / 2, 2.5, phase, horizontalalignment='center', fontsize=12, color='black')

for phase, (start, end, color) in teaching_phases.items():
    # 绘制不同颜色的区域表示每个教学环节
    plt.axvspan(start, end, color=color, alpha=0.5)

    # 将标签放置在每个教学环节区块的中间
    # plt.text(start + (end - start) / 2, 1 + 0.2, phase,
    #          horizontalalignment='center', fontsize=12, color='black', weight='bold')


# 添加标题和标签
#plt.title('学生学习行为与情感状态随时间的演变', fontsize=14)
plt.xlabel('时间', fontsize=12)
#plt.ylabel('状态值', fontsize=12)

# 添加图例
plt.legend()

# 自定义横坐标时间格式
plt.gca().xaxis.set_major_formatter(FuncFormatter(time_formatter))

# 设置横坐标显示的刻度数量（至少10个）
# time_seconds = np.arange(0, 2401, 120)
# plt.xticks(time_seconds, labels=[f"{t//60}" for t in time_seconds])  # 转换为 "分钟:秒" 格式
#plt.xticks(ticks=range(0, 2401, 120), rotation=0)  # 这里我们手动设置了横坐标显示的时间点
plt.xticks(ticks=range(0, 2401, 200), rotation=0,fontsize=12)  # 这里我们手动设置了横坐标显示的时间点
plt.xlim(left=0, right=2401)
plt.xlim(left=0, right=2401)
#plt.legend(title="教学环节")
# 去除坐标轴与图形边缘之间的空隙
plt.xlim(left=0)  # 确保x轴从0开始
plt.ylim(bottom=0)  # 确保y轴从0开始

# 调整图形边距，使坐标轴从(0, 0)开始没有空隙
#plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
# 显示图形
plt.grid(True)
plt.show()