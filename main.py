import cv2
import multiprocessing as mp
from threading import Thread
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import time

import logging

for _ in ("boto", "elasticsearch", "urllib3", "gensim"):
    logging.getLogger(_).setLevel(logging.CRITICAL)

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class camera:
    def __init__(self, rtsp_url, cam_id, max_frame_queue=20, num_qr_scanner=1):
        self.cam_id = cam_id
        self.rtsp_url = rtsp_url
        self.max_frame_queue= max_frame_queue
        self.frame_queue = mp.Queue()
        self.result = mp.Queue()

        self.start_stream_camera()
        self.init_qr_scanner(num_qr_scanner)

    @staticmethod
    def decode(image):
        gray_img = cv2.cvtColor(image, 0)
        barcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])
        for obj in barcode:
            """DETECT QRCODE"""
            points = obj.polygon
            (x, y, w, h) = obj.rect

            """EXTRACT QRCODE INFO"""
            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            data = [barcodeData, barcodeType, points, x, y]
            logger.info(data)

    def run(self):
        while True:
            try:
                time.sleep(1)
                prevTime = time.time()
                next_frame = self.frame_queue.get()
                self.decode(next_frame)
                ## FPS
                logger.info(f"{self.cam_id} - FPS: {1 / (time.time() - prevTime): .4f}")
            except Exception as ex:
                logger.error(ex)

    def update(self):
        camera_stream = cv2.VideoCapture(self.rtsp_url)
        while True:
            (ret, frame) = camera_stream.read()
            self.frame_queue.put(frame)
            if self.frame_queue.qsize() == self.max_frame_queue:
                self.frame_queue.get()

    def init_qr_scanner(self, num_process):
        for idx in range(num_process):
            logger.info(f"Init QR Scanner {idx} ...")
            p = Thread(target=self.run, args=())
            p.daemon = True
            p.start()

    def start_stream_camera(self):
        Thread(target=self.update, args=()).start()


if __name__ == '__main__':
    cam1 = mp.Process(target=camera, args=("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101",
                                           "CAMERA", 20, 20))
    cam2 = mp.Process(target=camera, args=(0, "WEBCAM", 20, 20))
    cam1.start()
    cam2.start()
    # cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "CAMERA", 20)
    # cam1 = camera(0, "WEBCAM", 20)
