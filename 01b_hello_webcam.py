import cv2

# 1. 建立影像擷取物件
# 參數 0 代表電腦預設的網路攝影機 (Webcam)
cap = cv2.VideoCapture(0)

# 檢查攝影機是否成功開啟
if not cap.isOpened():
    print("錯誤：無法開啟攝影機！")
else:
    print("攝影機已開啟，按下 'q' 鍵退出，按下 's' 鍵存檔...")

    # 2. 使用迴圈不斷讀取畫面
    while True:
        # cap.read() 會傳回兩個值：
        # ret: 是否成功讀取 (True/False)
        # frame: 讀取到的那一影格圖片 (Numpy 矩陣)
        ret, frame = cap.read()

        if not ret:
            print("無法接收影格，正在退出...")
            break

        # 3. 顯示即時畫面
        cv2.imshow("Webcam Live", frame)

        # 4. 偵測按鍵
        # waitKey(1) 表示等待 1 毫秒
        key = cv2.waitKey(1) & 0xFF
        
        # 按下 'q' 鍵退出
        if key == ord('q'):
            break
        
        # 按下 's' 鍵存檔
        elif key == ord('s'):
            cv2.imwrite("captured_image.jpg", frame)
            print("照片已儲存為 captured_image.jpg")

    # 5. 釋放資源
    cap.release()
    cv2.destroyAllWindows()
