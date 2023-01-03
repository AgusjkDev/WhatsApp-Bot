import requests
import os
import subprocess
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from qrcode import QRCode

from constants import BRAVE_PATH


def get_driver_versions() -> list[str] | None:
    html = BeautifulSoup(
        requests.get("https://chromedriver.chromium.org/downloads").content,
        "html.parser",
    )

    versions = []
    for v in html.find_all("strong")[1:]:
        text = v.text

        if "ChromeDriver" in text:
            versions.append(text.split(" ")[-1])

    return versions if versions else None


def get_brave_version() -> str | None:
    for f in os.listdir(BRAVE_PATH):
        if os.path.isdir(BRAVE_PATH + f"\\{f}") and len(f.split(".")) == 4:
            return f


def await_element_load(
    locator: tuple,
    driver_or_element: Chrome | WebElement,
    timeout: int | None = None,
) -> WebElement | None:
    while True:
        try:
            return WebDriverWait(
                driver_or_element, timeout if timeout else 5, poll_frequency=0.25
            ).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            if not timeout:
                continue

            return


def show_qr(qr_string=str) -> None:
    qr = QRCode(version=1, box_size=7, border=3)
    qr.add_data(qr_string)
    qr.make(fit=True)
    qr.make_image().show()


def close_qr() -> None:
    subprocess.call(
        "taskkill /im Microsoft.Photos.exe /f /t",
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
