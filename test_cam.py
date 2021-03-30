import cv2
import multiprocessing as mp
from qr_scanner import decoder
import time

from utils.logger import get_logger
logger = get_logger('Init Camera')

class camera():

	def __init__(self, rtsp_url, id):
		# Camera's ID
		self.id = id

		#load pipe for data transmittion to the process
		self.q = mp.Queue()

		#load process
		self.p = mp.Process(target=self.update, args=(self.q, rtsp_url))

		#start process
		self.p.daemon = True
		self.p.start()

	def update(self, q, rtsp_url):
		#load cam into seperate process

		logger.info(f"{self.id} Loading...")
		# cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
		cap = cv2.VideoCapture(rtsp_url)
		logger.info(f"{self.id} Loaded...")
		run = True

		while run:
			#grab frames from the buffer
			cap.grab()

			#if frame requested
			ret, frame = cap.read()
			q.put(frame)
		cap.release()


		# print("Camera Connection Closed")
		logger.info("Camera Connection Closed")

	def get_frame(self, resize=None):
		###used to grab frames from the cam connection process

		##[resize] param : % of size reduction or increase i.e 0.65 for 35% reduction  or 1.5 for a 50% increase

		#send request
		frame = self.q.get()

		#resize if needed
		if resize == None:
			return frame
		else:
			frame = self.rescale_frame(frame, resize)
			return frame


	def rescale_frame(self,frame, percent=50):
		return cv2.resize(frame, None, fx=percent, fy=percent)

# cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "cam0")
# cam0 = camera(0,"cam0")
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