import cv2
import numpy as np
# from multi_camera import camera
from test_camera import camera
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
	cam0 = camera("rtsp://admin:123456ab@192.168.23.101:554/Streaming/Channels/101", "cam0", 2)
	# logger.info(f"Camera is alive?: {cam0.p.is_alive()} ---- Camera's ID: {cam0.id}")
	camera0_name = cam0.id

	# # Cam 1
	# cam1 = camera(0, "cam1", 2)
	# # logger.info(f"Camera is alive?: {cam1.p.is_alive()} ---- Camera's ID: {cam1.id}")
	# camera1_name = cam1.id

	# camera_list = [camera0_name, camera1_name]

	# Video capture
	# data0 = cam0.get_frame(0.50)
	# data1 = cam1.get_frame()
	# p0 = mp.Process(target=cam0.get_frame(), args=())
	# # p1 = mp.Process(target=cam1.get_frame(), args=())
	#
	# p0.start()
	# # p1.start()
	#
	# p0.join()
	# # p1.join()


