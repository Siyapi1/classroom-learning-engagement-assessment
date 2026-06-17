import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 数据
df = pd.read_excel('E:/task-YY/20240319博士大论文/识别结果/行为识别结果/5.8/杜/one_student_major_behaviors.xlsx')

# 查看数据的前几行，确保读取正确
print(df.head())

# 删除第一列（秒数列），保留学生的行为数据
df_students = df.drop(columns=['秒数'])

# 统计每个学生不同行为类别的数量
behavior_counts = df_students.apply(pd.Series.value_counts, axis=0).fillna(0)

# 将每个学生不同行为类别的数量转为比例（每列总和为 100%）
behavior_proportions = behavior_counts / behavior_counts.sum(axis=0)

# 将比例转换为百分比
behavior_proportions_percent = behavior_proportions * 100

# 查看比例数据
print(behavior_proportions_percent.head())

# 绘制堆积图
plt.figure(figsize=(12, 8))

# 绘制堆积图，百分比数据
behavior_proportions_percent.plot(kind='bar', stacked=True, figsize=(12, 8))

# 设置图表标题和标签
plt.title('学生不同行为识别类别所占比例')
plt.xlabel('学生编号')
plt.ylabel('百分比')
plt.xticks(rotation=45)
plt.legend(title='行为类别')

# 显示图形
plt.tight_layout()
plt.show()