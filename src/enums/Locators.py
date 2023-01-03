from selenium.webdriver.common.by import By


class Locators:
    QR = (By.XPATH, '//div[@data-testid="qrcode"]')
    HEADER = (By.XPATH, '//header[@data-testid="chatlist-header"]')
    PINNED_CHAT = (
        By.XPATH,
        '//div[@data-testid="cell-frame-container"]/div[2]/div[2]/div[2]/span[1]/div/span[@data-testid="pinned2"]',
    )
    NEW_CHAT = (
        By.XPATH,
        '//div[@data-testid="cell-frame-container"]/div[2]/div[2]/div[2]/span[1]/div/span[@aria-label]',
    )
    NEW_CHAT_CONTAINER = (By.XPATH, "../../../../..")
    CHAT_HEADER = (By.XPATH, '//header[@data-testid="conversation-header"]')
    CHAT_INFO = (By.XPATH, '//div[@data-testid="contact-info-drawer"]')
    BUSINESS_NAME = (By.XPATH, ".//div/section/div[1]/div[3]/div[1]/div[1]/span")
    BUSINESS_NUMBER = (
        By.XPATH,
        './/div[@data-testid="container_with_separator"]/div/div/span/span',
    )
    PERSON_NAME = (By.XPATH, ".//div/section/div[1]/div[2]/div/span/span")
    PERSON_NUMBER = (By.XPATH, ".//div/section/div[1]/div[2]/h2/span")
    MESSAGE_CONTAINER = (By.XPATH, '//div[contains(@class, "message-in")]/div/div[1]')
    MESSAGE_WITH_TEXT = (
        By.XPATH,
        './div[not(contains(@data-testid, "poll-bubble"))]/div[1]/div/span[1]/span',
    )
    EMOJIS = (By.XPATH, "//img[@data-plain-text]")
    IMAGE_WITH_TEXT_CONTAINER = (
        By.XPATH,
        './div[1]/div/div[@data-testid="image-thumb"]/../div[2]/div/span[1]/span/../../../../div[@data-testid="image-thumb"]',
    )
    IMAGE_WITH_TEXT = (By.XPATH, './div/div/img[@alt and contains(@src, "blob")]')
    INPUT_BOX = (By.XPATH, '//div[@data-testid="conversation-compose-box-input"]')
    EMOJI_MENU = (By.XPATH, '//button[@data-testid="compose-btn-emoji"]')
    FILE_INPUT = (By.XPATH, '//input[@type="file"]')
    SEND_BUTTON = (By.XPATH, '//span[@data-testid="send"]/..')
    PENDING_MESSAGE = (By.XPATH, '//span[@data-testid="msg-time"]')
