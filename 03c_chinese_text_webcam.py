import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def load_chinese_font(size=32):
    """Try common Windows CJK fonts and return the first available one."""
    font_candidates = [
        "C:/Windows/Fonts/msjh.ttc",      # Microsoft JhengHei
        "C:/Windows/Fonts/msjhbd.ttc",    # Microsoft JhengHei Bold
        "C:/Windows/Fonts/msyh.ttc",      # Microsoft YaHei
        "C:/Windows/Fonts/simhei.ttf",    # SimHei
    ]

    for font_path in font_candidates:
        try:
            return ImageFont.truetype(font_path, size=size)
        except OSError:
            continue

    raise FileNotFoundError(
        "找不到可用的中文字型。請安裝微軟正黑體，或修改程式中的字型路徑。"
    )


def put_chinese_text(img_bgr, text, position, color=(255, 255, 255), font_size=32):
    """Draw Chinese text on a BGR image via Pillow, then convert back to OpenCV format."""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)
    font = load_chinese_font(size=font_size)

    # Pillow uses RGB color order.
    draw.text(position, text, font=font, fill=(color[2], color[1], color[0]))

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("無法開啟 Webcam，請確認攝影機是否被其他程式占用。")

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像，程式結束。")
        break

    now = time.time()
    fps = 1.0 / max(now - prev_time, 1e-6)
    prev_time = now

    # 半透明資訊框，避免文字被背景吃掉
    overlay = frame.copy()
    cv2.rectangle(overlay, (15, 15), (650, 155), (20, 20, 20), -1)
    frame = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)

    frame = put_chinese_text(frame, "即時 Webcam 中文疊加範例", (30, 30), (255, 255, 255), 34)
    frame = put_chinese_text(frame, "按 Q 離開，按 S 儲存截圖", (30, 75), (160, 255, 255), 28)
    frame = put_chinese_text(frame, f"目前 FPS: {fps:.1f}", (30, 115), (180, 255, 180), 28)

    cv2.imshow("03c Chinese Text Webcam", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
        filename = f"webcam_chinese_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"已儲存: {filename}")

cap.release()
cv2.destroyAllWindows()