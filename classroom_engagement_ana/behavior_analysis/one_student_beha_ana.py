import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']            # 设置中文为宋体
plt.rcParams['axes.unicode_minus'] = False             # 解决负号无法显示的问题
plt.rcParams.update({
    #'font.size': 12,  # 设置全局字体大小
    'axes.titlesize': 14,  # 坐标轴标题字体大小
    'axes.labelsize': 14,  # 坐标轴标签字体大小
    'xtick.labelsize': 14,  # x轴刻度字体大小
    'ytick.labelsize': 14,  # y轴刻度字体大小
    'legend.fontsize': 14,  # 图例字体大小
    'figure.titlesize': 14  # 图形标题字体大小
})
# 时间格式化函数：将秒数转换为 00:01 格式
def time_formatter(x, pos):
    return f'{int(x // 60):02}:{int(x % 60):02}'
# Step 1: 读取Excel文件
# 请根据你的文件路径修改文件名
file_path = 'F:/python-pycharm/classroom_engagement_ana/behavior_analysis/6_student/student2_200s.xlsx'
df = pd.read_excel(file_path)

# Step 2: 数据预处理
# 假设数据结构为：
# 第一列：秒数
# 第二列：学习行为
# 第三列：学习情感状态

time_in_seconds = df.iloc[:, 0]  # 第一列：秒数
behavior = df.iloc[:, 1]         # 第二列：行为
#emotion = df.iloc[:, 2]          # 第三列：情感状态

# Step 3: 每30秒为一组，按时间分组
time_interval = 10 # 时间间隔：30秒
df['time_group'] = (time_in_seconds // time_interval) * time_interval  # 计算每30秒的时间段

# Step 4: 按时间段统计每个时间段的主要行为和情感
# 使用多数投票法获取每个时间段的主要行为和情感
def most_frequent(lst):
    return lst.mode()[0]  # 获取出现次数最多的元素

# 每个时间段内的主要行为和情感
grouped = df.groupby('time_group').agg({
    'behavior': most_frequent
}).reset_index()

# Step 5: 绘制图形
plt.figure(figsize=(10, 6))

# 绘制行为（实线）
plt.plot(grouped['time_group'], grouped['behavior'],  linestyle='-', color='#9271B1', linewidth=2)

# 绘制情感（虚线）
#plt.plot(grouped['time_group'], grouped['emotion'], label='面部表情', linestyle='-', color='#C367A2', linewidth=2)

# 添加标题和标签
plt.title('学生2每隔10秒检测结果', fontsize=16)
plt.xlabel('Time', fontsize=14)
#plt.ylabel('状态值', fontsize=12)

# 添加图例
#plt.legend()

# 自定义横坐标时间格式
#plt.gca().xaxis.set_major_formatter(FuncFormatter(time_formatter))

# 设置横坐标显示的刻度数量（至少10个）
plt.xticks(ticks=range(0, 210,10), rotation=0)  # 这里我们手动设置了横坐标显示的时间点
plt.xlabel('时间（秒）', fontsize=14)
# 显示图形
#plt.grid(True)
plt.show()