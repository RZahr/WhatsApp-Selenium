# python_service.py
from Whatsapp import Whatsapp
from fastapi import FastAPI, Request, HTTPException
import uvicorn
from logger_config import logger
from greeclimate.main import GetCurrentStatus, DeviceInfo, SetPowerState

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp(data: dict):
    logger.info(f"request: {data}")

    mobileNumber = data.get("mobileNumber")
    message = data.get("message")
    file = data.get("file")
    print(f"mobile: {mobileNumber}")
    print(f"message: {message}")
    print(f"file: {file}")

    whatsapp = Whatsapp(silent=False, headless=False)
    logger.info(f"123456")
    logger.info(f"request2: {data}")
    status = False
    try:
        if file:
            status = { "status": whatsapp.uploadFile(message, file, mobileNumber) }
        else:
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


la_maylit_faw2 = DeviceInfo(
            version="V2.0.0",
            ip="192.168.0.21",
            brand="gree",
            mac="9424b8feaa47",
            model="gree",
            name="9424b8feaa47",
            port=7000
        ) 
la_maylit_faw2DeviceKey = "Xz847mBUFh9182TA"
upper = DeviceInfo(
            version="V2.0.0",
            ip="192.168.0.25",
            brand="gree",
            mac="9424b8faee40",
            model="gree",
            name="9424b8faee40",
            port=7000
        ) 
upperDeviceKey = "7k3vKgep2ju0GK5F"
one_more_rep = DeviceInfo(
            version="V2.0.0",
            ip="192.168.0.94",
            brand="gree",
            mac="9424b8f8cb24",
            model="gree",
            name="9424b8f8cb24",
            port=7000
        ) 
oneMoreRepDeviceKey = "42Y9mHFA5805VqtQ"

@app.get("/greeStatus")
async def GreeStatus(acId: str):
     if (acId == oneMoreRepDeviceKey):
        return await GetCurrentStatus(one_more_rep, acId)
     if (acId == la_maylit_faw2DeviceKey):
        return await GetCurrentStatus(la_maylit_faw2, acId)
     if (acId == upperDeviceKey):
        return await GetCurrentStatus(upper, acId)

@app.post("/greeStatus")
async def GreeStatus(acId: str, status: bool):
    if (acId == oneMoreRepDeviceKey):
        return await SetPowerState(status, one_more_rep, acId)
    if (acId == la_maylit_faw2DeviceKey):
        return await SetPowerState(status, la_maylit_faw2, acId)
    if (acId == upperDeviceKey):
        return await SetPowerState(status, upper, acId)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)