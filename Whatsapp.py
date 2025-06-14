from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from logger_config import logger
import os
import sys
import time
from dotenv import load_dotenv


# Load .env file
load_dotenv()

class Whatsapp:
    def __init__(self, executable_path=None, silent=False, headless=False):
        self.options = webdriver.ChromeOptions()
        if silent:
            self.__addOption("--log-level=3")
        if headless:
            self.__addOption("--headless")
            self.__addOption("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
            self.__addOption("--window-size=1920,1080")
            self.__addOption("--no-sandbox")

            # Get absolute path to directory where the script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        user_data_dir = os.path.join(base_dir, "UserData")
        os.makedirs(user_data_dir, exist_ok=True)


        self.__addOption(f"user-data-dir={user_data_dir}")

        # Use the actual path to your downloaded chromedriver
        service = Service(os.getenv("CHROME_DRIVER", ""))

        if executable_path:
            self.browser = webdriver.Chrome(service = service,
                options=self.options, executable_path=executable_path)
        else:
            self.browser = webdriver.Chrome(service = service, options=self.options)

    def __addOption(self, option):
        self.options.add_argument(option)

    def _waitFor(self, key, type, timeout=60):
        logger.info(f"Waiting for: {key}")
        wait = WebDriverWait(self.browser, timeout)
        try:
            element = wait.until(EC.presence_of_element_located((type, key)))
        except Exception as e:
            #call slack
            logger.error(f"Error: Element not found or timed out - {key}")
            self.browser.save_screenshot(os.path.join(sys.path[0], "Error.png"))
            raise
        return element

    def __waitForLink(self, cName):
        self._waitFor(cName, By.LINK_TEXT)
    
    def __waitForXPath(self, cName):
        self._waitFor(cName, By.XPATH)

    def __waitForClassLike(self, cName):
        self._waitFor(f"//button[contains(@class, '{cName}')]", By.XPATH)
    
    def clickOnLink(self, link): 
        self.__waitForLink(link)
        button = self.browser.find_element(By.LINK_TEXT, link)
        button.click()

    def writeInput(self, msg):
        self.__waitForXPath('//div[@aria-label="Type a message"]')
        actions = ActionChains(self.browser)
        textbox = self.browser.find_elements(By.XPATH, '//div[@role="textbox"]')[-1]
        textbox.send_keys(Keys.CONTROL + "a")
        textbox.send_keys(Keys.DELETE)
        
        for line in msg.split('\n'):
            actions.send_keys(line)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
        actions.perform()  

    def clickSend(self):
        self.__waitForClassLike("x1c4vz4f")
        send_button = self.browser.find_element(By.XPATH, "//button[contains(@class, 'x1c4vz4f')]")
        send_button.click()

    def isMessageSent(self):
        start_time = time.time()  # Capture time at start
        # Find all matching elements
        elements = self.browser.find_elements(By.CSS_SELECTOR, 'span[dir="auto"].x1rg5ohu.x16dsc37')
        message_sent = False
        # Get the last one
        if elements:
            last_element = elements[-1]
            last_timestamp_str = last_element.text
            #logger.info(f"Last timestamp:{last_element.text}")
            
            # Get current time
            now = datetime.now()
            # Parse both times as datetime objects (set today's date so they're comparable)
            today_str = now.strftime('%Y-%m-%d')
            last_timestamp_dt = datetime.now()
            try:
               #logger.info(f"last stamp: {today_str} {last_timestamp_str}")
               last_timestamp_dt = datetime.strptime(f"{today_str} {last_timestamp_str}", '%Y-%m-%d %H:%M')
            except Exception as e:
                #call slack
                logger.error(f"Error in timestamp format")
                raise
            
            # Difference in minutes
            difference = abs((now - last_timestamp_dt).total_seconds() / 60)
           
            if difference <= 1:
                #logger.info("Timestamps are the same or within 1 minute.")
                status = self.browser.find_elements(By.XPATH, '//span[@aria-label]')[-1].get_attribute("aria-label").strip()
                logger.info (f"status: -{status}-")
                while status.lower() != "delivered" and status.lower() != "sent":
                    try:
                        time.sleep(2)  # Wait 2 seconds before checking again
                        status = self.browser.find_elements(By.XPATH, '//span[@aria-label]')[-1].get_attribute("aria-label").strip()
                        logger.info (f"status: -{status}-")
                        current_time = time.time()
                        elapsed = current_time - start_time
                        if (elapsed > 60):
                            logger.error('More than 60 seconds passed')
                            break
                    except Exception as e:
                        logger.error(f"Error while waiting for the status to change {e}")

                message_sent = True
            else:
                logger.error(f"Timestamps differ by more than 1 minute ({difference:.1f} minutes).")
            
        else:
            logger.error("No matching elements found.")

        return message_sent
    
    def sendMessage(self, msg: str, phoneNumber: str):
        self.browser.get(f'https://wa.me/{phoneNumber}')
        logger.info(f'https://wa.me/{phoneNumber}')
        # time.sleep(150) 
        self.clickOnLink("Continue to Chat")
        self.clickOnLink("use WhatsApp Web")
        self.writeInput(msg)    
        self.clickSend()
        time.sleep(2) 
 

        return self.isMessageSent()
