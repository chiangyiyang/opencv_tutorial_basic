import argparse
import time

import cv2
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLO26 網路影片來源即時物件偵測（支援 YouTube）"
    )
    parser.add_argument("--model", default="yolo26n.pt", help="模型權重路徑")
    parser.add_argument(
        "--source",
        default="https://www.youtube.com/watch?v=LNwODJXcvt4",
        help="影片來源，可為 MP4 連結、串流 URL 或 YouTube 網址",
    )
    parser.add_argument("--conf", type=float, default=0.35, help="最低信心分數門檻")
    parser.add_argument("--imgsz", type=int, default=640, help="推論尺寸")
    return parser.parse_args()


def resolve_source(source: str) -> str:
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

    print(f"正在載入 YOLO26 模型：{args.model}")
    model = YOLO(args.model)

    try:
        source = resolve_source(args.source)
    except RuntimeError as e:
        print(e)
        return

    print(f"正在開啟來源：{args.source}")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("無法開啟影片來源，請確認 URL 可用或網路狀態。")
        return

    print("按 Q 離開，按 S 儲存目前畫面。")
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("影片播放結束或讀取失敗。")
            break

        results = model(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)
        annotated = results[0].plot()

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-6)
        prev_time = curr_time

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

        cv2.imshow("YOLO26 Online Video Detection", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("使用者中斷程式。")
            break
        if key == ord("s"):
            filename = f"yolo26_online_capture_{int(time.time())}.jpg"
            cv2.imwrite(filename, annotated)
            print(f"已儲存：{filename}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
