import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.utils import to_categorical

# 参数设定
unlabeled_dir = 'F:/python-pycharm/align'         # 未标注图像文件夹路径
output_dir = 'F:/pseudo_labeled_images'               # 输出的伪标签分类图像路径
model_path = 'F:/python-pycharm/0321face_expression_recognition/ResNet50_Student_Emotion2.h5'              # 已训练模型的路径
img_size = (224, 224)                              # 图像大小应与模型一致
confidence_threshold = 0.94                       # 置信度阈值（可调节）
class_names = ['Boring', 'Confused', 'Engaged', 'Happy', 'Neutral', 'Tired', 'Yawning'] #修改实际标签

# 创建输出目录（每个类别一个子文件夹）
os.makedirs(output_dir, exist_ok=True)
for class_name in class_names:
    os.makedirs(os.path.join(output_dir, class_name), exist_ok=True)

# ---------- 加载模型 ----------
model = load_model(model_path)

# ---------- 遍历图像并分类 ----------
for img_name in os.listdir(unlabeled_dir):
    img_path = os.path.join(unlabeled_dir, img_name)

    try:
        # 加载并预处理图像
        img = load_img(img_path, target_size=img_size)
        # img_array = img_to_array(img)
        # img_array = np.expand_dims(img_array, axis=0)
        # img_array = preprocess_input(img_array)  # ✅ ResNet50 专属预处理
        face = img_to_array(img) / 255.0
        face = np.expand_dims(face, axis=0)

        # 预测
        preds = model.predict(face)
        pred_label = np.argmax(preds)
        confidence = np.max(preds)

        # 高置信度图像分类保存
        if confidence >= confidence_threshold:
            label_name = class_names[pred_label]
            target_path = os.path.join(output_dir, label_name, img_name)
            shutil.copy(img_path, target_path)
            print(f"[✓] Saved {img_name} to {label_name} (confidence={confidence:.2f})")
        else:
            print(f"[✗] Skipped {img_name} (low confidence: {confidence:.2f})")

    except Exception as e:
        print(f"[!] Error processing {img_name}: {e}")