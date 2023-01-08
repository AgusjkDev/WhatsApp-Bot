import requests
import os
import psutil
import time
import subprocess
import phonenumbers
import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from datetime import datetime

from traceback import print_exception  # Only for development purposes

from constants import BRAVE_PATH, TEMP_FOLDER


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


def open_qr(qr_image_path: str) -> list[int]:
    old_qr = Image.open(qr_image_path)
    width, height = old_qr.size

    # Create a new QR code image but with padding.
    new_qr = Image.new(old_qr.mode, (width + 50, height + 50), (255, 255, 255))
    new_qr.paste(old_qr, (25, 25))

    processes_before_showing = [p.pid for p in psutil.process_iter()]
    new_qr.show()
    os.remove(qr_image_path)

    time.sleep(0.5)

    return [
        p.pid for p in psutil.process_iter() if p.pid not in processes_before_showing
    ]


def kill_process(*pids: int) -> None:
    for pid in pids:
        subprocess.call(
            f"taskkill /pid {pid} /f /t",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )


def normalize_phone_number(number: str) -> str:
    return "".join([c for c in number if c.isdigit()])


def is_valid_phone_number(phone_number: str) -> bool:
    try:
        return phonenumbers.is_valid_number(phonenumbers.parse(phone_number))
    except phonenumbers.NumberParseException:
        return False


def format_date(date: datetime) -> str:
    return date.strftime("%H:%M:%S, %d/%m/%Y")


def download_random_image() -> str | None:
    image_path = f"{TEMP_FOLDER}\\temp-{int(time.time())}.webp"

    try:
        urllib.request.urlretrieve("https://picsum.photos/1080.webp", image_path)

        return image_path
    except Exception as e:
        print_exception(e)


def get_random_quote() -> dict[str, str] | None:
    try:
        request = requests.get("https://zenquotes.io/api/random")
        if request.status_code != 200:
            return

        response = request.json()[0]

        return {"content": response["q"], "author": response["a"]}
    except Exception as e:
        print_exception(e)
