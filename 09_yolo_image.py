import cv2
from ultralytics import YOLO

# 1. 載入預訓練的 YOLOv8 模型
# 'yolov8n.pt' 是最輕量級的版本 (nano)，非常適合在一般電腦上快速執行。
# 第一次執行時，程式會自動從網路下載這個模型檔案 (約 6MB)。
print("正在載入 YOLOv8 模型...")
model = YOLO('yolov8n.pt') 

# 2. 讀取要進行辨識的圖片
# 我們使用之前的測試圖片
img_path = 'sample_portrait.jpg'
img = cv2.imread(img_path)

if img is None:
    print(f"找不到圖片：{img_path}，請確認檔案是否存在。")
    exit()

# 3. 進行物件偵測 (Inference)
# 只需要一行程式碼，模型就會找出圖片中所有它認識的物件！
print("正在進行物件偵測...")
results = model(img)

# 4. 解析結果並畫在圖片上
# results 是一個串列 (list)，因為我們只傳入一張圖片，所以取第一個元素 results[0]
# results[0].plot() 會自動把偵測到的邊界框 (Bounding Boxes) 和標籤畫在圖片上
annotated_img = results[0].plot()

# 5. 顯示結果
# 先將圖片縮小以便在螢幕上完整顯示 (可選)
height, width = annotated_img.shape[:2]
resized_img = cv2.resize(annotated_img, (width // 2, height // 2))

cv2.imshow('YOLOv8 Object Detection', resized_img)

print("偵測完成！請查看彈出的視窗。")
print("按下任意鍵關閉視窗...")

# 等待使用者按鍵後關閉視窗
cv2.waitKey(0)
cv2.destroyAllWindows()
