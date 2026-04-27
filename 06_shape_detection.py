import cv2

# 讀取包含各種形狀的圖片
img = cv2.imread("sample_shapes.jpg")

if img is None:
    print("找不到圖片！")
else:
    # 1. 前處理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # 使用門檻值 (Threshold) 轉為二值化影像 (黑白)
    _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)

    # 2. 尋找輪廓
    # RETR_EXTERNAL 只抓最外層的輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # 計算輪廓面積，太小的可能是雜訊，忽略它
        area = cv2.contourArea(cnt)
        if area < 500:
            continue

        # 3. 多邊形逼近 (Polygon Approximation)
        # 它可以簡化輪廓的點數，用來判斷形狀的邊數
        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        # 取得頂點數量
        objCor = len(approx)
        
        # 取得邊界框以便標記文字
        x, y, w, h = cv2.boundingRect(approx)

        # 4. 根據頂點數量判斷形狀
        if objCor == 3:
            objectType = "Triangle"
        elif objCor == 4:
            # 判斷是正方形還是長方形 (長寬比)
            aspRatio = w / float(h)
            if 0.95 < aspRatio < 1.05:
                objectType = "Square"
            else:
                objectType = "Rectangle"
        elif objCor > 4:
            objectType = "Circle"
        else:
            objectType = "None"

        # 5. 繪製輪廓與標籤
        cv2.drawContours(img, [cnt], -1, (255, 0, 0), 2)
        cv2.putText(img, objectType, (x + (w // 2) - 10, y + (h // 2)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # 顯示辨識結果
    cv2.imshow("Shape Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
