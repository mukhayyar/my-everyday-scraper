from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import os
from contextlib import contextmanager
from selenium.webdriver.support.ui import Select


load_dotenv()

# Setup logging
logging.basicConfig(
    filename='daily_claim.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@contextmanager
def wait_for_page_load(driver, timeout=30):
    try:
        old_page = driver.find_element(By.TAG_NAME, 'html')
        yield
        WebDriverWait(driver, timeout).until(EC.staleness_of(old_page))
    except Exception as e:
        logging.warning(f"Page load wait error: {str(e)}")

def claim_daily_reward(email, password):
    logging.info("Starting daily claim process")
    link = "https://kageherostudio.com/event/?event=daily"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(link)
        logging.info("Accessed website successfully")

        tombol_login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-login'))
        )
        tombol_login.click()
        logging.info("Clicked login button")

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'txtuserid'))
        )
        driver.execute_script(f"document.getElementsByName('txtuserid')[0].value = '{email}'")

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'txtpassword'))
        )
        driver.execute_script(f"document.getElementsByName('txtpassword')[0].value = '{password}'")
        logging.info("Filled login credentials")

        tombol_submit_login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#form-login-btnSubmit'))
        )
        
        tombol_submit_login.click()
        with wait_for_page_load(driver):
            logging.info("Submitted login form and waiting for refresh")

        time.sleep(5)  

        try:
            reward_claim = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.reward-content.dailyClaim.reward-star'))
            )
            reward_claim.click()
            logging.info("Successfully clicked the daily reward!")
            

            try:
                server_option = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//select/option[@value='3']"))
                )
                logging.info("Found the server option element using XPath")

                # Click directly on the option
                server_option.click()
                logging.info("Clicked on the desired server option")

                tombol_submit_server = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#form-server-btnSubmit'))
                )
                
                tombol_submit_server.click()

                # Wait for the alert to appear
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                logging.info(f"Alert detected with text: {alert_text}")

                # Click OK in the alert
                alert.accept()
                logging.info("Accepted the alert")
                
                with wait_for_page_load(driver):
                    logging.info("Submitted server selection and waiting for refresh")

                logging.info("Successfully claimed the daily reward!")
                time.sleep(5)  
                
            except TimeoutException:
                logging.error("Failed to find server selection after login. Login might have failed.")
            
        except TimeoutException:
            logging.warning("Could not find reward button. The reward might have been already claimed or the event has ended.")
            
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    finally:
        time.sleep(5)
        if driver:
            driver.quit()
            logging.info("Browser closed")

if __name__ == "__main__":
    email = os.getenv("MAIN_MAIL")
    password = os.getenv("MAIL_PASS_NH")
    print(email, password)
    claim_daily_reward(email, password)
