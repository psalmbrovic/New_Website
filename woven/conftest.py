# conftest.py
import pytest
import os
from datetime import datetime

# Define the screenshot directory here
SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        # Create the directory if it doesn't exist
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

        driver = item.funcargs["launchbrowser"]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"failure_{item.name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)

        # Attach screenshot to HTML report
        extras.append(pytest_html.extras.png(screenshot_path))

    report.extras = extras






# import os
# from datetime import datetime
#
# import pytest
#
# SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#
#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#         try:
#             # Get the driver instance from the test item's fixture request
#             # if "driver_instance" in item.funcargs:
#             #     driver = item.funcargs["driver_instance"]
#             #     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             if "driver" in item.funcargs:  # Use your correct fixture name
#                 driver = item.funcargs["driver"]
#                 print(f"DEBUG: Found driver object: {driver}")  # Add this line
#                 timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                 # Sanitize test name for filename
#                 test_name = item.name.replace("[", "_").replace("]", "").replace(" ", "_")
#                 screenshot_path = os.path.join(SCREENSHOT_DIR, f"failure_{test_name}_{timestamp}.png")
#                 driver.save_screenshot(screenshot_path)
#                 print(f"\nScreenshot saved for failed test '{item.name}': {screenshot_path}")
#         except Exception as e:
#             print(f"Error taking screenshot: {e}")
#
# # conftest.py
# # import pytest
# # from selenium import webdriver
# #
# #
# # @pytest.hookimpl(hookwrapper=True)
# # def pytest_runtest_report(item, call):
# #     pytest_html = item.config.pluginmanager.getplugin("html")
# #     outcome = yield
# #     report = outcome.get_result()
# #     extra = getattr(report, "extra", [])
# #
# #     if report.when == "call" and report.failed:
# #         driver = item.funcargs["browser"]
# #         screenshot = driver.get_screenshot_as_png()
# #         extra.append(pytest_html.extras.image(screenshot, "Failure Screenshot"))
# #
# #     report.extra = extra