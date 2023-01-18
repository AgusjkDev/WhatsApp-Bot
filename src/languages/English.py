from classes.Language import Language


class English(Language):
    MAIN_STARTING = "Starting WhatsApp Bot v{}..."
    MAIN_UNEXPECTED_ERROR = "There was an unexpected error!"
    DB_NO_CREDENTIALS = "Please add the database credentials in '.env' file!"
    DB_INITIALIZING = "Initializing Database..."
    DB_COULDNT_INITIALIZE = "Couldn't initialize the database!"
    DB_INITIALIZED = "Database initialized."
    DB_CLOSING = "Closing database session..."
    BOT_DRIVER_NOT_FOUND_DOWNLOADING = "Driver not found! Downloading it..."
    BOT_DRIVER_COULDNT_DOWNLOAD = "Couldn't download the driver!"
    BOT_DRIVER_DOWNLOADED = "Driver downloaded successfully."
    BOT_DRIVER_INITIALIZING = "Initializing driver..."
    BOT_DRIVER_INVALID_VERSION_DOWNLOADING = (
        "Invalid driver version! Downloading the correct one..."
    )
    BOT_DRIVER_INITIALIZED = "Driver initialized."
    BOT_PINNED_CHAT_COULDNT_FIND_RETRYING = (
        "Couldn't find a pinned chat to focus on! Trying again in {} seconds... ({}/{})"
    )
    BOT_PINNED_CHAT_COULDNT_FIND = "Couldn't find a pinned chat to focus on. ({}/{})"
    BOT_LOGIN_TRYING = "Trying to log in..."
    BOT_LOGIN_ALREADY_LOGGED = "Already logged in."
    BOT_LOGIN_AWAITING_QR_SCAN = "Awaiting QR code scan..."
    BOT_LOGIN_QR_SCANNED = "Scanned, logging in..."
    BOT_LOGIN_LOGGED = "Logged in."
    BOT_LOGIN_QR_ERROR = "There was an error with the QR code! Trying again..."
    BOT_LOGIN_COULDNT_LOGIN_RETRYING = (
        "Couldn't log in! Trying again in {} seconds... ({}/{})"
    )
    BOT_LOGIN_COULDNT_LOGIN = "Couldn't log in."
    BOT_MESSAGE_HANDLING = "Handling messages..."
    BOT_MESSAGE_HANDLING_ERROR = "There was an error handling a message!"
    BOT_MESSAGE_HANDLING_SPAMMING = "{} is probably spamming messages!"
    BOT_CLOSE_CLOSING = "Closing driver instance..."
    COMMAND_HANDLER_REGISTERING = "Registering {} command: {}..."
    COMMAND_HANDLER_EXECUTED_COMMAND = "{} ({}) executed a command in {}s: {}"
    COMMAND_HANDLER_EXECUTING_ERROR = "There was an error executing command: {}"

    def __repr__(self) -> str:
        return "English"
