import pandas as pd

# 读取 Excel 文件（第一列为时间，其余列为情绪标签）
file_path = 'F:/python-pycharm/classroom_engagement_ana/emotion_analysis/学业情绪/5.8_du_01_1.xlsx'  # 修改为你的文件路径
df = pd.read_excel(file_path)

# 提取情绪数据列（假设从第2列开始）
emotion_columns = df.columns[1:]

# 定义情绪类别
emotion_types = ['Engaged', 'Happy','Neutral', 'Tired', 'Yawning','Boring','Confused', 'Empty']

# 准备一个新 DataFrame 来存储比例结果
proportion_df = pd.DataFrame()
proportion_df['Time'] = df.iloc[:, 0]  # 保留时间列

# 对每一行计算各类情绪比例
def calc_emotion_proportion(row):
    counts = row.value_counts()
    total = len(row)
    return [counts.get(emotion, 0) / total for emotion in emotion_types]

# 应用到每一行
proportions = df[emotion_columns].apply(calc_emotion_proportion, axis=1, result_type='expand')
proportions.columns = [f'{emotion}_ratio' for emotion in emotion_types]

# 合并时间列 + 比例数据
result_df = pd.concat([proportion_df, proportions], axis=1)

# 保存到新的 Excel 文件
output_path = 'emotion_ratios_per_row.xlsx'
result_df.to_excel(output_path, index=False)
print("✅ 每行情绪比例已保存：", output_path)
