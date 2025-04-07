from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
import os # For creating screenshots directory
from datetime import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")



@pytest.fixture(scope="module")  # Reset browser per test
def launchbrowser():
    chr_options = Options()
    global driver
    chr_options.add_experimental_option("detach", True)
    driver_path = ChromeDriverManager(driver_version="134.0.6998.166").install()

    driver = webdriver.Chrome(
        service=Service(driver_path),
        options=chr_options
    )
    driver.maximize_window()
    yield driver
    driver.quit()


def accept_cookies_if_present(driver):
    try:
        # Adjust locator based on the actual cookie banner button
        cookie_button_xpath = "//button[contains(text(), 'Accept') or contains(text(), 'Okay') or contains(@id, 'cookie')]"
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, cookie_button_xpath))
        )
        print("Accepting cookies...")
        cookie_button.click()
        time.sleep(1)  # Short pause after clicking
    except TimeoutException:
        print("Cookie banner not found or already accepted.")
    except Exception as e:
        print(f"Error handling cookie banner: {e}")


def test_homepage(launchbrowser):
    driver = launchbrowser
    driver.get("https://woven.finance")
    driver.find_element(By.XPATH,'//*[@id="app"]/main[1]/div[1]/div/div[2]/a[1]').click()


    # Wait for the element to be visible and assert text
    expected_text = "Streamline Your Payments with Woven Finance"
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[1]')
        )
    )

    assert element.text == expected_text, f"Expected '{expected_text}', but found '{element.text}'"

def test_about_us():
    #about_us
    driver.find_element(By.XPATH,'//*[@id="app"]/main[1]/div[1]/div/div[2]/a[2]').click()
    expected_text = "Central Bank of Nigeria licensed payment service provider that enables seamless online transactions for businesses and individuals."
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app"]/div/main/main[1]/main/p[2]')
        )
    )

def test_pricing():

    #pricing
    # driver.find_element(By.XPATH,'//*[@id="app"]/main[1]/div[1]/div/div[2]/a[3]').click()
    # expected_text = "Pricing with     you in mind"
    # element = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located(
    #         (By.XPATH, '//*[@id="app"]/div/main[1]/main[2]/main[1]/p[1]')
    #     )
    # )

    def test_pricing(launchbrowser):
        driver = launchbrowser
        # pricing
        driver.find_element(By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/a[3]').click()
        expected_text = "Pricing with you in mind"
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/main[1]/main[2]/main[1]/p[1]')
            )
        )
        assert element.text == expected_text  # <-- Add assertion

def test_Developer_Portal():
    original_window = driver.current_window_handle
    link = driver.find_element(By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/a[4]')
    link.click()
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    all_windows = driver.window_handles
    new_window = [window for window in all_windows if window != original_window][0]
    driver.switch_to.window(new_window)
    print("New Tab Title:", driver.title)
    driver.close()
    driver.switch_to.window(original_window)


def test_FAQs():

    # FAQs
    driver.find_element(By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/a[5]').click()
    expected_text = "Frequently Asked Questions"
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/div[1]')
        )
    )

def test_our_solutions():

    # Locate the element you want to hover over
    element_to_hover = driver.find_element(By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/div/div[1]/img[2]')
    actions = ActionChains(driver)
    actions.move_to_element(element_to_hover).perform()

    sub_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/div/div[2]/a[4]'))
    )
    sub_element.click()


