import pandas as pd
import numpy as np
import time

PATH = 'E:/task-YY/20240319博士大论文/识别结果/行为识别结果/4.24/'
filename = 'E:/task-YY/20240319博士大论文/识别结果/行为识别结果/4.24/pai_302_1.xlsx'
# filename = 'test.xlsx'

file = pd.read_excel(filename,index_col=0)
print(file.head())
print("—— start ——")
data = np.array(file.T)
# size = 140
# 这里的size是我直接打开文件看到的最大的，不知道怎么能直接获取最大帧
size = 73801
# print(data)
# 73800 138
res = []
start = time.time()
for stud in data:
    # 这里如果要显示nan，就用第一个，显示空格就用第二个
    # ls = [np.nan for i in range(140)]
    ls = ['' for i in range(size)]
    for act in stud:
        if(type(act) == float):
            continue
        act = act.strip('[\'\']')
        index, ing = act.split('-')
        ls[int(index)] = ing
    res.append(ls)
end = time.time()
res = pd.DataFrame(np.array(res)).T

print(res)
print('—— finish ——')
print('—— out ——')
# 直接输出xlsx会卡住，可能因为太大了要运行久一点，或许可以用csv格式输出
# res.to_excel(PATH + 'output.xlsx', header=file.columns)
res.to_csv(PATH + 'pai_302_1_handle.csv', header=file.columns)
print('—— done ——')
print("time: "+str(end-start)+'s')