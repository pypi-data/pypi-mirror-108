# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_testing_library']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.0.0,<4.0.0', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'selenium-testing-library',
    'version': '2021.6.9b1',
    'description': 'A Python Selenium library inspired by the Testing Library',
    'long_description': '# Selenium Testing Library\n\nSlenium Testing Library (STL) is a Python library for Selenium inspired by the [Testing Library](https://testing-library.com/).\n\n```python\nfrom selenium import webdriver\nfrom selenium_testing_library import Screen\n\n\nscreen = Screen(webdriver.Chrome())\nscreen.driver.get("http://www.google.com/ncr")\nscreen.get_by_text("Accept").click()\nscreen.get_by_role("combobox").send_keys("Dogs" + Keys.RETURN)\n# Find waits until the results become available\nscreen.find_by_text("Dog - Wikipedia", timeout=5, poll_frequency=0.5)\nassert screen.query_by_text("Cats") is None\n```\n\n## API Parity with Testing Library\n\n### Queries\n\n| Testing Library          | STL                     | Status      |\n| ------------------------ | ----------------------- | ----------- |\n| `getBy`                  | `get_by`                | 🟢 Done     |\n| `queryBy`                | `query_by`              | 🟢 Done     |\n| `findBy`                 | `find_by`               | 🟢 Done     |\n| `getAllBy`               | `get_all_by`            | 🟢 Done     |\n| `queryAllBy`             | `query_all_by`          | 🟢 Done     |\n| `findAllBy`              | `find_all_by`           | 🟢 Done     |\n\nExamples:\n\n```python\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium_testing_library import Screen, locators\n\nscreen = Screen(webdriver.Chrome())\nscreen.get_by(locators.Css(".my_class"))  # locator classes are a shorthand for (By.CSS_SELECTOR, ".my_class"). All Selenium By.* options are supported\nscreen.query_by((By.ID, "my_id")) # you can use regular tuples/lists if you want to\nscreen.find_by(locators.Text("My text"), timeout=5, poll_frequency=0.5) # locators for searching through text also work\n```\n\n| Testing Library          | STL                     | Status      |\n| ------------------------ | ----------------------- | ----------- |\n| `ByRole`                 | `by_role`               | ⚠️ Partial  |\n| `ByLabelText`            | `by_label_text`         | ⚠️ Partial  |\n| `ByPlaceholderText`      | `by_placeholder_text`   | ⚠️ Partial  |\n| `ByText`                 | `by_text`               | ⚠️ Partial  |\n| `ByDisplayValue`         | `by_display_value`      | ⚠️ Partial |\n| `ByAltText`              | `by_alt_text`           | ⚠️ Partial  |\n| `ByTitle`                | `by_title`              | ⚠️ Partial |\n| `ByTestId`               | `by_test_id`            | ⚠️ Partial |\n| N/A                      | `by_css`                | 🟢 Done   |\n| N/A                      | `by_xpath`              | 🟢 Done   |\n\nExamples:\n\n```python\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium_testing_library import Screen, locators\n\nscreen = Screen(webdriver.Chrome())\nscreen.query_by_role("role_name")\nscreen.get_by_label_text("label text")\nscreen.find_all_by_text("my text", timeout=5, poll_frequency=0.5)\nscreen.get_all_by_alt_text("alt text")\n```\n\n### User Actions\n\n| Testing Library          | STL                     | Status          |\n| ------------------------ | ----------------------- | --------------- |\n| `fireEvent`              | `N/A`                   | ❌ Not Planned  |\n| `fireEvent[eventName]`   | `N/A`                   | ❌ Not Planned  |\n| `createEvent[eventName]` | `N/A`                   | ❌ Not Planned  |\n\nThere is currently no plan to support the event API of Testing Library. Use the methods on `WebElement` instead.\n\n| Testing Library             | STL                     | Status        |\n| --------------------------- | ----------------------- | ------------- |\n| `waitFor`                   | `wait_for`              | 🟢 Done       |\n| `waitForElementToBeRemoved` | `wait_for_stale`        | 🟢 Done       |\n\n```python\nfrom selenium import webdriver\nfrom selenium_testing_library import Screen, locators\n\nscreen = Screen(webdriver.Chrome())\n\n# Wait for the element to be clickable:\nelement = screen.get_by_text("Submit")\nscreen.wait_for(lambda _: element.is_enabled(), timeout=5, poll_frequency=0.5)\n# Wait for the element to be removed from the page:\nscreen.wait_for_stale(element)\n```\n\n## Local development\n\n```shell\npoetry install && poetry shell\n# Make sure `chromedriver` is in your PATH, download from https://chromedriver.chromium.org/downloads\n# run tests:\npytest --selenium-headless\n# run tests and display coverage info:\npytest --selenium-headless --cov=selenium_testing_library --cov-report html\n```\n',
    'author': 'Anže Pečar',
    'author_email': 'anze@pecar.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Smotko/selenium-testing-library',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
