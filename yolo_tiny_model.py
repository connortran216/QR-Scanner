# https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html
# https://docs.opencv.org/master/d6/d0f/group__dnn.html
# https://docs.opencv.org/3.4/db/d30/classcv_1_1dnn_1_1Net.html
# https://github.com/opencv/opencv/blob/master/samples/dnn/object_detection.py
import cv2
import numpy as np
import time
from threading import Thread
import queue
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import os
import multiprocessing as mp


class Detector:
	def __init__(self):
		# self.frame = frame
		self.threshold = 0.6  # threshold
		self.classes = open('./core/qrcode.names').read().strip().split('\n')  # classes
		# self.weights = './core/qrcode-yolov3-tiny.weights' #weights
		# self.config = './core/qrcode-yolov3-tiny.cfg' #config
		self.net = cv2.dnn.readNetFromDarknet('./core/qrcode-yolov3-tiny.cfg', './core/qrcode-yolov3-tiny.weights')
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

		self.ln = self.net.getLayerNames()
		self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

	def detect_qr(self, frame):
		if not frame is None:
			blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)

			# Run a model
			# net.setInput(blob)
			self.net.setInput(blob)

			# # Determine the output layer
			# ln = self.net.getLayerNames()
			# ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

			# Compute
			# outs = net.forward(ln)
			outs = self.net.forward(self.ln)

			return outs

		return None


def postprocess(frame, outs):
	frameHeight, frameWidth = frame.shape[:2]

	classIds = []
	confidences = []
	boxes = []

	for out in outs:
		for detection in out:
			scores = detection[5:]
			classId = np.argmax(scores)
			confidence = scores[classId]
			if confidence > 0.6:
				x, y, width, height = detection[:4] * np.array([frameWidth, frameHeight, frameWidth, frameHeight])
				left = int(x - width / 2)
				top = int(y - height / 2)
				classIds.append(classId)
				confidences.append(float(confidence))
				boxes.append([left, top, int(width), int(height)])

	indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.6 - 0.1)
	for i in indices:
		i = i[0]
		box = boxes[i]
		left = box[0]
		top = box[1]
		width = box[2]
		height = box[3]
		cropped_image = frame[top:top + height, left:left + width]
		# cropped_image = cv2.cvtColor(cropped_image, 0)
		# cv2.imshow("TESTING", cropped_image)
		# cv2.waitKey()
		# barcode = decode(cropped_image, symbols=[ZBarSymbol.QRCODE])
		# print(barcode)
		return cropped_image

# if __name__ == "__main__":
# 	detector = Detector()
# img = cv2.imread("27.png")
#
# start_time = time.monotonic()
# outs = detector.detect_qr(img)
# elapsed_ms = (time.monotonic() - start_time) * 1000
# print('forward in %.1fms' % (elapsed_ms))
#
# start_time = time.monotonic()
# postprocess(img, outs)
# elapsed_ms = (time.monotonic() - start_time) * 1000
# print('posprocess in %.1fms' % (elapsed_ms))
#
# cv2.imshow("TESTING", img)
# cv2.waitKey()
