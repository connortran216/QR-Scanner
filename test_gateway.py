from test_camera import camera
import requests
from utils.logger import get_logger
import multiprocessing as mp
import sys
import chime

global db


# def check_data(data):
# 	db = []
# 	# Check QR code in DB
# 	if data is not None:
# 		if data not in db:
# 			db.append(data)
# 			if len(db) >= 1000:
# 				del db[:-100]
# 			logger.info(f"{db}")
# 			return True
# 		else:
# 			return False

class send_result():
	def __init__(self, url, token, result_queue, camera_name):
		self.result_queue = result_queue
		self.camera_name = camera_name
		self.url = url
		self.token = token
		self.start_send_result()

	@staticmethod
	def check_data(data):
		# Check QR code in DB
		if data is not None:
			if data not in db:
				db.append(data)
				if len(db) >= 1000:
					del db[:-100]
				logger.info(f"{db}")
				return True
			else:
				return False

	def return_qr(self, url, token, camera_name):
		while 1:
			try:
				data = self.result_queue.get()
				# logger.info(f"Data: {data}")

				if self.check_data(data):
				# if check_data(data):
					chime.success(sync=True, raise_error=True)
					# barcodeData = data[0]
					# logger.info(f"Barcode: {barcodeData}")
					#
					# # Send result by API
					# code_data = list(barcodeData.split(","))
					# headers = {
					# 	"token": self.token
					# }
					# data = {
					# 	"maphieu": str(code_data[1]),
					# 	"mahang": str(code_data[0]),
					# 	"soluong": str(code_data[2]),
					# 	"tencamera": self.camera_name
					# }
					#
					# res = requests.request("POST", self.url, headers=headers, data=data)
					# logger.info(res)
				else:
					pass

			except KeyboardInterrupt:
				logger.info("Kill all Processes Result Data")
				sys.exit(1)

	def start_send_result(self):
		# load process
		p = mp.Process(target=self.return_qr, args=(self.url, self.token, self.camera_name))
		p.start()

if __name__ == "__main__":
	logger = get_logger('JFA REST Server Gateway')

	# Init Process Camera
	cam0 = camera("rtsp://admin:123456ab@192.168.23.105:554/Streaming/Channels/101", "CAMERA0", 2)
	cam1 = camera("rtsp://admin:123456ab@192.168.23.106:554/Streaming/Channels/101", "CAMERA1", 2)
	# cam1 = camera(0, "WEBCAM", 2)

	# Init Process Return Data
	url = "http://localhost:8200/qr_receive/"
	# url = "http://api-lq.bookqve.com.vn/api/qr-code/save"
	token = "95003e12-f3a1-4717-aeda-bdc0e058400d"
	r0 = send_result(url, token, cam0.result, "CAMERA0")
	r1 = send_result(url, token, cam1.result, "CAMERA1")




