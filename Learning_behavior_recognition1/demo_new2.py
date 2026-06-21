from objdetector import Detector
import imutils
import cv2
import copy
from Classificationv5 import  Classificationv5
import pandas as pd
import torch
import torch.nn.functional as F
from models.common import DetectMultiBackend
from utils.augmentations import (classify_transforms)
from utils.general import ( Profile,cv2,)
from utils.torch_utils import select_device


VIDEO_PATH = '/video.mp4'
weights='/train-cls/exp8/weights/best.pt'  # model.pt path(s)
data='F:/python-pycharm/0625yolov5-7.0/data/coco128.yaml'  # dataset.yaml path
RESULT_PATH = '01_1_output.mp4'
imgsz=(224, 224)  # inference size (height, width)
#device='cpu' # cuda device, i.e. 0 or 0,1,2,3 or cpu
device='0' # cuda device, i.e. 0 or 0,1,2,3 or cpu
# 定义跳帧间隔
SKIP_FRAMES = 2


func_status = {}
func_status['headpose'] = None

name = 'demo'

det = Detector()
cap = cv2.VideoCapture(VIDEO_PATH)
fps = int(cap.get(5))
print('fps:', fps)

t = int(1000 / fps)
d_result = dict()
size = None
videoWriter = None
# 初始化计数器变量
frame_counter = 0

# Load model
device = select_device(device)
model = DetectMultiBackend(weights, device=device, dnn=False, data=data, fp16=False)
stride, names, pt = model.stride, model.names, model.pt
bs = 1  # batch_size
transforms=classify_transforms(imgsz[0])
model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
seen, dt = 0, (Profile(), Profile(), Profile())

while True:

    # try:
    _, im = cap.read()
    if im is None:
        break
    oldimg = copy.deepcopy(im)
    frame_counter += 1
    result = det.feedCap(im, func_status)

    box = result['obj_bboxes']
    result = result['frame']
    height, width, _ = result.shape

    for box_i in box:
        if str(box_i[5]) not in d_result:
            d_result[str(box_i[5])] = []
        img_i = oldimg[int(box_i[1]):int(box_i[3]),int(box_i[0]):int(box_i[2])]
        im = transforms(img_i)
        with dt[0]:
            im = torch.Tensor(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
        # Inference
        with dt[1]:
            results = model(im)

        # Post-process
        with dt[2]:
            pred = F.softmax(results, dim=1)  # probabilities
        # Process predictions
        for i, prob in enumerate(pred):  # per image
            seen += 1
            # Print results
            top = prob.argsort(0, descending=True)[:1].tolist()  # top 5 indices
        re = names[top[0]]

        d_result[str(box_i[5])].append([str(frame_counter) + '-' + str(re)])
        cv2.putText(result, str(re), (box_i[0],  box_i[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    result = imutils.resize(result, height=800)
    if videoWriter is None:
        fourcc = cv2.VideoWriter_fourcc(
            'm', 'p', '4', 'v')  # opencv3.0
        videoWriter = cv2.VideoWriter(
            RESULT_PATH, fourcc, fps, (result.shape[1], result.shape[0]))

    videoWriter.write(result)
    cv2.imshow(name, result)
    cv2.waitKey(t)

    if cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) < 1:
        # 点x退出
        break
cap.release()
videoWriter.release()
cv2.destroyAllWindows()
df = pd.DataFrame.from_dict(d_result, orient='index')  
df_transposed = df.T

# 写入Excel文件
#df_transposed.to_excel('04_1.xlsx',engine='openpyxl', index=False)
out_csv='/output.csv'
df_transposed.to_csv(out_csv, index=False)