# python_service.py
from Whatsapp import Whatsapp
from fastapi import FastAPI, Request
import uvicorn
from logger_config import logger

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp(data: dict):
    logger.info(f"request: {data}")

    mobileNumber = data.get("mobileNumber")
    message = data.get("message")
    print(f"mobile: {mobileNumber}")
    print(f"message: {message}")

    whatsapp = Whatsapp(silent=True, headless=False)
    status = False
    try:
        status = { "status": whatsapp.sendMessage(message, mobileNumber) }
    except Exception as e:
        status = False

    logger.info(f"status result: {status}")
    return status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)