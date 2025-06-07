#!/usr/bin/env python
import argparse
import json
import os
import pathlib
import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


def main():
    """Entry"""
    # Get the default ctrl dashboard URL
    symbols_path = os.getenv("TESTRUN_SYMBOLS")
    if symbols_path is not None:
        with open(symbols_path) as stream:
            symbols = json.load(stream)
        ctrl_dashboard_url = symbols["ctrl_dashboard_url"]

    # Get Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--ctrl_dashboard_url", default=ctrl_dashboard_url)
    arguments = parser.parse_args()
    ctrl_dashboard_url = arguments.ctrl_dashboard_url

    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")

    browser = Chrome(options=options)
    browser.get(f"{ctrl_dashboard_url}/login")
    time.sleep(1)

    # Fill the form
    email_input = browser.find_element(By.CSS_SELECTOR, "input")
    email_input.send_keys("admin@nginx.test\tTestenv12#")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button")
    submit_button.submit()
    time.sleep(1)

    browser.get(f"{ctrl_dashboard_url}/services/envs/")


if __name__ == "__main__":
    main()
