import cv2
import multiprocessing as mp
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import time
from multi_qr_scanner import QR_Scanner

from utils.logger import get_logger
logger = get_logger('Init Camera')


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
				next_frame = self.task.get()
				# print('%s: %s' % (proc_name, next_task))
				answer = self.decode(next_frame)
				# self.result.put(answer)
				## FPS
				logger.info(f"{self.id} - FPS: {1 / (time.time() - prevTime): .4f}")
			except Exception as ex:
				logger.error(ex)

	@staticmethod
	def update(id, task, rtsp_url):
		logger.info(f"{id} Loading...")
		cap = cv2.VideoCapture(rtsp_url)
		logger.info(f"{id} Loaded...")
		run = True
		while run:
			ret, frame = cap.read()
			task.put(frame)
			# logger.info(task.qsize())
			if task.qsize() == 5:
				task.get()
		cap.release()
		logger.info("Camera Connection Closed")

	def init_qr_scanner(self, num_process):
		# a = []
		# for _ in range(num_process):
		# 	a.append(mp.Process(target=self.run))
		# 	a[-1].daemon = True
		# 	a[-1].start()
		for i in range(num_process):
			exec(f'proc_{i} = mp.Process(target=self.run)')
			exec(f'proc_{i}.start()')
			logger.info(f"Process -- proc_{i}")

	def start_stream_camera(self):
		# load process
		p = mp.Process(target=self.update, args=(self.id, self.task, self.rtsp_url))
		p.start()

cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "CAMERA", 2)
cam1 = camera(0, "WEBCAM", 2)


# def get_frame(self, resize=None):
	# 	###used to grab frames from the cam connection process
	#
	# 	##[resize] param : % of size reduction or increase i.e 0.65 for 35% reduction  or 1.5 for a 50% increase
	# 	prevTime = 0
	# 	#send request
	# 	# # Init Consumer cam0
	# 	# # Establish communication queues
	# 	results_cam = mp.Queue()
	#
	# 	# Start consumers
	# 	num_consumers = 1  # multiprocessing.cpu_count() * 2
	# 	print('Creating %d consumers' % num_consumers)
	#
	# 	consumers_cam0 = [Consumer(self.q, results_cam) for i in range(num_consumers)]
	# 	for w in consumers_cam0:
	# 		w.start()
	#
	# 	#resize if needed
	# 	if resize == None:
	#
	# 		while 1:
	# 			frame = self.q.get()
	# 			# # Process task cam0
	# 			tasks_cam.put(Task(frame))
	# 			data = results_cam.get()
	#
	# 			# mp.Process(target=return_qr, args=(data0, "cam0"))
	# 			mp.Process(target=return_qr, args=(data, "cam1"))
	#
	# 			### FPS
	# 			curTime = time.time()
	# 			sec = curTime - prevTime
	# 			fps = 1 / (sec)
	# 			str = "FPS : %0.1f" % fps
	# 			print(str)
	#
	# 			prevTime = curTime
	#
	# 	else:
	# 		while 1:
	# 			frame = self.q.get()
	# 			frame = self.rescale_frame(frame, resize)
	#
	# 			# # Process task cam0
	# 			tasks_cam.put(Task(frame))
	# 			data = results_cam.get()
	#
	# 			return data
	#
	#
	# def rescale_frame(self,frame, percent=50):
	# 	return cv2.resize(frame, None, fx=percent, fy=percent)

# cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "CAMERA")
# cam1 = camera(0, "WEBCAM")
# logger.info(f"Camera is alive?: {cam0.p.is_alive()} ---- Camera's ID: {cam0.id}")
# camera0_name = cam0.id
#
# prevTime = 0
# while (1):
# 	# Video capture
# 	frame0 = cam0.get_frame(0.5)
# 	cv2.imshow(f"Cam--", frame0)
#
# 	### FPS
# 	curTime = time.time()
# 	sec = curTime - prevTime
# 	fps = 1 / (sec)
# 	str = "FPS : %0.1f" % fps
# 	print(str)
# 	prevTime = curTime
#
# 	key = cv2.waitKey(10)
# 	if key == ord('q'):
# 		break