import uvicorn
from fastapi import FastAPI, Form
import requests
from utils.logger import get_logger


logger = get_logger('JFA REST Server Gateway')
server = FastAPI(title='API Gateway',
				 description='QR Scanner',
				 version='1.0.0')

@server.post("/qr_receive/", tags=['CRUD'])
async def insert(maphieu: str = Form(...), mahang: str = Form(...), soluong: str = Form(...)):
	logger.info(f"MaPhieu: {maphieu}")
	logger.info(f"MaHang: {mahang}")
	logger.info(f"Soluong {soluong}")

	res = {
		"Message": 'Return successfully !!!',
		"status": 200
	}
	return res


if __name__ == "__main__":
	# host = 'localhost' if run local else 'receive_api'
	uvicorn.run(server, port=8200, host='receive_api', debug=True)