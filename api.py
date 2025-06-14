# python_service.py
from Whatsapp import Whatsapp
from fastapi import FastAPI, Request, HTTPException
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
    logger.info(f"request2: {data}")
    status = False
    try:
        status = { "status": whatsapp.sendMessage(message, mobileNumber) }
    except Exception as e:
        status = False
        # logger.info(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")

    logger.info(f"status result: {status}")
    if status == False:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
    else:
        return status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)