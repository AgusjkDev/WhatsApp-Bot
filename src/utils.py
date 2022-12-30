import requests
import os
from bs4 import BeautifulSoup

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
