import argparse
import time

import cv2
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLO26 Webcam 即時物件偵測教案"
    )
    parser.add_argument(
        "--model",
        default="yolo26n.pt",
        help="模型權重路徑，預設為 yolo26n.pt（若本機沒有會自動下載）",
    )
    parser.add_argument("--camera", type=int, default=0, help="攝影機編號，預設 0")
    parser.add_argument(
        "--conf", type=float, default=0.35, help="最低信心分數門檻，預設 0.35"
    )
    parser.add_argument(
        "--imgsz", type=int, default=640, help="推論尺寸，預設 640"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"正在載入 YOLO26 模型：{args.model}")
    model = YOLO(args.model)

    print(f"正在啟動攝影機（index={args.camera}）...")
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("無法開啟攝影機，請檢查 camera index 或設備連接。")
        return

    print("按 Q 離開，按 S 儲存目前畫面。")

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法取得畫面，程式結束。")
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

        cv2.imshow("YOLO26 Webcam Detection", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("使用者中斷程式。")
            break
        if key == ord("s"):
            filename = f"yolo26_capture_{int(time.time())}.jpg"
            cv2.imwrite(filename, annotated)
            print(f"已儲存：{filename}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
