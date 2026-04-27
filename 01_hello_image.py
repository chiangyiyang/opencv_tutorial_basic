import cv2

# 1. 讀取影像
# 使用 cv2.imread() 函數讀取圖片檔案
# 路徑可以改為你自己的圖片路徑
img = cv2.imread("sample_portrait.jpg")

# 檢查圖片是否讀取成功
if img is None:
    print("錯誤：找不到圖片檔案！")
else:
    # 2. 顯示影像
    # 第一個參數是視窗名稱，第二個參數是要顯示的影像變數
    cv2.imshow("Hello OpenCV!", img)

    # 3. 等待按鍵
    # cv2.waitKey(0) 會暫停程式，直到你按下鍵盤上的任意鍵
    # 如果不加這一行，視窗會一閃而過
    print("按下任意鍵關閉視窗...")
    cv2.waitKey(0)

    # 4. 關閉所有視窗
    cv2.destroyAllWindows()
