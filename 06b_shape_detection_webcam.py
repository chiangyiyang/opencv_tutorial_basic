import cv2

# 1. 建立影像擷取物件
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("錯誤：無法開啟攝影機！")
else:
    print("即時形狀辨識中，按下 'q' 鍵退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- 形狀辨識邏輯開始 ---
        
        # 1. 前處理
        # 複製一份影像用來處理，避免影響原始 frame 的顯示（如果需要原始畫面的話）
        imgContour = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 1)
        # 在即時環境中，Canny 邊緣偵測通常比固定門檻值更穩定
        canny = cv2.Canny(blur, 50, 150)

        # 2. 尋找輪廓
        contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            # 過濾太小的雜訊
            if area < 1000:
                continue

            # 3. 多邊形逼近
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            # 4. 判斷形狀
            if objCor == 3:
                objectType = "Triangle"
            elif objCor == 4:
                aspRatio = w / float(h)
                if 0.95 < aspRatio < 1.05:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4:
                objectType = "Circle"
            else:
                objectType = "None"

            # 5. 繪製結果
            cv2.drawContours(imgContour, [cnt], -1, (0, 255, 0), 2)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(imgContour, objectType, (x, y - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # --- 形狀辨識邏輯結束 ---

        # 顯示結果
        cv2.imshow("Webcam Shape Detection", imgContour)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
