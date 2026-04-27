# OpenCV 測繪與空間資訊進階教學

這份文件針對測繪與空間資訊系所（Surveying and Geomatics）的學生，解釋如何利用 OpenCV 處理遙測影像與幾何校正。

---

## 🛰️ 07_ndvi_simulation.py - 真實衛星波段運算 (NDVI)
在遙測領域，我們直接操作衛星感測器回傳的特定光譜波段。

*   **Sentinel-2 衛星資料**：
    *   **B04 (Red)**：紅光波段，會被植物葉綠素強烈吸收。
    *   **B08 (NIR)**：近紅外光波段，會被植物葉肉組織強烈反射。
*   **真實波段運算 (Real Band Math)**：
    *   本範例讀取 `bands` 目錄下的真實衛星影像檔。
    *   **公式**：`NDVI = (B08 - B04) / (B08 + B04)`。
    *   這是一個標準的矩陣運算流程，展現了 OpenCV 處理科學數據的能力。
*   **結果解讀 (JET 色譜)**：
    *   **紅色 (High Value)**：NDVI 接近 1，代表植生最茂盛的區域。
    *   **黃色/綠色 (Mid Value)**：代表一般植生或混合地表。
    *   **藍色 (Low Value)**：NDVI 接近 0 或負值，代表水體、裸地或人工建物。此外，JET 色譜的強烈對比有助於快速識別地物差異。

---

## 🗺️ 08_ortho_rectification.py - 正射校正與透視變換
航拍影像往往因為相機角度產生透視變形。為了測量真實距離，我們需要進行校正。

*   **透視變換 (Perspective Transform)**：
    *   這是將影像從一個座標系映射到另一個座標系的過程。
    *   `cv2.getPerspectiveTransform(pts1, pts2)`：計算變換矩陣。在攝影測量中，這相當於已知地面控制點 (GCP) 來解求影像的外方位元素。
*   **影像糾正 (Image Rectification)**：
    *   `cv2.warpPerspective`：利用計算出的矩陣，將傾斜的照片「拉正」。
    *   這是在製作 **正射影像 (Orthophoto)** 或進行建築物立面校正時的核心技術。

---

## 🛠️ 專業術語對照
*   **Raster (網格)** = OpenCV 中的 `Numpy Array`
*   **Band (波段)** = OpenCV 中的 `Channel`
*   **GCP (地面控制點)** = `pts1` 中的標記點
*   **Rectification (糾正)** = `Warping`

希望這些範例能幫助你將 OpenCV 應用在測繪專業領域！
