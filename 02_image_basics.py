import cv2

# 讀取原始圖片
img = cv2.imread("sample_portrait.jpg")

if img is None:
    print("找不到圖片！")
else:
    # 1. 影像屬性
    # shape 傳回 (高, 寬, 通道數)
    h, w, c = img.shape
    print(f"圖片大小: {w}x{h}, 通道數: {c}")

    # 2. 轉為灰階 (Grayscale)
    # 許多影像處理演算法在灰階下執行更快、更準確
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 調整大小 (Resize)
    # 指定新的寬度與高度
    img_resized = cv2.resize(img, (400, 300))

    # 4. 裁剪 (Crop)
    # 利用 Numpy 的切片功能：[y開始:y結束, x開始:x結束]
    # 例如擷取中間的一部分
    img_cropped = img[50:250, 100:300]

    # 顯示所有結果
    cv2.imshow("Original", img)
    cv2.imshow("Gray", img_gray)
    cv2.imshow("Resized", img_resized)
    cv2.imshow("Cropped", img_cropped)

    print("按下任意鍵關閉...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
