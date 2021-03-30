import cv2
import multiprocessing as mp
from qr_scanner import decoder
from camera import camera
import requests, json
import os
from utils.logger import get_logger
import chime, time


if __name__ == "__main__":
	logger = get_logger('JFA REST Server Gateway')

	logger.info(f"RTSP_URL: {os.environ.get('CAMERA_RTSP_URL')}")
	rtsp_url = os.environ.get('CAMERA_RTSP_URL', 'rtsp://admin:123456ab@192.168.23.103:554/Streaming/Channels/103')
	# rtsp_url = os.environ.get('CAMERA_RTSP_URL', 'rtsp://admin:123456ab@192.168.23.102:554/Streaming/Channels/101')
	camera_name = rtsp_url.split('@')[1]

	cam = camera(rtsp_url)
	logger.info(f"Camera is alive?: {cam.p.is_alive()}")

	prevTime = 0

	while(1):
		# Video capture
		frame = cam.get_frame()
		data = decoder(frame)
		if data is not None:
			chime.success(sync=True, raise_error=True)

		### FPS
		curTime = time.time()
		sec = curTime - prevTime
		fps = 1 / (sec)
		str = "FPS : %0.1f" % fps
		cv2.putText(frame, str, (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0))
		prevTime = curTime

		cv2.imshow("Feed", frame)

		# # Check QR code in DB
		# if data is not None:
		# 	barcodeData = data[0]
		# 	barcodeType = data[1]
		#
		# 	logger.info(f"Barcode: {barcodeData}")
		# 	# Send result by API
		# 	code_data = list(barcodeData.split(","))
		#
		# 	# url = "http://receive_api:8200/qr_receive/"
		# 	url = "http://api-lq.bookve.com.vn/api/qr-code/save"
		# 	headers = {
		# 		"token": "95003e12-f3a1-4717-aeda-bdc0e058400d"
		# 	}
		# 	data = {
		# 		"maphieu": str(code_data[1]),
		# 		"mahang": str(code_data[0]),
		# 		"soluong": str(code_data[2]),
		# 		"tencamera": camera_name
		# 	}
		#
		# 	res = requests.request("POST", url, headers=headers, data=data)
		# 	logger.info(res)

		key = cv2.waitKey(10)
		if key == ord('q'):
			break

	cv2.destroyAllWindows()
	cam.end()