import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def load_chinese_font(size=42):
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


def put_chinese_text(img_bgr, text, position, color=(255, 255, 255), font_size=42):
    """Draw Chinese text on a BGR image via Pillow, then convert back to OpenCV format."""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)
    font = load_chinese_font(size=font_size)

    # Pillow uses RGB color order.
    draw.text(position, text, font=font, fill=(color[2], color[1], color[0]))

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


# 建立示範畫布
canvas = np.zeros((500, 900, 3), dtype=np.uint8)

# 畫一個漸層背景，讓中文字更容易看清楚
for y in range(canvas.shape[0]):
    intensity = int(30 + 120 * (y / canvas.shape[0]))
    canvas[y, :, :] = (intensity // 2, intensity, intensity + 40)

cv2.rectangle(canvas, (40, 40), (860, 460), (20, 20, 20), 2)

canvas = put_chinese_text(canvas, "OpenCV 中文顯示範例", (70, 90), (255, 255, 255), 50)
canvas = put_chinese_text(canvas, "課程：電腦視覺入門", (70, 180), (0, 255, 255), 38)
canvas = put_chinese_text(canvas, "說明：cv2.putText 不支援中文", (70, 250), (255, 230, 120), 30)
canvas = put_chinese_text(canvas, "作法：OpenCV + Pillow + TrueType 字型", (70, 305), (255, 230, 120), 30)
canvas = put_chinese_text(canvas, "按任意鍵結束", (70, 390), (180, 255, 180), 34)

cv2.imshow("03b Chinese Text Demo", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()