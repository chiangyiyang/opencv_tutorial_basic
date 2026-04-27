import cv2
import numpy as np

# 讀取影像
img = cv2.imread("aerial_view.png")

if img is None:
    print("找不到影像檔案！")
else:
    # 取得影像維度
    height, width = img.shape[:2]

    # 1. 定義原始影像中的四個點 (例如：無人機傾斜拍攝到的農田四角)
    # 這裡我們手動定義一組點，模擬傾斜的透視效果
    # 格式: [左上, 右上, 右下, 左下]
    pts1 = np.float32([[200, 300], [800, 200], [900, 800], [100, 700]])

    # 2. 定義校正後的目標點 (正射投射後的矩形座標)
    # 我們希望將上述不規則四邊形轉為 500x500 的正方形
    pts2 = np.float32([[0, 0], [500, 0], [500, 500], [0, 500]])

    # 3. 計算透視變換矩陣 (Perspective Transform Matrix)
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # 4. 執行變換 (Warp Perspective)
    # 這就是製作正射影像 (Orthophoto) 的核心數學步驟
    result = cv2.warpPerspective(img, matrix, (500, 500))

    # 為了方便觀察，在原圖上畫出取樣範圍
    img_draw = img.copy()
    for i in range(4):
        cv2.circle(img_draw, tuple(pts1[i].astype(int)), 10, (0, 0, 255), -1)
    cv2.polylines(img_draw, [pts1.astype(np.int32)], True, (0, 0, 255), 2)

    # 顯示結果
    cv2.imshow("Original with ROIs", img_draw)
    cv2.imshow("Rectified Orthophoto Result", result)

    print("透視變換（正射校正模擬）完成。")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
