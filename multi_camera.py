import cv2
import multiprocessing as mp
from qr_scanner import decoder
import requests

from utils.logger import get_logger
logger = get_logger('Init Camera')

class camera():

	def __init__(self, rtsp_url, id):
		# Camera's ID
		self.id = id

		#load pipe for data transmittion to the process
		self.parent_conn, child_conn = mp.Pipe()

		#load process
		self.p = mp.Process(target=self.update, args=(child_conn, rtsp_url))

		#start process
		self.p.daemon = True
		self.p.start()

	def end(self):
		#send closure request to process
		self.parent_conn.send(2)

	def update(self, conn, rtsp_url):
		#load cam into seperate process

		logger.info(f"{self.id} Loading...")
		# cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
		cap = cv2.VideoCapture(rtsp_url)
		logger.info(f"{self.id} Loaded...")
		run = True

		while run:
			#grab frames from the buffer
			cap.grab()

			#recieve input data
			rec_dat = conn.recv()

			# print("Running")
			if rec_dat == 1:
				#if frame requested
				ret, frame = cap.read()
				conn.send(frame)

			elif rec_dat ==2:
				#if close requested
				cap.release()
				run = False

		# print("Camera Connection Closed")
		logger.info("Camera Connection Closed")
		conn.close()

	def get_frame(self, resize=None):
		###used to grab frames from the cam connection process

		##[resize] param : % of size reduction or increase i.e 0.65 for 35% reduction  or 1.5 for a 50% increase

		#send request
		self.parent_conn.send(1)
		frame = self.parent_conn.recv()

		#reset request
		self.parent_conn.send(0)

		#resize if needed
		if resize == None:
			return frame
		else:
			frame = self.rescale_frame(frame, resize)
			return frame


	def rescale_frame(self,frame, percent=50):
		return cv2.resize(frame, None, fx=percent, fy=percent)
