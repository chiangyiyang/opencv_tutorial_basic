# OpenCV 範例程式詳解

這份文件為每個教學範例提供詳細的說明，幫助你理解每一行程式碼背後的原理。

---

## 🖼️ 01_hello_image.py - 讀取與顯示圖片

這是 OpenCV 的第一個練習，學習如何讓電腦「看見」圖片。

* **`cv2.imread(路徑)`**: 將圖片從硬碟載入到記憶體中。
* **`cv2.imshow(標題, 影像)`**: 彈出視窗顯示影像。
* **`cv2.waitKey(0)`**: 這是最重要的步驟。它會讓程式停在這一行，直到你按下鍵盤按鍵。如果沒有這行，視窗會瞬間出現又消失。

---

## 📹 01b_hello_webcam.py - 讀取網路攝影機

學習如何處理「動態」的影像串流，並進行拍照存檔。

* **`cv2.VideoCapture(0)`**: 初始化攝影機。數字 `0` 通常代表筆電內建攝影機。
* **`while True` 迴圈**: 影片其實就是一連串快速播放的圖片。我們使用無限迴圈來不斷抓取最新的影像。
* **`cap.read()`**: 傳回 `ret` (成功與否) 與 `frame` (當下的圖片)。
* **`cv2.waitKey(1)`**: 在迴圈中，我們等待按鍵輸入。除了用來控制流暢度，也能捕捉特定按鍵（如 's'）來執行動作。
* **`cv2.imwrite(檔名, 影像)`**: 將當前的影格（frame）儲存為圖檔。這就是實現「拍照」功能的核心。

---

## 🎨 02_image_basics.py - 影像基礎轉換

學習如何修改圖片的尺寸與色彩。

* **`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`**: 電腦處理彩色圖片需要很大運算量。轉成「灰階」可以簡化資訊，讓後續的辨識更快。
* **`cv2.resize(img, (寬, 高))`**: 調整解析度。
* **`img[y1:y2, x1:x2]`**: 這是利用 Python 的「切片」功能。就像在報紙上剪下感興趣的區域 (ROI, Region of Interest)。

---

## ✏️ 03_drawing.py - 影像繪圖標記

在圖片上畫框框或寫字，是標註 AI 偵測結果的基本功。

* **`np.zeros((512, 512, 3), dtype=np.uint8)`**: 建立一張全黑的空白畫布。
* **顏色 (B, G, R)**: 注意 OpenCV 的顏色順序是 **藍、綠、紅**，不是常見的 RGB。
* **`cv2.putText`**: 可以在畫面上即時顯示狀態或偵測結果。

---

## 🈶 03b_chinese_text.py - 在畫面顯示中文字

`cv2.putText` 內建字型無法正確顯示中文，本範例示範實務常見解法：OpenCV + Pillow。

* **核心觀念**：先把 OpenCV 的 BGR 影像轉成 Pillow 可處理的 RGB 影像。
* **`ImageFont.truetype`**：載入系統中文字型（例如微軟正黑體）。
* **`ImageDraw.text`**：在 Pillow 影像上寫入中文，再轉回 OpenCV 顯示。
* **字型路徑**：Windows 常見可用路徑為 `C:/Windows/Fonts/msjh.ttc`。

---

## 📹 03c_chinese_text_webcam.py - 即時 Webcam 中文疊加

把 03b 的中文顯示方法延伸到即時影像串流，常用於教學、監控畫面資訊疊加與展示用途。

* **即時串流**：透過 `cv2.VideoCapture(0)` 連續讀取 Webcam 畫面。
* **中文覆蓋**：每個 frame 都先畫半透明底板，再用 Pillow 疊加中文，提升可讀性。
* **效能觀察**：顯示當前 FPS，方便觀察文字疊加後的效能變化。
* **快捷鍵**：按 `S` 儲存當前畫面，按 `Q` 結束程式。

---

## 🌫️ 04_filters_edges.py - 濾波與邊緣偵測

學習如何去除雜訊並抓取輪廓。

