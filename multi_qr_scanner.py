import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2

from utils.logger import get_logger
logger = get_logger('JFA REST Server Gateway')

import cv2
import multiprocessing as mp
from qr_scanner import decoder
import requests

from utils.logger import get_logger
logger = get_logger('JFA REST Server Gateway')

import multiprocessing
import time

class Consumer(multiprocessing.Process):

	def __init__(self, task_queue, result_queue):
		multiprocessing.Process.__init__(self)
		self.task_queue = task_queue
		self.result_queue = result_queue

	def run(self):
		proc_name = self.name
		while True:
			next_task = self.task_queue.get()
			if next_task is None:
				# Poison pill means we should exit
				print('%s: Exiting' % proc_name)
				break
			# print('%s: %s' % (proc_name, next_task))
			answer = next_task()
			self.result_queue.put(answer)
		return


class Task(object):
	def __init__(self, image):
		self.image = image

	def __call__(self):
		# time.sleep(0.1) # pretend to take some time to do our work
		gray_img = cv2.cvtColor(self.image, 0)

		# box = detect(self.image)
		# roi_corners = np.array([box], dtype=np.int32)
		# gray_img = cv2.polylines(self.image, roi_corners, 1, (255, 0, 0), 3)

		barcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])

		for obj in barcode:
			"""DETECT QRCODE"""
			points = obj.polygon
			(x, y, w, h) = obj.rect
			# pts = np.array(points, np.int32)
			# pts = pts.reshape((-1, 1, 2))
			# cv2.polylines(self.image, [pts], True, (0, 255, 0), 3)

			"""EXTRACT QRCODE INFO"""
			barcodeData = obj.data.decode("utf-8")
			barcodeType = obj.type
			# string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)

			# cv2.putText(self.image, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

			# print("Barcode: " + barcodeData + " | Type: " + barcodeType)
			data = [barcodeData, barcodeType, points, x, y]

			return data

	def __str__(self):
		return "Scanning.."


# if __name__ == '__main__':
# 	# Establish communication queues
# 	tasks = multiprocessing.Queue()
# 	results = multiprocessing.Queue()
#
# 	# Start consumers
# 	num_consumers = multiprocessing.cpu_count() * 2
# 	print('Creating %d consumers' % num_consumers)
#
# 	consumers = [ Consumer(tasks, results)
# 				  for i in range(num_consumers) ]
# 	for w in consumers:
# 		w.start()
#
# 	# Enqueue jobs
# 	num_jobs = 10
# 	for i in range(num_jobs):
# 		tasks.put(Task(i, i))
#
# 	# Add a poison pill for each consumer
# 	for i in range(num_consumers):
# 		tasks.put(None)
#
# 	# Start printing results
# 	while num_jobs:
# 		result = results.get()
# 		print('Result:', result)
# 		num_jobs -= 1


# import the necessary packages

import numpy as np
import cv2
import imutils

def detect(image):
	# convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction using OpenCV 2.4
	ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
	gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
	gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

	# subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)

	# cv2.imshow("sample", gray)
	# cv2.waitKey(0)

	# blur and threshold the image
	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	# perform a series of erosions and dilations
	closed = cv2.erode(closed, None, iterations=4)
	closed = cv2.dilate(closed, None, iterations=4)

	cv2.imshow("sample", gradient)
	cv2.waitKey(0)

	# find the contours in the thresholded image
	cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# if no contours were found, return None
	if len(cnts) == 0:
		return None

	# otherwise, sort the contours by area and compute the rotated
	# bounding box of the largest contour
	c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
	rect = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
	box = np.int0(box)

	# return the bounding box of the barcode
	return box

# image = cv2.imread("qr1.jpg")
# box = detect(image)
# print(box)
# roi_corners = np.array([box], dtype=np.int32)
# gray_img = cv2.polylines(image, roi_corners, 1, (255, 0, 0), 3)
# cv2.imshow("sample", gray_img)
# cv2.waitKey(0) # waits until a key is pressed
# cv2.destroyAllWindows()


# gray_img = cv2.cvtColor(image, 0)
# barcode = decode(gray_img)
# for obj in barcode:
# 	"""DETECT QRCODE"""
# 	points = obj.polygon
# 	(x, y, w, h) = obj.rect
# 	pts = np.array(points, np.int32)
# 	pts = pts.reshape((-1, 1, 2))
# 	cv2.polylines(image, [pts], True, (0, 255, 0), 3)
#
# 	"""EXTRACT QRCODE INFO"""
# 	barcodeData = obj.data.decode("utf-8")
# 	barcodeType = obj.type
# 	string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
#
# 	cv2.putText(image, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
# 	cv2.imshow("sample", image)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()
# 	print("Barcode: " + barcodeData + " | Type: " + barcodeType)
# 	data = [barcodeData, barcodeType, points, x, y]

