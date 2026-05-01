# YOLO 客製化模型：資料蒐集、標註與訓練指南

當預先訓練好的 YOLO 模型 (例如能辨識人、車子、貓狗的 `yolov8n.pt`) 無法滿足你的需求時 (例如：你想辨識特定種類的零件、特定的手勢或特定的昆蟲)，你就需要**訓練自己的客製化模型**。

這份指南將帶領你走過訓練客製化模型的完整流程。

---

## 步驟一：資料蒐集 (Data Collection)

深度學習模型是靠「看圖學習」的。你要它認得什麼，就要給它看足夠多該物件的圖片。

### 蒐集原則：
1. **數量要夠**：每個類別至少需要 **100~300 張**圖片作為起步，如果要達到商業應用級別，可能需要數千張。
2. **具備多樣性 (Diversity)**：
   - **不同角度**：正面、側面、背面、俯視。
   - **不同光線**：白天、晚上、室內、室外。
   - **不同背景**：乾淨的背景、雜亂的背景。
   - **不同大小/遮擋**：物件在畫面中忽大忽小，或是被其他東西稍微遮住。
3. **怎麼蒐集？**
   - 使用手機或攝影機自行拍攝（最推薦，最符合實際應用場景）。
   - 從 Google 圖片搜尋下載。
   - 從開源資料集尋找 (例如 Kaggle, Roboflow Universe)。

---

## 步驟二：資料標註 (Data Annotation)

把圖片收集好之後，電腦依然不知道圖片裡哪個東西是你要的。我們必須人工把目標「框出來」，並告訴電腦「這是什麼」，這個過程稱為標註 (Annotation / Labeling)。

### 推薦標註工具：

#### 1. Roboflow (強烈推薦，最適合新手)
* **網址**：[https://roboflow.com/](https://roboflow.com/)
* **優點**：完全在雲端網頁上操作，介面直觀，支援團隊協作，而且可以**一鍵匯出 YOLOv8 格式**。
* **流程**：
  1. 註冊帳號並建立 Project (選擇 Object Detection)。
  2. 上傳你的圖片。
  3. 使用滑鼠在圖片上畫框 (Bounding Box)，並輸入類別名稱 (例如：`apple`, `banana`)。
  4. 點擊 Generate 產生資料集，匯出時選擇 **YOLOv8** 格式。

#### 2. MakeSense.ai (免註冊的輕量級選擇)
* **網址**：[https://www.makesense.ai/](https://www.makesense.ai/)
* **優點**：不用註冊帳號，打開網頁就能畫，資料不會上傳到雲端 (注重隱私)。
* **缺點**：如果關閉瀏覽器，未匯出的進度可能會消失。匯出時需選擇 YOLO 格式。

#### 3. LabelImg (傳統本機端軟體)
* 需要透過 Python 安裝 (`pip install labelImg`)，介面較老舊，目前較少推薦給新手，但依然是非常經典的本機端工具。

### YOLO 的標註檔案格式
YOLO 要求的標註格式是一張圖片對應一個同名的 `.txt` 檔案。
例如 `image_01.jpg` 必須有一個 `image_01.txt`。
TXT 檔內的每一行代表一個被框出來的物件，格式為：
`<類別ID> <中心點X> <中心點Y> <寬度W> <高度H>` (數值皆為 0~1 之間的比例)。

---

## 步驟三：準備資料集結構與設定檔 (data.yaml)

如果你使用 Roboflow 匯出資料集，它會自動幫你建好以下結構。如果你是手動整理，請確保資料夾長這樣：

```text
my_dataset/
├── train/          # 訓練集 (佔總資料約 80%)
│   ├── images/     # 存放 .jpg 圖片
│   └── labels/     # 存放 .txt 標註檔
├── val/            # 驗證集 (佔總資料約 20%，用於訓練中途的測驗)
│   ├── images/
│   └── labels/
└── data.yaml       # 告訴 YOLO 你的資料在哪裡的重要設定檔
```

### `data.yaml` 檔案內容範例：
你需要建立一個名為 `data.yaml` 的檔案，內容如下：

```yaml
# 指定 train 和 val 資料夾的絕對路徑或相對路徑
train: ./train/images
val: ./val/images

# 類別數量
nc: 2

# 類別名稱 (順序必須與你標註時的 ID 對應，0 代表 apple, 1 代表 banana)
names: ['apple', 'banana']
```

---

## 步驟四：開始訓練 (Training)

在 YOLOv8 (Ultralytics 套件) 中，訓練模型非常簡單，甚至不需要寫複雜的 Python 程式碼，直接在終端機 (Terminal) 輸入指令即可！

請確保你已經啟動了虛擬環境，並且安裝了 `ultralytics` (`pip install ultralytics`)。

在終端機輸入以下指令開始訓練：

```bash
yolo task=detect mode=train data=my_dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640
```

### 指令參數說明：
* **`task=detect`**：執行的任務是物件偵測。
* **`mode=train`**：我們現在要「訓練」模型。
* **`data=...`**：指向你剛才建立的 `data.yaml` 檔案路徑。
* **`model=yolov8n.pt`**：我們基於最輕量的 YOLOv8n 模型來進行「遷移學習」(Transfer Learning)，這會比從零開始學快非常多。
* **`epochs=50`**：訓練的回合數。模型會把所有圖片看過 50 遍。如果發現模型還沒學好，可以增加到 100 或 200。
* **`imgsz=640`**：訓練時會將圖片縮放成 640x640。

> [!TIP]
> **使用 GPU 加速訓練**
> 如果你的電腦有 NVIDIA 顯示卡，訓練速度會比單純用 CPU 快上數十倍！
> 要啟用 GPU，你需要安裝適合你顯示卡的 CUDA 版本的 PyTorch。對於初學者，我們也強烈建議使用 **Google Colab** (免費提供雲端 GPU) 來進行訓練，訓練完再把模型下載到自己電腦上使用。

---

## 步驟五：驗收成果與使用模型

訓練開始後，YOLO 會在目錄下自動產生一個名為 `runs/detect/train/` 的資料夾。

1. **查看訓練過程**：在該資料夾中，你可以找到許多圖表（如 `results.png`），它們記錄了模型的準確率是如何隨著 epochs 提升的。
2. **取得最佳模型**：訓練完成後，你可以在 `runs/detect/train/weights/` 目錄下找到兩個檔案：
   * `last.pt` (最後一個 epoch 的權重)
   * **`best.pt` (訓練過程中表現最好的一次權重) <- 我們通常使用這個！**

### 如何把訓練好的模型放到 Python 中使用？

非常簡單！只需要把原本程式碼中的 `yolov8n.pt` 換成你訓練出來的 `best.pt` 的路徑即可。

修改 `09b_yolo_webcam.py` (或是圖片偵測版)：

```python
import cv2
from ultralytics import YOLO

# 載入你剛訓練好的【客製化模型】
# 假設你把 best.pt 複製到了專案目錄下
model = YOLO('best.pt') 

# ... 下面的程式碼完全一樣 ...
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow('My Custom Model', annotated_frame)
    if cv2.waitKey(1) == ord('q'):
        break
# ...
```

恭喜！你現在已經具備從頭到尾打造專屬 AI 視覺模型的能力了！
