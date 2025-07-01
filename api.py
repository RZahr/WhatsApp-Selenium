# python_service.py
import asyncio
from fastapi.responses import HTMLResponse
from Whatsapp import Whatsapp
from fastapi import FastAPI, Request, HTTPException
import uvicorn
from logger_config import logger
from greeclimate.main import GetCurrentStatus, managed_device, Device, DeviceInfo, SetPowerState, discover

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp_endpoint(data: dict):
    mobileNumber = data.get("mobileNumber")
    message = data.get("message")
    file = data.get("file")

    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, send_whatsapp_sync, message, mobileNumber, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WhatsApp message: {e}")

    if not result:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
    return {"status": result}


def send_whatsapp_sync(message, mobileNumber, file):
    whatsapp = Whatsapp(silent=False, headless=False)
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

@app.get("/greeStatus")
async def GreeStatus(acId: str, version: str, ip: str, mac: str):
    device_info = DeviceInfo(
            version=version,
            ip=ip,
            brand="gree",
            mac=mac,
            model="gree",
            name=mac,
            port=7000
        )
    async with managed_device(Device(device_info), acId) as device:
        return await GetCurrentStatus(device) 

@app.get("/greeStatusBAK")
async def GreeStatusBAK(acId: str, version: str, ip: str, mac: str):
    device = DeviceInfo(
            version=version,
            ip=ip,
            brand="gree",
            mac=mac,
            model="gree",
            name=mac,
            port=7000
        )
   
    return await GetCurrentStatus(device, acId)

@app.post("/greeStatus")
async def GreeStatus(acId: str, status: bool, version: str, ip: str, mac: str):
    device_info = DeviceInfo(
            version=version,
            ip=ip,
            brand="gree",
            mac=mac,
            model="gree",
            name=mac,
            port=7000
        ) 
    async with managed_device(Device(device_info), acId) as device:
        return await SetPowerState(status, device)
    
@app.get("/oauth/callback", response_class=HTMLResponse)
async def oauth_callback(request: Request):
    query_params = dict(request.query_params)
    code = query_params.get("code")
    logger.info(f"code: {code}")
    if code:
        # Here you'd normally exchange the code for an access token
        return f"""
        <html>
            <body>
                <h2>Authorization successful!</h2>
                <p>Your authorization code is:</p>
                <code>{code}</code>
                <p>You can now close this tab.</p>
            </body>
        </html>
        """
    else:
        return "No authorization code found in query parameters."
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)