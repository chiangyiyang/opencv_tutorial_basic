import cv2
import numpy as np
import os

# 1. 設定路徑
base_path = "bands"
red_file = "2026-04-14-00_00_2026-04-14-23_59_Sentinel-2_L2A_B04_(Raw).png"
nir_file = "2026-04-14-00_00_2026-04-14-23_59_Sentinel-2_L2A_B08_(Raw).png"

# 2. 讀取真實衛星波段 (Sentinel-2)
# B04 是紅光 (Red), B08 是近紅外光 (NIR)
red_img = cv2.imread(os.path.join(base_path, red_file), cv2.IMREAD_GRAYSCALE)
nir_img = cv2.imread(os.path.join(base_path, nir_file), cv2.IMREAD_GRAYSCALE)

if red_img is None or nir_img is None:
    print("找不到衛星波段影像檔案！請確認 bands 目錄下的檔名。")
else:
    # 3. 轉換資料型態為 float 以進行精確運算
    red = red_img.astype(float)
    nir = nir_img.astype(float)

    # 4. 計算標準 NDVI (Normalized Difference Vegetation Index)
    # 公式: (NIR - Red) / (NIR + Red)
    denominator = nir + red
    denominator[denominator == 0] = 0.01  # 防止除以零
    
    ndvi = (nir - red) / denominator

    # 5. 視覺化處理
    # 將 NDVI (-1 到 1) 映射到 0-255 以利顯示
    ndvi_display = ((ndvi + 1.0) / 2.0 * 255).astype(np.uint8)

    # 使用 COLORMAP_SUMMER 或 COLORMAP_JET，前者對植生較直觀（綠色調）
    ndvi_color = cv2.applyColorMap(ndvi_display, cv2.COLORMAP_JET)

    # 6. 顯示結果
    cv2.imshow("Red Band (B04)", red_img)
    cv2.imshow("NIR Band (B08)", nir_img)
    cv2.imshow("Calculated NDVI (Sentinel-2)", ndvi_color)

    print("NDVI 真實衛星資料計算完成。")
    print(f"影像尺寸: {red_img.shape}")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
