from selenium.webdriver.common.by import By


class Locators:
    QR = (By.XPATH, '//div[@data-testid="qrcode"]')
    HEADER = (By.XPATH, '//header[@data-testid="chatlist-header"]')
