from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras import models
import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.models import load_model
import csv
from openpyxl import Workbook

if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")
# face detection model
net = cv2.dnn.readNetFromTensorflow("models/opencv_face_detector_uint8.pb", "models/opencv_face_detector.pbtxt")

# emotion models
#model = models.load_model('models/alexnetfer2013ck_model.pth')
#model = models.load_model('models/FER_Model.h5') #最开始使用的模型
model = load_model(
    'F:/0321face_expression_recognition/ResNet50_Student_Emotion2.h5'
)

EMOTIONS = ['Boring', 'Confused', 'Engaged', 'Happy', 'Neutral', 'Tired', 'Yawning']
# starting video streaming
cv2.namedWindow('test_video')
camera = cv2.VideoCapture("1.mp4")
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),  int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('museum2.avi', fourcc, 20.0, size, True)
#out = cv2.VideoWriter('class_15s_output.mp4', fourcc, 20.0, (512, 288), True)

# used to record the time when we processed last frame
prev_frame_time = 0
# used to record the time at which we processed current frame
new_frame_time = 0
# 定义跳帧间隔
SKIP_FRAMES = 30
# 初始化计数器变量
frame_count = 0
#保存结果
result=[]
while True:
    image = camera.read()[1]
    if image is None:
        break
    else:
        frame_count += 1
        if frame_count % SKIP_FRAMES==0:
            # new_frame_time = time.time()
            # fps = 1 / (new_frame_time - prev_frame_time)
            # prev_frame_time = new_frame_time
            # fps = str(fps)
            # cv2.putText(image, fps, (1600, 900), cv2.FONT_HERSHEY_PLAIN, 3, (100, 255, 0), 3, cv2.LINE_AA)
            # image = imutils.resize(image, width=1040)
            h, w = image.shape[:2]
            blob = cv2.dnn.blobFromImage(image, 1.1, (1040, 585), [104., 117., 123.], False, False)
            # blob = cv2.dnn.blobFromImage(image, 1.1, (512, 288), [104., 117., 123.], False, False)
            #start_time1 = time.time()
            net.setInput(blob)
            detections = net.forward()
            #end_time1 = time.time()
            # print(f"Execution time of detecting: {end_time1 - start_time1} seconds")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            frameClone = image.copy()
            #start_time2 = time.time()
            frame_emotion = [frame_count]
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.6:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h]) #
                    (startX, startY, endX, endY) = box.astype('int')
                    # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
                    # the ROI for classification via the CNN
                    roi = gray[startY:endY, startX:endX]
                    roi = cv2.resize(roi, (224, 224))
                    roi = roi.astype("float") / 255.0
                    roi = np.expand_dims(roi, axis=0)
                    #roi = np.array(roi, dtype='float32').reshape(-1, 48, 48, 1)
                    start_time3 = time.time()
                    preds = model.predict(roi)
                    end_time3 = time.time()
                    # print(f"Execution time of face{i}: {end_time3 - start_time3} seconds")
                    emotion_probability = np.max(preds)
                    label = EMOTIONS[preds.argmax()]
                    frame_emotion.append(label) #保存一帧中的所有学生的情绪标签
                    img_text = "{}: {:.2f}%".format(label, emotion_probability * 100)
                    cv2.putText(frameClone, img_text, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    cv2.rectangle(frameClone, (startX, startY), (endX, endY),
                                  (0, 0, 255), 2)
                else:
                    continue
            result.append(frame_emotion)

            #end_time2 = time.time()
            #print(f"Execution time of frame: {end_time2 - start_time2} seconds")
            cv2.imshow('test_video', frameClone)
            out.write(frameClone)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
camera.release()
out.release()
cv2.destroyAllWindows()
#将结果写入Excel
# 创建一个新的Excel工作簿
wb = Workbook()
ws = wb.active


# 写入数据
for row_num, row in enumerate(result[0:], start=2):  # 写入数据
    for col_num, cell in enumerate(row, start=1):
        ws.cell(row=row_num, column=col_num, value=cell)

# 保存工作簿
wb.save('test1.xlsx')

