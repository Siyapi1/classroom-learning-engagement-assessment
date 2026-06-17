import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# 设置支持英文的字体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei），您也可以选择其他支持中文的字体
# plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 设置全局字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
# 读取Excel文件（假设文件名为'face_expression.xlsx'，需要根据实际文件名修改）

df = pd.read_excel('F:/python-pycharm/classroom_engagement_ana/behavior_analysis/输出/5.8_du_301_1_30frame.xlsx')

# 查看数据的结构
print(df.head())
time_column = df.iloc[:, 0]  # 第一列时间

# 时间格式化函数：将秒数转换为 00:01 格式
def time_formatter(x, pos):
    return f'{int(x // 60):02}:{int(x % 60):02}'

# 假设Excel文件的结构是这样的:
# 第一列是时间（单位秒），后面的列是学生的表情
# 例如：
# Time  Student1  Student2  Student3  ...
# 0.0    happy    sad       neutral  ...
# 1.0    sad      neutral   happy    ...
# ...
#定义教学环节
teaching_phases = {
    "课堂引入": (0, 180, 'lightcoral'), # 时间区间：0到180秒
    "巩固练习": (180, 1260,'lightgreen'),
    "课堂讲授": (1260, 2280,'lightblue'),
    "课堂总结": (2280, 2401,'#D8B6E0')
}
# 定义不同行为投入类别
Passive_behavioral = ['listening', 'reading']
Proactive_behavioral = ['writing', 'raising_hand']
Interactive_behavioral = ['standing','leaning_the_body']
Non_behavioral=['looking_around','lyingon_desk','other']
# 创建一个新的列分类情绪为积极、消极和中性
def classify_behavior(behavior):
    if behavior in Passive_behavioral:
        return 'Passive'
    elif behavior in Proactive_behavioral:
        return 'Proactive'
    elif behavior in Interactive_behavioral:
        return 'Interactive'
    elif behavior in Non_behavioral:
        return 'Non_behavioral'
    else:
        return 'unknown'  # 如果存在未知的情绪标签

# 从第二列开始遍历每个学生的情绪列，并应用情绪分类
behavior_columns = df.columns[1:]  # 从第二列开始是情绪数据
for col in behavior_columns:
    df[col] = df[col].apply(classify_behavior)

# 将时间按30秒间隔分组，得到每个30秒段的统计
# 假设时间为整数秒数，按30秒划分时间段
df['TimeInterval'] = (df['Time'] // 30) * 30  # 将时间按30秒分组，取整

# 统计每个时间段内的积极、消极和中性情绪数量
behavior_counts = df.groupby('TimeInterval')[behavior_columns].apply(
    lambda x: pd.Series({
        'Passive': (x == 'Passive').sum().sum(),  # 所有学生的被动行为总和
        'Proactive': (x == 'Proactive').sum().sum(),  # 所有学生的主动行为总和
        'Interactive': (x == 'Interactive').sum().sum(),     # 所有学生的互动行为总和
        'Non_behavioral': (x == 'Non_behavioral').sum().sum()     # 所有学生的非投入行为总和
    })
)

# 归一化处理：将每种情绪数量归一化为0到1之间
max_values = behavior_counts.max()  # 计算每种情绪的最大值，用于归一化
normalized_emotion_counts = behavior_counts / max_values  # 对情绪计数进行归一化处理


# 绘制情绪随时间的变化图
plt.figure(figsize=(10, 6))
#plt.plot(behavior_counts.index, behavior_counts['Passive'], label='被动行为', color='#9271B1')
plt.plot(behavior_counts.index, behavior_counts['Passive'], label='Passive Behavior', color='#9271B1')
#plt.plot(behavior_counts.index, behavior_counts['Proactive'], label='主动行为', color='#EF607A')
plt.plot(behavior_counts.index, behavior_counts['Proactive'], label='Active Behavior', color='#EF607A')
#plt.plot(behavior_counts.index, behavior_counts['Interactive'], label='互动行为', color='#3583B4')
plt.plot(behavior_counts.index, behavior_counts['Interactive'], label='Interactive Behavior', color='#3583B4')
#plt.plot(behavior_counts.index, behavior_counts['Non_behavioral'], label='脱离行为', color='#F4A7C1')
plt.plot(behavior_counts.index, behavior_counts['Non_behavioral'], label='Off-task Behavior', color='#F4A7C1')
for phase, (start, end, color) in teaching_phases.items():
    # 绘制不同颜色的区域表示每个教学环节
    plt.axvspan(start, end, color=color, alpha=0.5)


#plt.xlabel('时间(分钟)')
plt.xlabel('Time (minutes)')
plt.ylabel('Frequency')
#plt.ylabel('Number of behaviors')
#plt.title('不同行为投入水平随时间的变化')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 自定义横坐标时间格式
#plt.gca().xaxis.set_major_formatter(FuncFormatter(time_formatter))

# 设置横坐标显示的刻度数量（至少10个）
time_seconds = np.arange(0, 2401, 120)
plt.xticks(time_seconds, labels=[f"{t//60}" for t in time_seconds])  # 转换为 "分钟:秒" 格式
#plt.xticks(ticks=range(0, 2401, 120), rotation=0)  # 这里我们手动设置了横坐标显示的时间点
plt.xlim(left=0, right=2401)
#plt.legend(title="教学环节")
# 去除坐标轴与图形边缘之间的空隙
plt.xlim(left=0)  # 确保x轴从0开始
plt.ylim(bottom=0)  # 确保y轴从0开始

# 显示图形
plt.show()