import unittest
from django.test import TestCase
from django.shortcuts import reverse
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class seliumtesting(unittest.TestCase):
    # declare variable to store the URL to be visited
    base_url="https://www.plan-your-journey.eu"

    # --- Pre - Condition ---
    def setUp(self):
        # declare and initialize driver variable
        self.driver=webdriver.Chrome(ChromeDriverManager().install())
        # browser should be loaded in maximized window
        self.driver.maximize_window()
        # driver should wait implicitly for a given duration, for the element under consideration to load.
        # to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
        self.driver.implicitly_wait(10)  # 10 is in seconds

    # --- Steps ---
    def test_realtime(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url)

        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="realtime-tab"]')))
        element.click()

        # look for the input box and enter 123
        user_input = self.driver.find_element_by_id("Stop-number")
        user_input.send_keys(6245)

        # click the search button
        button=self.driver.find_element_by_id("real-time-button")
        button.click()
        time.sleep(5)

    # --- Steps ---
    def test_leapcard(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url)

        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leap-tab"]')))
        element.click()

        # look for the logging box and enter the login details
        user_input = self.driver.find_element_by_id("leap-user")
        user_input.send_keys('testing@outlook.com')

        # look for the password input box and enter the password
        user_password = self.driver.find_element_by_id("leap-password")
        user_password.send_keys("testing")

        # click the  button
        button=self.driver.find_element_by_id("leap-login-button")
        button.click()
        time.sleep(5)

    def test_routeplanner(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url)

        # to enter orgin adress, we need to locate the search textbox
        user_origin=self.driver.find_element_by_id("origin")
        user_origin.send_keys('UCD Sports Centre, Belfield, Dublin, Ireland')

        user_destination = self.driver.find_element_by_id("destination")
        user_destination.send_keys('Ballsbridge, Dublin, Ireland')

        button=self.driver.find_element_by_id("go")
        button.click()

        time.sleep(4)

    # --- Steps ---
    def test_tourist(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url)

        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tourist-tab"]')))
        element.click()
        # input the origin destination
        user_origin = self.driver.find_element_by_id("origin-tourist")
        user_origin.send_keys('Ballsbridge, Dublin, Ireland')

        # look for the check  box and click it
        checkbox = self.driver.find_element_by_id("coffee-shops")
        checkbox.click()

        time.sleep(5)

    def test_allroutes(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url)

        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allroutes-tab"]')))
        element.click()

        user_input = self.driver.find_element_by_id("estimator-route")
        user_input.send_keys('151 towards Bargy Road')
        user_input.click()

        # select the origin option
        x=(self.driver.find_element_by_id('estimator-origin'))
        x.click()

        origin=Select(self.driver.find_element_by_id('estimator-origin'))
        origin.select_by_index(4)

        time.sleep(1)

        # select the destination option
        destination = Select(self.driver.find_element_by_id('estimator-destination'))
        destination.select_by_index(8)

        # click on the go button
        button = self.driver.find_element_by_id('stop-to-stop-go')
        button.click()

        time.sleep(5)

    # --- Post - Condition ---
    def tearDown(self):
        # to close the browser
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
