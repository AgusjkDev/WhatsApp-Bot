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
    CHAT_HEADER = (By.XPATH, '//header[@data-testid="conversation-header"]')
    CONTACT_INFO = (By.XPATH, '//div[@data-testid="contact-info-drawer"]')
    BUSINESS_ACCOUNT_NAME = (
        By.XPATH,
        ".//div/section/div[1]/div[3]/div[1]/div[1]/span",
    )
    BUSINESS_ACCOUNT_NUMBER = (
        By.XPATH,
        './/div[@data-testid="container_with_separator"]/div/div/span/span',
    )
    CONTACT_NAME_OR_NUMBER = (By.XPATH, ".//div/section/div[1]/div[2]/h2/span")
    CONTACT_ALIAS_OR_NUMBER = (By.XPATH, ".//div/section/div[1]/div[2]/div/span/span")
    CLOSE_CONTACT_INFO = (By.XPATH, '//div[@data-testid="btn-closer-drawer"]')
    MESSAGE_CONTAINER = (By.XPATH, '//div[contains(@class, "message-in")]')
    TEXT_CONTAINER = (
        By.XPATH,
        './/div/div[1]/div[1][not(@data-testid="poll-bubble")]/div[1]/div/span[1]/span',
    )
    EMOJIS = (By.XPATH, ".//img[@data-plain-text]")
    ONLY_EMOJIS = (
        By.XPATH,
        ".//div/div[1]/div[1]/div[1]/div/div/span/img[@data-plain-text]",
    )
    AUDIO = (By.XPATH, './/span[@data-testid="audio-play"]')
    STICKER = (
        By.XPATH,
        './/div/div[1]/span/descendant::img[@draggable="false" and not(@crossorigin)]',
    )
    IMAGE_CONTAINER = (By.XPATH, './/div[@data-testid="image-thumb"]')
    VIDEO = (By.XPATH, './/div[@data-testid="video-content"]')
    GIF = (By.XPATH, './/div[@data-testid="media-state-gif-icon"]')
    VIEW_ONCE = (By.XPATH, './/span[@data-testid="view-once-sunset"]')
    DOCUMENT = (By.XPATH, './/button[@data-testid="document-thumb"]')
    LOCATION = (By.XPATH, './/a[@dir="auto" and @data-plain-text]')
    CONTACT = (By.XPATH, './/div[@data-testid="vcard-msg"]')
    POLL = (By.XPATH, './/div[@data-testid="poll-bubble"]')
    DELETED = (By.XPATH, './/span[@data-testid="recalled"]')
    INPUT_BOX = (By.XPATH, '//div[@data-testid="conversation-compose-box-input"]')
