import cv2
import numpy as np

# 建立一個全黑的畫布 (512x512, 3 通道)
# np.zeros 建立全為 0 的矩陣，dtype=np.uint8 代表 0-255 的整數
canvas = np.zeros((512, 512, 3), dtype=np.uint8)

# 1. 畫線 (Line)
# 參數：(畫布, 起點, 終點, 顏色BGR, 粗細)
cv2.line(canvas, (0, 0), (512, 512), (255, 0, 0), 5)

# 2. 畫矩形 (Rectangle)
# 參數：(畫布, 左上角, 右下角, 顏色BGR, 粗細)
# 粗細設為 -1 表示填滿
cv2.rectangle(canvas, (100, 100), (300, 300), (0, 255, 0), 3)

# 3. 畫圓形 (Circle)
# 參數：(畫布, 圓心, 半徑, 顏色BGR, 粗細)
cv2.circle(canvas, (400, 100), 50, (0, 0, 255), -1)

# 4. 寫文字 (Text)
# 參數：(畫布, 文字, 起點, 字體, 比例, 顏色BGR, 粗細)
cv2.putText(canvas, "OpenCV Drawing", (50, 450), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# 顯示畫布
cv2.imshow("Drawing", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
