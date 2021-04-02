import numpy as np
import pyboof as pb
import cv2
import os
import time
from pyzbar.pyzbar import decode

# VideoCapture
cap = cv2.VideoCapture("rtsp://admin:123456ab@192.168.23.105:554/Streaming/Channels/101")

# QRCodeDetector
findQR = False
qrResult = ''
pb.init_memmap()
detector = pb.FactoryFiducial(np.uint8).qrcode()

print('Demo will work')
cnt = 0

while (cap.isOpened()):
	ret, frame = cap.read()
	if ret == True:
		# frame = cv2.flip(frame,-1)

		# # QR Code Detector
		# if not findQR:
		frame_mono = cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2GRAY)
		boof_img = pb.ndarray_to_boof(frame_mono)
		# boof_img = pb.load_single_band( 'path to image', np.uint8)
		start = time.time_ns()
		detector.detect(boof_img)
		if len(detector.detections) > 0:
			end = time.time_ns()
			print("running time is ", str(end - start))
			print("find QR Code ")
			findQR = True

			qrResult = detector.detections[0].message
			# print("QR Code  is: {}".format(qrResult))

			mask = detector.detections[0].mask_pattern
			# print("mask", mask)

			bounds = detector.detections[0].bounds
			# print(bounds)

			p0 = [int(bounds.vertexes[0].x), int(bounds.vertexes[0].y)]
			p1 = [int(bounds.vertexes[1].x), int(bounds.vertexes[1].y)]
			p2 = [int(bounds.vertexes[2].x), int(bounds.vertexes[2].y)]
			p3 = [int(bounds.vertexes[3].x), int(bounds.vertexes[3].y)]
			points = np.array([p0, p1, p2, p3], np.int32)
			points = points.reshape((-1, 1, 2))
			# print(points)
			cv2.polylines(frame, points, True, (0, 255, 0), 20)
			# cv2.rectangle(frame, p3, p1, color=(255, 0, 0), thickness=int(1))

			# x1, y1 = (int(bounds.vertexes[0].x), int(bounds.vertexes[0].y))
			# x2, y2 = (int(bounds.vertexes[1].x), int(bounds.vertexes[1].y))
			# x3, y3 = (int(bounds.vertexes[2].x), int(bounds.vertexes[2].y))
			# x4, y4 = (int(bounds.vertexes[3].x), int(bounds.vertexes[3].y))
			# line_length = 20
			#
			# cv2.line(frame, (x1, y1), (x1, y1 + line_length), (0, 255, 0), 2)  # -- top-left
			# cv2.line(frame, (x1, y1), (x1 + line_length, y1), (0, 255, 0), 2)
			#
			# cv2.line(frame, (x2, y2), (x2, y2 - line_length), (0, 255, 0), 2)  # -- bottom-left
			# cv2.line(frame, (x2, y2), (x2 + line_length, y2), (0, 255, 0), 2)
			#
			# cv2.line(frame, (x3, y3), (x3 - line_length, y3), (0, 255, 0), 2)  # -- top-right
			# cv2.line(frame, (x3, y3), (x3, y3 + line_length), (0, 255, 0), 2)
			#
			# cv2.line(frame, (x4, y4), (x4, y4 - line_length), (0, 255, 0), 2)  # -- bottom-right
			# cv2.line(frame, (x4, y4), (x4 - line_length, y4), (0, 255, 0), 2)



		cv2.imshow("test", frame)
	key = cv2.waitKey(10)

	if key == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()