* **`cv2.GaussianBlur`**: 讓影像變模糊。這在處理品質不佳的監視器畫面時非常有用，可以過濾掉不必要的「雜點」。
* **`cv2.Canny`**: 電腦視覺中最經典的邊緣偵測演算法。它會找出影像中顏色變化最劇烈的地方，繪製成白線。

---

## 👤 05_face_detection.py - 即時人臉偵測

這是你的第一個電腦視覺小專案！

* **Haar Cascades**: 這是一種基於特徵的分類器。它已經學會了人臉具備的特徵（例如：眼睛區域比鼻樑暗）。
* **`detectMultiScale`**: 會在影像中搜尋不同大小的人臉。
* **整合應用**: 我們將讀取 Webcam、轉灰階、偵測、畫框這四個步驟結合在迴圈中，實現即時偵測。

---

## 🔺 06_shape_detection.py - 圖形辨識

學習如何讓電腦區分圓形、三角形與正方形。

* **`cv2.threshold`**: 將影像轉為純黑白（二值化），方便找輪廓。
* **`cv2.findContours`**: 找出影像中所有獨立物體的邊界。
* **`cv2.approxPolyDP`**: 多邊形逼近。透過計算「頂點數量」來判斷形狀。
  * 3 個頂點 = 三角形
  * 4 個頂點 = 正方形/長方形
  * 更多頂點 = 圓形

---

## 🎥 06b_shape_detection_webcam.py - 即時圖形辨識

將圖形辨識技術應用在即時影像串流中。

* **`cv2.Canny`**: 在即時環境中，使用 Canny 邊緣偵測通常比簡單的門檻值 (Threshold) 更能適應不同的光影變化。
* **動態處理**: 結合了 `VideoCapture` 迴圈與圖形辨識邏輯，實現即時的 AI 偵測效果。
* **效能優化**: 在迴圈中加入了面積過濾 (`area < 1000`)，以確保程式不會被微小的背景雜訊干擾。

---

## 🚀 09_yolo_image.py - YOLO 深度學習物件偵測 (圖片)

帶領學生進入強大的深度學習領域，使用業界最流行的 YOLO (You Only Look Once) 模型。

* **`from ultralytics import YOLO`**: 我們使用 `ultralytics` 套件，它把複雜的神經網路操作簡化成了幾行程式碼。
* **`model = YOLO('yolov8n.pt')`**: 載入 YOLOv8 的 nano 版本。這是最輕量、最快的版本，非常適合在沒有高級顯示卡的筆電上執行。程式會自動下載模型檔案。
* **`results = model(img)`**: 進行推論 (Inference)。這短短一行，模型就完成了尋找特徵、分類和計算位置等複雜的工作。
* **`results[0].plot()`**: 這是 `ultralytics` 提供的超方便功能，它會自動把偵測到的物件框框 (Bounding Box)、信心分數 (Confidence) 和類別名稱畫在圖片上。

---

## 📹 09b_yolo_webcam.py - YOLO 即時物件偵測

將強大的 YOLO 模型結合到 Webcam 串流中，打造真正的即時 AI 應用！

* **即時推論**: 我們把 `model(frame)` 放入無限迴圈中。由於 `yolov8n.pt` 夠輕量，一般筆電的 CPU 也能達到每秒數幀 (fps) 的偵測速度。
* **`verbose=False`**: 在迴圈中不斷推論會產生大量的終端機輸出。將 `verbose` 設為 `False` 可以讓終端機畫面保持乾淨。
* **結合所學**: 這個範例完美結合了 `01b_hello_webcam.py` (讀取串流) 和 `09_yolo_image.py` (模型推論) 的核心概念。

---
## 🗺️ 測繪與空間資訊進階教學
如果你對地理資訊 (GIS) 或遙測 (Remote Sensing) 有興趣，可以查看專屬教學：
*   **[tutorial_guide_geomatics.md](file:///d:/Projects/CCIT/opencv_tutorial/tutorial_guide_geomatics.md)**：包含 NDVI 衛星影像運算與正射校正原理。

---
希望這些說明能讓你更深入了解 OpenCV 的運作方式！
