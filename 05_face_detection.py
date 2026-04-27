import cv2

# 1. 載入預訓練的人臉分類器 (Haar Cascade)
# cv2.data.haarcascades 提供了內建模型檔案的路徑
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. 開啟 Webcam
cap = cv2.VideoCapture(0)

print("正在啟動人臉偵測，按下 'q' 鍵退出...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. 轉為灰階 (偵測器需要灰階影像)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 4. 偵測人臉
    # scaleFactor: 影像縮放比例，越接近 1 越精確但越慢
    # minNeighbors: 每個目標至少要被偵測到幾次才算成功
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 5. 在人臉位置畫出矩形
    # faces 傳回的是一個清單，每個元素是 (x, y, w, h)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Face Detected", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 6. 顯示結果
    cv2.imshow("Real-time Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
