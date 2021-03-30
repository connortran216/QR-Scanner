import cv2
import numpy as np
# from multi_camera import camera
from test_cam import camera
from multi_qr_scanner import decoder, Consumer, Task
import requests
import multiprocessing as mp
from utils.logger import get_logger

import multiprocessing
import time

global db
db = []


def return_qr(data, camera_name):
	# Check QR code in DB
	if data is not None:
		if data not in db:
			db.append(data)
			if len(db) >= 1000:
				del db[:-100]
			print(data)
			# return data
			# barcodeData = data[0]
			# logger.info(f"Barcode: {barcodeData}")
			#
			# # Send result by API
			# code_data = list(barcodeData.split(","))
			#
			# # url = "http://receive_api:8200/qr_receive/"
			# url = "http://api-lq.bookve.com.vn/api/qr-code/save"
			# headers = {
			# 	"token": "95003e12-f3a1-4717-aeda-bdc0e058400d"
			# }
			# data = {
			# 	"maphieu": str(code_data[1]),
			# 	"mahang": str(code_data[0]),
			# 	"soluong": str(code_data[2]),
			# 	"tencamera": camera_name
			# }
			#
			# res = requests.request("POST", url, headers=headers, data=data)
			# logger.info(res)

if __name__ == "__main__":
	logger = get_logger('JFA REST Server Gateway')

	# logger.info(f"RTSP_URL: {os.environ.get('CAMERA_RTSP_URL')}")
	# rtsp_url = os.environ.get('CAMERA_RTSP_URL', 'rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101')
	# camera_name = rtsp_url.split('@')[1]

	# Init camera process
	# Cam 0
	cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "cam0")
	logger.info(f"Camera is alive?: {cam0.p.is_alive()} ---- Camera's ID: {cam0.id}")
	camera0_name = cam0.id

	# Cam 1
	cam1 = camera(0, "cam1")
	logger.info(f"Camera is alive?: {cam1.p.is_alive()} ---- Camera's ID: {cam1.id}")
	camera1_name = cam1.id

	camera_list = [camera0_name, camera1_name]
	# camera_list = [camera0_name]
	task_list = []
	result_list = []
	consumer_list = []

	for camera in range(len(camera_list)):
		task = multiprocessing.Queue()
		task_list.append(task)

		result = multiprocessing.Queue()
		result_list.append(result)

		# Start consumers
		num_consumers = 1  # multiprocessing.cpu_count() * 2
		print('Creating %d consumers' % num_consumers)

		consumer = [Consumer(task, result)
						  for i in range(num_consumers)]
		consumer_list.append(consumer)

	for consumer in consumer_list:
		for w in consumer:
			w.start()

	# # Init Consumer cam0
	# # Establish communication queues
	# tasks_cam0 = multiprocessing.Queue()
	# results_cam0 = multiprocessing.Queue()
	#
	# # Start consumers
	# num_consumers = 1 #multiprocessing.cpu_count() * 2
	# print('Creating %d consumers' % num_consumers)
	#
	# consumers_cam0 = [Consumer(tasks_cam0, results_cam0)
	# 			 for i in range(num_consumers)]
	# for w in consumers_cam0:
	# 	w.start()

	###----------------------###

	# # Init Consumer cam1
	# # Establish communication queues
	# tasks_cam1 = multiprocessing.Queue()
	# results_cam1 = multiprocessing.Queue()
	#
	# # Start consumers
	# num_consumers = 2 #multiprocessing.cpu_count() * 2
	# print('Creating %d consumers' % num_consumers)
	#
	# consumers_cam1 = [Consumer(tasks_cam1, results_cam1)
	# 				  for i in range(num_consumers)]
	# for w in consumers_cam1:
	# 	w.start()

	prevTime = 0

	while(1):
		# Video capture
		frame0 = cam0.get_frame(0.50)
		frame1 = cam1.get_frame()

		frame_list = []
		frame_list.append(frame0)
		frame_list.append(frame1)

		data_list = []
		for i in range(len(task_list)):
			task_list[i].put(Task(frame_list[i]))
			data_list.append(result_list[i].get())

			if data_list[i] is not None:
				"""DETECT QRCODE"""
				points = data_list[i][2]
				pts = np.array(points, np.int32)
				pts = pts.reshape((-1, 1, 2))
				cv2.polylines(frame_list[i], [pts], True, (0, 255, 0), 3)

				barcodeData = data_list[i][0]
				barcodeType = data_list[i][1]
				string = "Detected QR"
				cv2.putText(frame_list[i], string, (int(data_list[i][-1]), int(data_list[i][-2])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

				return_qr(data_list[i][0], camera_list[i])

			### FPS
			curTime = time.time()
			sec = curTime - prevTime
			fps = 1 / (sec)
			str = "FPS : %0.1f" % fps
			print(str)
			cv2.putText(frame_list[i], str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
			cv2.imshow(f"Cam--{i}", frame_list[i])

		prevTime = curTime

		# # Process task cam0
		# tasks_cam0.put(Task(frame0))
		# data0 = results_cam0.get()
		# # print(data0)
		#
		# # # Process task cam1
		# tasks_cam1.put(Task(frame1))
		# data1 = results_cam1.get()
		# # print(data1)

		# for i in range(len(data_list)):
		# 	if data_list[i] is not None:
		# 		"""DETECT QRCODE"""
		# 		points = data_list[i][2]
		# 		pts = np.array(points, np.int32)
		# 		pts = pts.reshape((-1, 1, 2))
		# 		cv2.polylines(frame0, [pts], True, (0, 255, 0), 3)
		#
		# 		barcodeData = data_list[i][0]
		# 		barcodeType = data_list[i][1]
		# 		string = "Detected QR"
		# 		cv2.putText(frame0, string, (int(data_list[i][-1]), int(data_list[i][-2])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
		#
		# 		return_qr(data_list[i][0], camera_list[i])
		#
		# 		cv2.imshow(f"Cam--{i}", frame_list[i])
		# if data0 is not None:
		# 	"""DETECT QRCODE"""
		# 	points = data0[2]
		# 	pts = np.array(points, np.int32)
		# 	pts = pts.reshape((-1, 1, 2))
		# 	cv2.polylines(frame0, [pts], True, (0, 255, 0), 3)
		#
		# 	barcodeData = data0[0]
		# 	barcodeType = data0[1]
		# 	string = "Detected QR"
		# 	cv2.putText(frame0, string, (int(data0[-1]), int(data0[-2])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
		#
		# if data1 is not None:
		# 	"""DETECT QRCODE"""
		# 	points = data1[2]
		# 	pts = np.array(points, np.int32)
		# 	pts = pts.reshape((-1, 1, 2))
		# 	cv2.polylines(frame1, [pts], True, (0, 255, 0), 3)
		#
		# 	barcodeData = data1[0]
		# 	barcodeType = data1[1]
		# 	string = "Detected QR"
		# 	cv2.putText(frame1, string, (int(data1[-1]), int(data1[-2])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
		#
		#
		#
		# cv2.imshow("Feed0", frame0)
		# cv2.imshow("Feed1", frame1)

		# for i in range(len(frame_list)):
		# 	cv2.imshow(f"Cam--{i}", frame_list[i])
		#
		# if data0 is not None:
		# 	return_qr(data0[0], camera0_name)
		#
		# if data1 is not None:
		# 	return_qr(data1[0], camera1_name)


		key = cv2.waitKey(1)
		# if key == ord('q'):
		# 	for task in range(0, num_consumers):
		# 		tasks_cam0.put(None)
		# 		tasks_cam1.put(None)
		# 	# results_cam0.put(None)
		# 	break
		if key == ord('q'):
			for task in task_list:
				task.put(None)
			# results_cam0.put(None)
			break

	cv2.destroyAllWindows()
	cam0.end()
	cam1.end()