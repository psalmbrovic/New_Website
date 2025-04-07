# Woven Finance Test Suite

This project contains a test suite for the Woven Finance website using Selenium and Pytest. The tests cover various functionalities of the website, including navigation, element visibility, and interactions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Test Structure](#test-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/psalmbrovic/New_Website.git
    cd New_Website
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the tests:**

    ```sh
    pytest --html=report.html
    ```

    This command will execute the tests and generate an HTML report.

2. **View the report:**

    Open `report.html` in your web browser to view the test results.

## Test Structure

- **`conftest.py`:** Contains the setup and teardown logic for the tests, including the browser fixture and screenshot-on-failure logic.
- **`test_suite.py`:** Contains the test cases for the Woven Finance website.

### Example Test Case

```python
def test_homepage(launchbrowser):
    driver = launchbrowser
    driver.get("https://woven.finance")
    driver.find_element(By.XPATH, '//*[@id="app"]/main[1]/div[1]/div/div[2]/a[1]').click()

    expected_text = "Streamline Your Payments with Woven Finance"
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[1]')
        )
    )

    assert element.text == expected_text, f"Expected '{expected_text}', but found '{element.text}'"