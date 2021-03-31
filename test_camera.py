import cv2
import multiprocessing as mp
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import time
from multi_qr_scanner import QR_Scanner

from utils.logger import get_logger
logger = get_logger('Init Camera')
import sys

class camera():
	def __init__(self, rtsp_url, id, num_process=1):
		self.id = id
		self.rtsp_url = rtsp_url

		self.task = mp.Queue()
		self.result = mp.Queue()

		self.start_stream_camera()
		self.init_qr_scanner(num_process)

	@staticmethod
	def decode(image):
		gray_img = cv2.cvtColor(image, 0)
		barcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])
		try:
			for obj in barcode:
				"""EXTRACT QRCODE INFO"""
				barcodeData = obj.data.decode("utf-8")
				barcodeType = obj.type
				data = [barcodeData, barcodeType]

				return data
		except Exception as ex:
			logger.error(ex)

	def run(self):
		while True:
			try:
				# time.sleep(1)
				prevTime = time.time()
				next_frame = self.task.get()
				data = self.decode(next_frame)
				# logger.info(f"\ndata --- {data}")

				self.result.put(data)
				# logger.info(f"data --- {self.result.get()}")

				## FPS
				# logger.info(f"{self.id} - FPS: {1 / (time.time() - prevTime): .4f}")
			# except Exception as ex:
			# 	logger.error(ex)
			except KeyboardInterrupt:
				logger.info("Kill all Processes QR Scanner")
				sys.exit(1)

	def update(self, id, task, rtsp_url):
		logger.info(f"{id} Loading...")
		cap = cv2.VideoCapture(rtsp_url)
		logger.info(f"{id} Loaded...")

		try:
			while True:
				# time.sleep(1)
				ret, frame = cap.read()
				task.put(frame)
				# logger.info(f" {id} {task.qsize()}")
				if task.qsize() == 20:
					task.get()
		except KeyboardInterrupt:
			logger.info("Kill all Processes Camera")
			sys.exit(1)

		cap.release()
		logger.info("Camera Connection Closed")

	def init_qr_scanner(self, num_process):
		for i in range(num_process):
			exec(f'proc{self.id}_{i} = mp.Process(target=self.run)')
			# exec(f"proc_{i}.daemon = True")
			exec(f'proc{self.id}_{i}.start()')
			# logger.info(f"Process -- proc_{i}")

	def start_stream_camera(self):
		# load process
		p = mp.Process(target=self.update, args=(self.id, self.task, self.rtsp_url))
		p.start()



# if __name__ == "__main__":
# 	cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "CAMERA", 2)
# 	cam1 = camera(0, "WEBCAM", 2)
#
# 	url = "http://localhost:8200/qr_receive/"
# 	# url = "http://api-lq.bookqve.com.vn/api/qr-code/save"
# 	token = "95003e12-f3a1-4717-aeda-bdc0e058400d"


