import cv2

img = cv2.imread("sample_portrait.jpg")

if img is None:
    print("找不到圖片！")
else:
    # 1. 高斯模糊 (Gaussian Blur)
    # 常用於去除影像雜訊
    # ksize 必須是奇數，如 (7, 7)
    img_blur = cv2.GaussianBlur(img, (15, 15), 0)

    # 2. Canny 邊緣偵測 (Canny Edge Detection)
    # 參數：(影像, 門檻1, 門檻2)
    # 門檻值決定了對邊緣的敏感度
    img_edges = cv2.Canny(img, 100, 200)

    # 顯示結果
    cv2.imshow("Original", img)
    cv2.imshow("Blurred", img_blur)
    cv2.imshow("Edges", img_edges)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
