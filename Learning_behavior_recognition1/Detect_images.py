import torch
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# 加载目标检测和行为识别模型
detection_model = torch.hub.load('ultralytics/yolov5', 'custom', path='F:/python-pycharm/yolov5-deepsort/weights/stu_weights/best.pt',
                                 force_reload=True)  # 替换为你的模型路径
behavior_model =torch.hub.load('ultralytics/yolov5', 'custom', path='F:/python-pycharm/yolov5-deepsort/weights/beha_weights/best.pt',
                                 force_reload=True)  # 替换为你的模型路径
#behavior_model = torch.jit.load('F:/python-pycharm/yolov5-deepsort/weights/beha_weights/best.pt')  # 加载行为识别模型，假设行为识别模型为torchscript格式

# 输入文件夹和输出文件夹路径
input_folder = 'F:/python-pycharm/yolov5-deepsort/test_images'
output_folder = 'F:/python-pycharm/yolov5-deepsort/out_images'
os.makedirs(output_folder, exist_ok=True)

# 遍历图像文件夹
for img_file in os.listdir(input_folder):
    if img_file.endswith(('.jpg', '.png', '.jpeg')):
        # 读取图像
        img_path = os.path.join(input_folder, img_file)
        img = cv2.imread(img_path)

        # 图像预处理 (如果需要，根据模型需求修改)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 目标检测
        detection_results = detection_model(img_rgb)
        detected_boxes = detection_results.xyxy[0].cpu().numpy()  # 检测结果中的边框

        # 遍历每个检测到的目标
        for i, box in enumerate(detected_boxes):
            x1, y1, x2, y2, conf, cls = box
            if conf < 0.5:  # 过滤掉置信度低的检测
                continue

            # 裁剪出检测到的目标区域
            student_img = img[int(y1):int(y2), int(x1):int(x2)]

            # 对学生目标进行行为识别
            student_img_rgb = cv2.cvtColor(student_img, cv2.COLOR_BGR2RGB)
            student_img_resized = cv2.resize(student_img_rgb, (224, 224))  # 假设行为识别模型需要224x224的输入
            student_img_tensor = torch.from_numpy(student_img_resized).permute(2, 0, 1).unsqueeze(
                0).float() / 255.0  # 转换为Tensor
            device = torch.device('cuda:0')
            student_img_tensor = student_img_tensor.to(device)

            # 行为识别推理
            with torch.no_grad():
                behavior_output = behavior_model(student_img_tensor)
                behavior_prediction = torch.argmax(behavior_output, dim=1).item()

            # 定义行为类别名称
            behavior_classes = ['leaning_the_body', 'listening', 'looking_around', 'lyingon_desk','other','raising_hand','reading','standing','writing']  # 根据你的模型定义
            behavior_label = behavior_classes[behavior_prediction]

            # 在原图上绘制检测框和行为类别
            label = f'{behavior_label} {conf:.2f}'
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # 保存带有可视化结果的图像
        output_img_path = os.path.join(output_folder, img_file)
        cv2.imwrite(output_img_path, img)

        # 也可以使用matplotlib显示图像（可选）
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # plt.show()

print("处理完毕，图像已保存至输出文件夹")
