import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# #构造函数，用拐点法确认最佳k值
# def k_SSE(X, clusters):
#     # 选择连续的K种不同的值
#     K = range(1, clusters + 1)
#     # 构建空列表用于存储总的簇内离差平方和
#     TSSE = []
#     for k in K:
#         # 用于存储各个簇内离差平方和
#         SSE = []
#         kmeans = KMeans(n_clusters=k)
#         kmeans.fit(X)
#         # 返回簇标签
#         labels = kmeans.labels_
#         # 返回簇中心
#         centers = kmeans.cluster_centers_
#         # 计算各簇样本的离差平方和，并保存到列表中
#         for label in set(labels):
#             SSE.append(np.sum((X.loc[labels == label,] - centers[label, :]) ** 2))
#         # 计算总的簇内离差平方和
#         TSSE.append(np.sum(SSE))
#
#     # 中文和负号的正常显示
#     plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#     plt.rcParams['axes.unicode_minus'] = False
#     # 设置绘图风格
#     plt.style.use('ggplot')
#     # 绘制K的个数与GSSE的关系
#     plt.plot(K, TSSE, 'b*-')
#     plt.xlabel('簇的个数',)
#     plt.ylabel('误差平方和（SSE）')
#     # 显示图形
#     plt.show()

# 加载数据
df = pd.read_excel('F:/python-pycharm/classroom_engagement_ana/behavior_analysis/课堂学习投入_聚类原始数据.xlsx')

# 计算每个时间点的行为频率
X = df.iloc[:, 1:]

# 假设我们选择行为频率作为特征进行聚类
#k_SSE(X, 15)

# 选择聚类数k（假设我们选择k=4）
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
X['Cluster'] = kmeans.fit_predict(X)

#保存聚类后的结果
X.to_excel('F:/python-pycharm/classroom_engagement_ana/behavior_analysis/4cluster_output_engagement.xlsx')
#  查看聚类结果
# print(df[['时间（秒）', 'Cluster']].head())
#
# # 可视化聚类结果
# plt.figure(figsize=(10, 6))
# plt.scatter(df['时间（秒）'], df['Cluster'], c=df['Cluster'], cmap='viridis')
# plt.title('Classroom Activity Segments')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Cluster')
# plt.colorbar(label='Cluster')
# plt.show()

# 查看每个聚类的时间范围和行为模式
# for cluster_num in df['Cluster'].unique():
#     cluster_data = df[df['Cluster'] == cluster_num]
#     print(f"Cluster {cluster_num} (Teaching Segment):")
#     print(f"Time range: {cluster_data['时间（秒）'].min()} to {cluster_data['时间（秒）'].max()}")
#     print(f"Sample behaviors:\n{cluster_data.iloc[:, 1:].mean()}\n")


