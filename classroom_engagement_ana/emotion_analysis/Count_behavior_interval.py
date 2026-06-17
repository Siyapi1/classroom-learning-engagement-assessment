#每隔30帧统计行为类型


import pandas as pd
import numpy as np
from collections import Counter

# 1. 读取Excel数据
file_path = 'F:/python-pycharm/classroom_engagement_ana/emotion_analysis/one_students.xlsx'  # 替换为你的文件路径
df = pd.read_excel(file_path, index_col=0)

# 打印原始数据，检查数据结构
#print("原始数据:")
#print(df.head())

# 2. 将空值视为特殊类型（例如 "Empty"）
df = df.fillna("Empty")


# 3. 以30帧为间隔，统计每个视频段的主要行为类型
frame_interval = 30  # 每30帧为一个视频段
segments_result = []  # 用于存储每个学生每段的主要行为类型

# 遍历每个学生（即每一列）
for student in df.columns.tolist():
    student_behaviors = []  # 存储该学生每个视频段的主要行为类型
    print(f"\n处理学生 {student} 的行为数据:")

    # 按照帧数拆分数据，每段30帧
    for start_frame in range(0, len(df), frame_interval):
        # 计算该段的结束帧数，确保不超出行数
        end_frame = min(start_frame + frame_interval, len(df))
        segment = df.loc[start_frame:end_frame, student]

        # 打印当前段落的帧数据
        #print(f"帧 {start_frame} 到 {end_frame} 的行为数据:")
        #print(segment)

        # 统计该段视频中的行为类型
        counter = Counter(segment)
        major_behavior = counter.most_common(1)[0][0]  # 选出最常见的行为类型
        #print(f"该段的主要行为类型: {major_behavior}")

        student_behaviors.append(major_behavior)

    segments_result.append(student_behaviors)

# 4. 整理输出结果
result_df = pd.DataFrame(segments_result, columns=[f"{i + 1}" for i in range(len(segments_result[0]))],
                         index=df.columns)

# 打印统计结果
#print("\n统计结果:")
#print(result_df)
result_df1=result_df.T
# 5. 保存结果到Excel
output_file = 'F:/python-pycharm/classroom_engagement_ana/emotion_analysis/5.8_du_301_1_30frame.xlsx'  # 输入你希望保存的文件路径
result_df1.to_excel(output_file)

print(f"\n结果已保存到 {output_file}")
