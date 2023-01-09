import os
import time
from selenium.common.exceptions import NoSuchWindowException

from classes import LanguageHandler, Logger, Database, Bot
from constants import VERSION

from traceback import print_exception  # Only for development purposes


def main():
    os.system(f"title WhatsApp Bot v{VERSION} by AgusjkDev")

    language = LanguageHandler.get_language()
    logger = Logger()
    db, bot = None, None

    logger.log(language.MAIN_STARTING.format(VERSION), "DEBUG")
    time.sleep(3)

    try:
        db = Database(language, logger)
        if db.connected:
            bot = Bot(language, logger, db)

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
        logger.log(language.MAIN_UNEXPECTED_ERROR, "ERROR")

        print_exception(e)

    if db:
        db.close()

    if bot:
        bot.close()


if __name__ == "__main__":
    main()
