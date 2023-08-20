from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageChops
from io import BytesIO
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

api_url = "https://flights-api.buraky.workers.dev/"
flights = {}

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://flights-app.pages.dev/")


def test_same_input():
    try:
        # Locate "From" and "To" input fields
        from_input = driver.find_element(By.ID, "headlessui-combobox-input-:Rq9lla:")
        to_input = driver.find_element(By.ID, "headlessui-combobox-input-:Rqhlla:")

        # Clear any pre-filled values
        from_input.clear()
        to_input.clear()

        # Enter the same location for both inputs
        location = "IST"
        from_input.send_keys(location)
        to_input.send_keys(location)

        # Take a screenshot before pressing Enter
        screenshot_before = Image.open(BytesIO(driver.get_screenshot_as_png()))

        # Press Enter in the "To" input field
        from_input.send_keys(Keys.ENTER)
        to_input.send_keys(Keys.ENTER)

        # Take a screenshot after pressing Enter
        screenshot_after = Image.open(BytesIO(driver.get_screenshot_as_png()))

        diff = ImageChops.difference(screenshot_before, screenshot_after)
        if diff.getbbox() is None:
            print("Test Result: Same text should not be entered. There should be an error message showing about it!")
        else:
            print("Test Result: Visual change detected. Bug not detected.")

    except Exception as e:
        print("An error occurred:", e)



def test_flight_amount():
    try:
        # Locate "From" and "To" input fields
        from_input = driver.find_element(By.ID, "headlessui-combobox-input-:Rq9lla:")
        to_input = driver.find_element(By.ID, "headlessui-combobox-input-:Rqhlla:")

        for key in flights:

            # Get the flight departure and destination cities
            splittedValue = key.split("-")
            from_city = splittedValue[0]
            to_city = splittedValue[1]

            # Clear any pre-filled values
            from_input.clear()
            to_input.clear()

            # Enter departure and destination cities
            from_input.send_keys(from_city)
            to_input.send_keys(to_city)

            # Press Enter in the input fields
            to_input.send_keys(Keys.ENTER)
            from_input.send_keys(Keys.ENTER)

            # Wait for the "Found X items" message to appear
            wait = WebDriverWait(driver, 5)
            found_items_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Found')]")))

            text = found_items_message.text
            parts = text.split()
            x_value = int(parts[1])

            # Get the flights
            flight_boxes = driver.find_elements(By.XPATH, "//li[contains(@class, 'overflow-hidden')]")

            # Perform the test
            if x_value != len(flight_boxes):
                print(f"Test Failed. Expected {x_value} items but found {len(flight_boxes)} items. Bug detected!")
                break
        
        print("Number of flights and listed flights are equal for all. Test passed!")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()


# This functions stores all the flight destinations in a dictionary
def setup_fnc():
    response = requests.get(api_url)
    data = response.json()
    for item in data["data"]:
        dictKey = item["from"] + "-" + item['to']
        flights[dictKey] = flights.get(dictKey, 0) + 1


if __name__ == "__main__":
    test_same_input()
    setup_fnc()
    test_flight_amount()