import cv2
import dlib
import numpy as np
from tensorflow.keras.models import load_model
from openpyxl import Workbook
from fer import FER

# 加载人脸检测模型
face_net = cv2.dnn.readNetFromTensorflow("models/opencv_face_detector_uint8.pb", "models/opencv_face_detector.pbtxt")

# 加载表情识别模型（假设您使用 FER 模型）
emotion_model = load_model('models/FER_Model.h5')
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
            "neutral"]
# 加载 FER 库的表情识别器
#emotion_detector = FER()

# 初始化 dlib 的人脸追踪器
tracker = dlib.correlation_tracker()

# 用于跟踪的字典
trackers = []
face_ids = []  # 用于存储每个人脸的ID
frame_count = 0  # 帧计数器
frame_interval = 30  # 每30帧进行一次检测

# 打开视频文件
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# 创建Excel文件并初始化
wb = Workbook()
ws = wb.active
ws.append(['Frame', 'Face_ID', 'Emotion', 'Confidence'])

# 处理视频
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # 每隔若干帧进行一次人脸检测与追踪
    if frame_count % frame_interval == 0:
        h, w = frame.shape[:2]

        # 使用 DNN 模型进行人脸检测
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 117, 123), swapRB=False, crop=False)
        face_net.setInput(blob)
        detections = face_net.forward()

        # 获取检测到的人脸
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                faces.append((x1, y1, x2, y2))

        # 初始化新的追踪器
        for face in faces:
            x1, y1, x2, y2 = face
            # 对每个检测到的人脸创建并启动一个新的追踪器
            new_tracker = dlib.correlation_tracker()
            new_tracker.start_track(frame, dlib.rectangle(x1, y1, x2, y2))
            trackers.append(new_tracker)
            face_ids.append(len(trackers))  # 给每个追踪器分配一个唯一的ID

    # 更新所有追踪器的位置并识别表情
    for i, tracker in enumerate(trackers):
        tracker.update(frame)
        pos = tracker.get_position()
        x1, y1, x2, y2 = int(pos.left()), int(pos.top()), int(pos.width()), int(pos.height())

        # 在人脸上画框
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        #转变为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 提取人脸区域并进行表情识别
        roi = gray[y1:y2, x1:x2]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.array(roi, dtype='float32').reshape(-1, 48, 48, 1)

        #emotion, score = emotion_detector.top_emotion(face_region)
        preds = emotion_model.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]

        # 将表情类型和置信度显示在视频上
        cv2.putText(frame, f"ID: {face_ids[i]}, {label}: {emotion_probability:.2f}",
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 将识别结果写入Excel
        ws.append([frame_count, face_ids[i], label, emotion_probability])

    # 显示视频帧
    cv2.imshow('Classroom Video', frame)

    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 保存结果到Excel
wb.save("pai_305_1.xlsx")

# 释放资源
cap.release()
cv2.destroyAllWindows()
