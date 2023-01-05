import os
import time
from selenium.common.exceptions import NoSuchWindowException

from classes import Logger, Database, Bot
from constants import VERSION

from traceback import print_exception  # Only for development purposes


def main():
    os.system(f"title WhatsApp Bot v{VERSION} by ShadeDev7")

    logger = Logger()
    db, bot = None, None

    logger.log(f"Starting WhatsApp Bot v{VERSION}...", "DEBUG")
    time.sleep(3)

    try:
        db = Database(logger)
        if db.connected:
            bot = Bot(logger, db)

            while True:
                if bot.error:
                    break

                if not bot.logged:
                    bot.login()

                    continue

                bot.handle_messages()

    except (KeyboardInterrupt, NoSuchWindowException):
        pass

    except BaseException as e:
        logger.log("There was an unexpected error!", "ERROR")

        print_exception(e)

    if db:
        db.close()

    if bot:
        bot.close()


if __name__ == "__main__":
    main()
