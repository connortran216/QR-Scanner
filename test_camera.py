import cv2
import multiprocessing as mp
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
# import pyboof as pb
import numpy as np
import time

from yolo_tiny_model import postprocess, Detector

from utils.logger import get_logger

logger = get_logger('Init Camera')
import sys

# QRCodeDetector
# qrResult = ''
# pb.init_memmap()
# detector = pb.FactoryFiducial(np.uint8).qrcode()


class Camera:
	def __init__(self, rtsp_url, id_, num_process=1):
		self.id = id_
		self.rtsp_url = rtsp_url

		self.task = mp.Queue()
		self.result = mp.Queue()

		self.start_stream_camera()
		self.init_qr_scanner(num_process)

	@staticmethod
	def qr_decoder(image, scanner, detector):

		# gray_img = cv2.cvtColor(image, 0)
		# barcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])

		outs = detector.detect_qr(image)
		cropped_image = postprocess(image, outs)

		if cropped_image is not None:
			cropped_image = cv2.cvtColor(cropped_image, 0)
			barcode = decode(cropped_image, symbols=[ZBarSymbol.QRCODE])

			try:
				for obj in barcode:
					"""EXTRACT QRCODE INFO"""
					barcodeData = obj.data.decode("utf-8")
					barcodeType = obj.type
					data = [barcodeData, barcodeType]
					logger.info(f"QR CODE ----- {data}")
					return data
			except Exception as ex:
				logger.error(ex)

		# try:
		# 	# # QR Code Detector:
		# 	outs = detector.detect_qr(image)
		# 	cropped_image = postprocess(image, outs)
		#
		# 	if cropped_image is not None:
		# 		# # QR Scanner:
		# 		frame_mono = cv2.cvtColor(np.uint8(cropped_image), cv2.COLOR_BGR2GRAY)
		# 		boof_img = pb.ndarray_to_boof(frame_mono)
		# 		scanner.detect(boof_img)
		# 		if len(scanner.detections) > 0:
		# 			qr_result = scanner.detections[0].message
		# 			logger.info(f"QR CODE ----- {qr_result}")
		# 			return qr_result
		# 	else:
		# 		return None

		# except Exception as ex:
		# 	logger.error(ex)

	def run(self):
		# i = 0
		# pb.init_memmap()
		# scanner = pb.FactoryFiducial(np.uint8)
		# scanner = scanner.qrcode()
		scanner = None
		detector = Detector()

		while True:
			try:
				next_frame = self.task.get()
				data = self.qr_decoder(next_frame, scanner, detector)
				# self.result.put(data)

				# i += 1
				# if data is not None:
				# 	cv2.imwrite('frames_qr/{index}.png'.format(index=i), next_frame)
				# else:
				# 	cv2.imwrite('frames_non_qr/{index}.png'.format(index=i), next_frame)

			except KeyboardInterrupt:
				logger.info("Kill all Processes QR Scanner")
				sys.exit(1)

	def update(self, id, task, rtsp_url):
		logger.info(f"{id} Loading...")
		cap = cv2.VideoCapture(rtsp_url)
		logger.info(f"{id} Loaded...")

		try:
			while True:
				prevtime = time.time()
				ret, frame = cap.read()
				task.put(frame)
				# FPS
				logger.info(f"{self.id} - FPS: {1 / (time.time() - prevtime): .4f}")

				# logger.info(f" {id} {task.qsize()}")
				if task.qsize() == 20:
					task.get()

		except KeyboardInterrupt:
			logger.info("Kill all Processes Camera")
			sys.exit(1)

		# cap.release()
		# logger.info("Camera Connection Closed")

	def init_qr_scanner(self, num_process):
		# pb.init_memmap()
		# scanner = pb.FactoryFiducial(np.uint8)
		# scanner = scanner.qrcode()

		for _ in range(num_process):
			p = mp.Process(target=self.run)
			p.start()

	def start_stream_camera(self):
		# load process
		p = mp.Process(target=self.update, args=(self.id, self.task, self.rtsp_url))
		p.start()


if __name__ == "__main__":

	cam0 = Camera("rtsp://admin:123456ab@192.168.23.105:554/Streaming/Channels/101", "CAMERA0", 10)
	cam1 = Camera("rtsp://admin:123456ab@192.168.23.106:554/Streaming/Channels/101", "CAMERA1", 10)
# #
# 	url = "http://localhost:8200/qr_receive/"
# 	# url = "http://api-lq.bookqve.com.vn/api/qr-code/save"
# 	token = "95003e12-f3a1-4717-aeda-bdc0e058400d"
