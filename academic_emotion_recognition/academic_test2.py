import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from openpyxl import Workbook
from mtcnn import MTCNN

# GPU 检查
if tf.config.list_physical_devices('GPU'):
    print('使用 GPU：{}'.format(tf.config.list_physical_devices('GPU')[0]))
else:
    print("使用 CPU 运行")

# 初始化 MTCNN
detector = MTCNN()

# 表情类别
EMOTIONS = ['Boring', 'Confused', 'Engaged', 'Happy', 'Neutral', 'Tired', 'Yawning']

# 加载模型
emotion_detection_model = load_model(
    'F:/python-pycharm/0321face_expression_recognition/ResNet50_Student_Emotion2.h5'
)

# 视频输入/输出初始化
cv2.namedWindow('test_video')
#camera = cv2.VideoCapture("F:/videos_dongzhimen/5.8/杜/01_1.mp4")
camera = cv2.VideoCapture("F:/python-pycharm/emotion_recog_BeiHang/2_1.mp4")
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('2_1_output.avi', fourcc, 25.0, (1920, 1080), True)

result = []
frame_count = 0  # ✅ 新增帧计数器
DETECT_EVERY_N_FRAMES = 30  # ✅ 每隔N帧检测一次
def enhance_image(image):
    # 对比度增强
    image = cv2.convertScaleAbs(image, alpha=1.2, beta=10)
    # 锐化滤波器
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    image = cv2.filter2D(image, -1, kernel)
    return image
def align_face(image, left_eye, right_eye):
    eye_center = ((left_eye[0] + right_eye[0]) / 2,
                  (left_eye[1] + right_eye[1]) / 2)
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dy, dx))
    M = cv2.getRotationMatrix2D(eye_center, angle, scale=1)
    aligned = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC)
    return aligned

last_detection_result = []  # 缓存上一次的检测结果

while True:
    ret, image = camera.read()
    if not ret:
        break
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    if frame_count % DETECT_EVERY_N_FRAMES == 0:
        frame_emotion = []
        faces = detector.detect_faces(image_rgb)
        last_detection_result = []  # 清空之前结果
        frame_emotion = [frame_count]

        for face in faces:
            if face['confidence'] < 0.80:
                continue

            x, y, width, height = face['box']
            x, y = max(0, x), max(0, y)
            x2, y2 = min(image.shape[1] - 1, x + width), min(image.shape[0] - 1, y + height)

            face_img = image[y:y2, x:x2]
            if face_img.size == 0:
                continue

            keypoints = face['keypoints']
            left_eye = (keypoints['left_eye'][0] - x, keypoints['left_eye'][1] - y)
            right_eye = (keypoints['right_eye'][0] - x, keypoints['right_eye'][1] - y)

            aligned_face = align_face(face_img, left_eye, right_eye)
            aligned_face = cv2.resize(aligned_face, (224, 224))
            aligned_face = enhance_image(aligned_face)
            aligned_face = img_to_array(aligned_face) / 255.0
            aligned_face = np.expand_dims(aligned_face, axis=0)

            preds = emotion_detection_model.predict(aligned_face, verbose=0)
            emotion_probability = np.max(preds)
            label = EMOTIONS[np.argmax(preds)]

            frame_emotion.append(label)
            last_detection_result.append((x, y, x2, y2, label, emotion_probability))
        result.append(frame_emotion)


    # ➕ 每帧都使用上一次检测结果可视化
    for (x, y, x2, y2, label, prob) in last_detection_result:
        label_text = "{}: {:.2f}%".format(label, prob * 100)
        cv2.putText(image, label_text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)

    out.write(image)
    cv2.imshow("test_video", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1


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
wb.save('2_1_output.xlsx')