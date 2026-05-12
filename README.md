# OpenCV 影像處理入門教學

歡迎來到 OpenCV (Open Source Computer Vision Library) 的世界！這份教學將帶領你一步步掌握電腦視覺的基礎。

## 1. 環境安裝與虛擬環境 (Virtual Environment)

為了保持電腦環境整潔，建議為此專案建立一個獨立的「虛擬環境」。請按照以下步驟操作：

### Step A: 建立虛擬環境

在專案目錄下開啟終端機 (Terminal)，輸入：

```bash
python -m venv venv
```

### Step B: 啟動虛擬環境

* **Windows (PowerShell/CMD):**
  ```bash
  .\venv\Scripts\activate
  ```
* **Windows (Git Bash):**
  ```bash
  source venv/Scripts/activate
  ```
* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

啟動成功後，你的終端機提示字元前面應該會出現 `(venv)` 字樣。

### Step C: 安裝 OpenCV 與所需套件

在啟動虛擬環境的狀態下，執行：

```bash
pip install -r requirements.txt
```

這會自動安裝 `opencv-python`、處理矩陣運算用的 `numpy`，以及顯示中文字會用到的 `Pillow`。

## 2. 學習目錄

本教學分為以下幾個章節：

* **[01_hello_image.py](file:///d:/Projects/CCIT/opencv_tutorial/01_hello_image.py)**: 學習如何讀取並顯示一張圖片。
* **[01b_hello_webcam.py](file:///d:/Projects/CCIT/opencv_tutorial/01b_hello_webcam.py)**: 學習如何開啟 Webcam 並讀取即時畫面。
* **[02_image_basics.py](file:///d:/Projects/CCIT/opencv_tutorial/02_image_basics.py)**: 影像的基本操作，包括轉灰階、縮放與裁剪。
* **[03_drawing.py](file:///d:/Projects/CCIT/opencv_tutorial/03_drawing.py)**: 在圖片上畫線、畫圓、寫字，這對於標註偵測結果非常重要。
* **[03b_chinese_text.py](file:///d:/Projects/CCIT/opencv_tutorial/03b_chinese_text.py)**: 如何在 OpenCV 畫面上顯示「中文字」。
* **[03c_chinese_text_webcam.py](file:///d:/Projects/CCIT/opencv_tutorial/03c_chinese_text_webcam.py)**: 在即時 Webcam 畫面上疊加中文字、FPS 與操作提示。
* **[04_filters_edges.py](file:///d:/Projects/CCIT/opencv_tutorial/04_filters_edges.py)**: 影像濾波（模糊）與邊緣偵測。
* **[05_face_detection.py](file:///d:/Projects/CCIT/opencv_tutorial/05_face_detection.py)**: **專題一**：實現即時人臉偵測系統。
* **[06_shape_detection.py](file:///d:/Projects/CCIT/opencv_tutorial/06_shape_detection.py)**: **專題二**：自動辨識圖片中的幾何圖形。
* **[09_yolo_image.py](file:///d:/Projects/CCIT/opencv_tutorial/09_yolo_image.py)**: **進階專題三**：使用 YOLOv8 進行深度學習物件偵測 (圖片篇)。
* **[09b_yolo_webcam.py](file:///d:/Projects/CCIT/opencv_tutorial/09b_yolo_webcam.py)**: **進階專題三**：使用 YOLOv8 進行深度學習物件偵測 (即時影像篇)。
* **[09c_yolo26_webcam.py](file:///d:/Projects/CCIT/opencv_tutorial_basic/09c_yolo26_webcam.py)**: **進階專題四**：使用 YOLO26 進行 Webcam 即時物件偵測（含 FPS 與快照儲存）。
* **[09d_yolo26_online_video.py](file:///d:/Projects/CCIT/opencv_tutorial_basic/09d_yolo26_online_video.py)**: **進階專題五**：使用 YOLO26 讀取網路影片來源（含 YouTube）進行即時偵測。
* **[yolo_custom_training_guide.md](file:///d:/Projects/CCIT/opencv_tutorial/yolo_custom_training_guide.md)**: **加碼教學**：如何蒐集資料、標註並訓練專屬於你自己的 YOLO 模型！

詳細的程式碼原理解析請參考：**[範例程式詳解 (tutorial_guide.md)](file:///d:/Projects/CCIT/opencv_tutorial/tutorial_guide.md)**

## 3. 準備素材

本目錄下已準備了兩個測試素材：

- `sample_portrait.jpg`: 用於人臉偵測。
- `sample_shapes.jpg`: 用於圖形辨識。

## 4. 如何使用

你可以按照數字順序，逐一打開 `.py` 檔案閱讀註解並執行程式。建議你自己動手修改程式碼中的參數，看看會有什麼變化！

---

祝學習愉快！
