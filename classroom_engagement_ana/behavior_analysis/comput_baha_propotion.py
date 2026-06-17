import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei），您也可以选择其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 读取Excel文件（假设文件名为'face_expression.xlsx'，需要根据实际文件名修改）

df = pd.read_excel('F:/python-pycharm/classroom_engagement_ana/behavior_analysis/输出/pai_402_de_nan.xlsx')

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

# 定义不同行为类别
Passive_behavioral = ['listening', 'reading']
Proactive_behavioral = ['writing', 'raising_hand']
Interactive_behavioral = ['standing','leaning_the_body']
Non_behavioral=['looking_around','lyingon_desk','other']
#Non_behavioral=['lyingon_desk','other']


# 创建一个新的列分类学习行为为主动、被动、互动、脱离
def classify_behavior(behavior):
    if behavior in Passive_behavioral:
        return 'Passive'
    elif behavior in Proactive_behavioral:
        return 'Proactive'
    elif behavior in Interactive_behavioral:
        return 'Interactive'
    elif behavior in Non_behavioral:
        return 'Non'
    else:
        return 'unknow'  # 如果存在未知的情绪标签

# 从第二列开始遍历每个学生的行为列，并应用行为分类
behavior_columns = df.columns[1:]  # 从第二列开始是情绪数据
for col in behavior_columns:
    df[col] = df[col].apply(classify_behavior)

# 将时间按30秒间隔分组，得到每个5秒段的统计
# 假设时间为整数秒数，按5秒划分时间段
df['TimeInterval'] = (df['Time'] // 5) * 5  # 将时间按5秒分组，取整

# 统计每个时间段内的积极、消极和中性情绪数量
behavior_counts = df.groupby('TimeInterval')[behavior_columns].apply(
    lambda x: pd.Series({
        'Passive': (x == 'Passive').sum().sum(),  # 所有学生的积极情绪总和
        'Proactive': (x == 'Proactive').sum().sum(),
        'Interactive': (x == 'Interactive').sum().sum(),
        'Non': (x == 'Non').sum().sum()
    })
)

# 归一化处理：将每种情绪数量归一化为0到1之间
# max_values = emotion_counts.max()  # 计算每种情绪的最大值，用于归一化
# normalized_emotion_counts = emotion_counts / max_values  # 对情绪计数进行归一化处理
row_sums = behavior_counts.sum(axis=1)
normalized_emotion_counts = behavior_counts.div(row_sums, axis=0)

output_file = 'F:/python-pycharm/classroom_engagement_ana/behavior_analysis/输出/pai_402_propotion.xlsx'  # 输入你希望保存的文件路径
normalized_emotion_counts.to_excel(output_file)

