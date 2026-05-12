import argparse
import time

import cv2
from ultralytics import YOLOE


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLOE YouTube 影片物件偵測 - 開放詞彙自然語言查詢"
    )
    parser.add_argument(
        "--model",
        default="yoloe-26s-seg.pt",
        help="YOLOE 模型版本。支援: yoloe-26n-seg.pt, yoloe-26s-seg.pt, yoloe-26m-seg.pt, yoloe-26l-seg.pt, yoloe-26x-seg.pt",
    )
    parser.add_argument(
        "--source",
        default="https://www.youtube.com/watch?v=zm7sr9CpxPw",
        help="YouTube 網址",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="person wearing a red hat",
        help=(
            "自然語言目標描述。支援開放詞彙：\n"
            "  - 單一物體: 'person', 'dog', 'car'\n"
            "  - 複雜描述: 'person wearing a red hat', 'person with sunglasses'\n"
            "  - 多個目標: 'person', 'bicycle', 'car' (分開執行)"
        ),
    )
    parser.add_argument("--conf", type=float, default=0.25, help="YOLOE 最低信心分數門檻")
    parser.add_argument("--imgsz", type=int, default=640, help="推論尺寸")
    return parser.parse_args()


def resolve_source(source: str) -> str:
    """解析 YouTube URL 或直接返回影片來源"""
    if "youtube.com" not in source and "youtu.be" not in source:
        return source

    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        raise RuntimeError("偵測到 YouTube 網址，但未安裝 yt-dlp。請先安裝 requirements.txt。")

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download=False)
        stream_url = info.get("url")

    if not stream_url:
        raise RuntimeError("無法解析 YouTube 串流網址，請更換來源。")

    return stream_url


def main():
    args = parse_args()
    target_classes = [t.strip() for t in args.target.split(",") if t.strip()]
    if not target_classes:
        target_classes = ["person"]

    print("=" * 70)
    print("YOLOE YouTube 影片物件偵測 - 開放詞彙自然語言查詢")
    print("=" * 70)

    # 載入 YOLOE 模型（會自動下載）
    print(f"正在載入 YOLOE 模型：{args.model}")
    try:
        model = YOLOE(args.model)
        # 依官方建議先設定提示詞，再執行 predict
        model.set_classes(target_classes)
    except Exception as e:
        print(f"❌ 載入模型失敗：{e}")
        print("提示：確保已安裝 ultralytics，可執行 pip install ultralytics")
        return

    # 解析 YouTube 連結
    print(f"正在解析 YouTube 連結...")
    try:
        source = resolve_source(args.source)
    except RuntimeError as e:
        print(f"❌ {e}")
        return

    # 開啟影片來源
    print(f"正在開啟影片...")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("❌ 無法開啟影片來源，請確認 URL 可用或網路狀態。")
        return

    print("✓ 影片已開啟")
    print(f"✓ 搜尋目標：{', '.join(target_classes)}")
    print("\n操作說明：")
    print("  Q 鍵     - 退出程式")
    print("  S 鍵     - 儲存目前畫面")
    print(f"  信心度   - {args.conf}")
    print("-" * 70)

    prev_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("影片播放結束或讀取失敗。")
            break

        frame_count += 1

        # 使用 YOLOE 進行開放詞彙物件偵測
        try:
            results = model.predict(
                source=frame,
                conf=args.conf,
                imgsz=args.imgsz,
                verbose=False
            )
        except Exception as e:
            print(f"偵測時出錯：{e}")
            break

        # 繪製結果
        if results and len(results) > 0:
            annotated = results[0].plot()
        else:
            annotated = frame.copy()

        # 計算 FPS
        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-6)
        prev_time = curr_time

        # 顯示 FPS
        cv2.putText(
            annotated,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

        # 顯示搜尋目標
        cv2.putText(
            annotated,
            f"Search: {', '.join(target_classes)}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # 顯示偵測到的物體數量
        num_detections = 0
        if results and len(results) > 0 and results[0].boxes:
            num_detections = len(results[0].boxes)
        
        cv2.putText(
            annotated,
            f"Number: {num_detections}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("YOLOE YouTube 物件偵測", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n使用者中斷程式。")
            break
        if key == ord("s"):
            filename = f"yoloe_youtube_capture_{int(time.time())}.jpg"
            cv2.imwrite(filename, annotated)
            print(f"✓ 已儲存：{filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("程式已結束。")


if __name__ == "__main__":
    main()
