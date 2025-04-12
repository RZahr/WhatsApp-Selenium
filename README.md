# WhatsApp-Selenium

## Disclaimer

Use this software at your own risk. The author assumes no responsibility or liability for any consequences resulting from the use or misuse of this tool.
You are solely responsible for ensuring your use complies with all applicable laws and regulations.


## What is this

Forked from https://github.com/ar-nadeem/WhatsApp-Selenium

# How to use ?

### Setup

1. First clone the prjoect then install requirements from the `requirements.txt`

```bash
pip install -r requirements.txt
```

2. Install **_Chrome web driver_** from herehttps://googlechromelabs.github.io/chrome-for-testing/ and **_Chrome browser_** from here https://www.google.com/chrome. Make sure to add your web driver to your system path, although it is not necessary.

3. Run uvicorn api:app --reload
4. you can now call
```
curl --location 'http://127.0.0.1:8000/whatsapp' \
--header 'Content-Type: application/json' \
--data '{
    "mobileNumber": "some number",
    "message": "test"
}'
```