from dotenv import dotenv_values

environ = dotenv_values(".env")

VERSION = "0.0.0"
BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application"
DRIVER_ARGUMENTS = [
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "--mute-audio",
    "--disable-extensions",
    "--disable-dev-sh-usage",
    "--disable-gpu",
    "log-level=3",
]
COMMAND_SYMBOL = "/"
DB_CONFIG = {
    "host": environ.get("DB_HOST"),
    "database": environ.get("DB_NAME"),
    "user": environ.get("DB_USERNAME"),
    "password": environ.get("DB_PASSWORD"),
}
