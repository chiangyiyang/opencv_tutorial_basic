import cv2
from ultralytics import YOLO

# 1. 載入預訓練的 YOLOv8 模型
print("正在載入 YOLOv8 模型...")
model = YOLO('yolov8n.pt') 

# 2. 開啟網路攝影機
# 參數 0 通常代表筆電內建的攝影機
print("正在啟動攝影機...")
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("無法開啟攝影機，請確認設備連接。")
    exit()

print("按下 'q' 鍵可以結束程式。")

# 3. 進入無限迴圈，不斷讀取攝影機畫面並進行偵測
while True:
    # 讀取一張畫面
    ret, frame = cap.read()
    
    # 如果讀取失敗，就跳出迴圈
    if not ret:
        print("無法取得畫面。")
        break

    # 4. 進行物件偵測 (Inference)
    # 為了保持畫面流暢，我們可以設定 verbose=False 來隱藏終端機的推論文字輸出
    results = model(frame, verbose=False)

    # 5. 解析結果並畫在畫面上
    # 使用 plot() 將框框畫在當前影格上
    annotated_frame = results[0].plot()

    # 6. 顯示結果
    cv2.imshow('YOLOv8 Real-time Object Detection', annotated_frame)

    # 7. 等待按鍵
    # 等待 1 毫秒，如果使用者按下 'q' 則跳出迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("使用者中斷程式。")
        break

# 釋放攝影機資源並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
