import time # Keep time for intentional pauses if absolutely needed
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.select import Select # Not used here
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os # For creating screenshots directory

BASE_URL = "https://woven.finance"

@pytest.fixture(scope="function") # <<< Changed scope to "function" for test isolation
def driver_instance(): # Renamed fixture for clarity
    chr_options = Options()
    # chr_options.add_experimental_option("detach", True) # Keep browser open after script finishes (useful for debugging)
    # chr_options.add_argument("--headless") # Optional: Run in headless mode
    chr_options.add_argument("--start-maximized") # Use argument for maximizing

    print("\nSetting up WebDriver...")
    # Let webdriver-manager find the correct driver version automatically
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chr_options)
    driver.implicitly_wait(5) # Basic implicit wait, but prefer explicit waits

    yield driver # Provide the driver instance to the test

    print("\nTearing down WebDriver...")
    driver.quit()

# Helper function to handle potential cookie banners, etc.
def accept_cookies_if_present(driver):
     try:
        # Adjust locator based on the actual cookie banner button
        cookie_button_xpath = "//button[contains(text(), 'Accept') or contains(text(), 'Okay') or contains(@id, 'cookie')]"
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, cookie_button_xpath))
        )
        print("Accepting cookies...")
        cookie_button.click()
        time.sleep(1) # Short pause after clicking
     except TimeoutException:
        print("Cookie banner not found or already accepted.")
     except Exception as e:
        print(f"Error handling cookie banner: {e}")


def test_homepage(driver_instance): # Use the fixture
    driver = driver_instance
    driver.get(BASE_URL)
    accept_cookies_if_present(driver) # Handle potential overlays

    # Using a potentially more stable locator based on text/structure if available
    # Adjust this XPath based on inspection
    expected_text = "Streamline Your Payments with Woven Finance"
    element_xpath = "//h1[contains(text(),'Streamline Your Payments')]" # Example: Target H1 containing the text
    try:
        element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[1]'))
        )
        # Using 'in' might be safer if exact spacing/newlines differ
        assert expected_text in element.text, f"Expected text containing '{expected_text}', but found '{element.text}'"
        print("Homepage test passed.")
    except TimeoutException:
        pytest.fail(f"Timed out waiting for homepage element: {element_xpath}")


def test_about_us(driver_instance):
    driver = driver_instance
    driver.get(BASE_URL)
    accept_cookies_if_present(driver)

    # Use Link Text which is generally robust
    about_us_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/a[2]'))
    )
    about_us_link.click()

    # Verify navigation by checking URL or a unique element on the About Us page
    WebDriverWait(driver, 10).until(EC.url_contains('/company'))
    assert '/about' in driver.current_url

    # Find an element unique to the about page for assertion
    expected_header_text = 'Central Bank of Nigeria licensed payment service provider that enables seamless online transactions for businesses and individuals.'

    header_element_xpath = "//h2[contains(text(), 'Central Bank of Nigeria licensed payment service provider that enables seamless online transactions for businesses and individuals.')]" # Adjust locator as needed
    header_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/a[2]'))
    )
    assert expected_header_text in header_element.text
    print("About Us test passed.")


def test_pricing(driver_instance):
    driver = driver_instance
    driver.get(BASE_URL)
    accept_cookies_if_present(driver)

    pricing_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Pricing'))
    )
    pricing_link.click()

    WebDriverWait(driver, 10).until(EC.url_contains('/pricing'))
    assert '/pricing' in driver.current_url

    # Example assertion for pricing page
    expected_text = "Pricing with you in mind"
    pricing_header_xpath = "//p[contains(text(), 'Pricing with you in mind')]" # Adjust locator
    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/main[1]/main[2]/main[1]/p[1]'))
    )
    assert expected_text in header.text
    print("Pricing test passed.")

# Add similar isolated tests for Developer Portal and FAQs, including assertions

def test_our_solutions_navigation(driver_instance): # Renamed for clarity
    driver = driver_instance
    driver.get(BASE_URL)
    accept_cookies_if_present(driver)

    # --- Hover ---
    # Find the element to hover over (e.g., by text or a more stable attribute)
    # Note: XPATH adjusted - you may need to refine this further by inspecting the element
    solutions_menu_xpath = "//div[contains(@class, 'links')]//div[contains(., 'Our Solution')]" # Example more robust xpath
    solution_element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, solutions_menu_xpath))
    )

    print("Hovering over Solutions menu...")
    actions = ActionChains(driver)
    actions.move_to_element(solution_element).perform()
    # Optional short pause ONLY if absolutely needed after hover for menu animation
    time.sleep(0.5) # Reduced pause, maybe remove entirely if EC.element_to_be_clickable works reliably

    # --- Click desired option ---
    # Target specific solution link by its text (most reliable)
    virtual_accounts_link_text = "Virtual Accounts"
    try:
        our_solution_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, virtual_accounts_link_text))
            # Alternative XPATH if Link Text fails (Relative to the hovered element if possible)
            # (By.XPATH, solutions_menu_xpath + "//following-sibling::div//a[contains(text(), 'Virtual Accounts')]")
        )
        print(f"Clicking on '{virtual_accounts_link_text}'...")
        our_solution_link.click()
    except StaleElementReferenceException:
        print("Stale element encountered, re-hovering and clicking...")
        # Re-find hover element and link
        solution_element = WebDriverWait(driver, 10).until(
           EC.visibility_of_element_located((By.XPATH, solutions_menu_xpath))
        )
        actions.move_to_element(solution_element).perform()
        time.sleep(0.5)
        our_solution_link = WebDriverWait(driver, 10).until(
             EC.element_to_be_clickable((By.LINK_TEXT, virtual_accounts_link_text))
        )
        our_solution_link.click()
    except TimeoutException:
         pytest.fail(f"Timed out waiting for the '{virtual_accounts_link_text}' link to be clickable after hover.")


    # --- Assert Correct Navigation ---
    # **CRUCIAL**: Replace 'virtual-accounts' and 'Virtual Accounts' with the
    #              actual URL part and expected Title/Header text of that page.
    expected_url_part = '/virtual-accounts' # <<< CHECK AND UPDATE THIS
    expected_title_part = 'Virtual Accounts' # <<< CHECK AND UPDATE THIS

    WebDriverWait(driver, 15).until(EC.url_contains(expected_url_part))
    assert expected_url_part in driver.current_url
    assert expected_title_part in driver.title # Check title
    print("Our Solutions navigation test passed.")


# Screenshot on failure hook (place in conftest.py is conventional, but here for completeness)
# Ensure 'screenshots' directory exists
SCREENSHOT_DIR = "screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
