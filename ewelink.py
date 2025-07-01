import http.client
import json

import hmac
import base64
import hashlib

NONCE = 'zt123456'
APP_ID = 'SfrSFyeJMgUaKktxWtuO1d845z3JpAKY'
appsecret = "fqxPgjsQq8erpIGFwNOdO6WELd1uPeN0"
REDIRECT_URL = "http://127.0.0.1:8000/oauth/callback"
PASSWORD = "p&ML^9l*7OwMqmEo1L7Y"
EMAIL = "rashadzahr@hotmail.com"

# Function to generate Base64-encoded HMAC-SHA256 signature
def create_signHelper(appsecret, message):
    signature = hmac.new(
        key=appsecret.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def createSign(code: str) -> str:
    # Your request body as a Python dictionary
    message_dict = {
        "code": code,
        "redirectUrl": REDIRECT_URL,
        "grantType": "authorization_code"
    }

    # Convert the dictionary to a compact JSON string
    message = json.dumps(message_dict, separators=(',', ':'))

    # Generate the signature
    sign = create_signHelper(appsecret, message)
    return sign

def getToken(code: str, sign: str):
    conn = http.client.HTTPSConnection("as-apia.coolkit.cc")
    payload = "{\"code\":\""+code+"\",\"redirectUrl\":\""+REDIRECT_URL+"\",\"grantType\":\"authorization_code\"}"
    headers = {
    'X-CK-Nonce': NONCE,
    'Authorization': f'Sign {sign}',
    'Content-Type': 'application/json',
    'X-CK-Appid': APP_ID
    }
    conn.request("POST", "/v2/user/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")  # Decode byte data to string

    json_data = json.loads(data)
    accessToken = json_data['data']['accessToken']
    refreshToken = json_data['data']['refreshToken']
    return accessToken, refreshToken
    
    #{"error":0,"msg":"","data":{"accessToken":"7e4f8d87451ababf66bd90672bd0aadba0ca9694","atExpiredTime":1753224432662,"refreshToken":"ae05dbc55b109fa960f27472b173f8e05c76c735","rtExpiredTime":1755816432664}}

def setDeviceStatus(accessToken: str, deviceId: str, deviceType: int, switch: str):
    conn = http.client.HTTPSConnection("as-apia.coolkit.cc")
    payload = "{\n    \"type\":"+deviceType+",\n    \"id\":\""+deviceId+"\",\n    \"params\":{\n        \"switch\":\""+switch+"\"\n    }\n}"
    headers = {
    'X-CK-Nonce': NONCE,
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/v2/device/thing/status", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def getDeviceList(accessToken: str):
    conn = http.client.HTTPSConnection("as-apia.coolkit.cc")
    payload = ''
    headers = {
    'X-CK-Nonce': NONCE,
    'Authorization': f'Bearer {accessToken}',
    'Content-Type': 'application/json'
    }
    conn.request("GET", "/v2/device/thing", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")  # Decode byte data to string

    json_data = json.loads(data)
    # Extract devices
    devices = json_data["data"]["thingList"]

    # Collect name, deviceid, and itemType
    device_info = []
    for device in devices:
        item_type = device.get("itemType")
        item_data = device.get("itemData", {})
        name = item_data.get("name")
        deviceid = item_data.get("deviceid")
        brandName = item_data.get("brandName")
        brandLogo = item_data.get("brandLogo")
        productModel = item_data.get("productModel")
        online = item_data.get("online")
        switch = item_data.get("params", {}).get("switch")
        startup = item_data.get("params", {}).get("startup")
        device_info.append({
            "name": name,
            "deviceid": deviceid,
            "itemType": item_type,
            "online": online, 
            "switch": switch,
            'brandName': brandName,
            'brandLogo': brandLogo,
            'productModel': productModel,
            'startup': startup
        })
    return device_info    

def getCode() -> str:
    conn = http.client.HTTPSConnection("apia.coolkit.cn")
    payload = "{\"password\":\""+PASSWORD+"\",\"clientId\":\""+APP_ID+"\",\"state\":\"XXX\",\"redirectUrl\":\""+REDIRECT_URL+"\",\"authorization\":\"Sign Ny/JJG3Oji9+RVM17kqQVcmM1wNyug7GcDtgBLde14A=\",\"nonce\":\""+NONCE+"\",\"seq\":\"123\",\"grantType\":\"authorization_code\",\"email\":\""+EMAIL+"\"}"
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Sign Ny/JJG3Oji9+RVM17kqQVcmM1wNyug7GcDtgBLde14A=',
    'content-type': 'application/json; charset=utf-8',
    'origin': 'https://c2ccdn.coolkit.cc',
    'priority': 'u=1, i',
    'referer': 'https://c2ccdn.coolkit.cc/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-ck-appid': APP_ID, 
    'x-ck-nonce': NONCE,
    'x-ck-seq': '123'
    }
    conn.request("POST", "/v2/user/oauth/code", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")  # Decode byte data to string

    json_data = json.loads(data)
    code = json_data['data']['code']
    return code
