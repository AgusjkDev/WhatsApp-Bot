import os

from classes import Bot
from constants import VERSION


def main():
    os.system(f"title WhatsApp Bot v{VERSION} by ShadeDev7")

    bot = None

    try:
        bot = Bot()

        while True:
            if bot.error:
                break

            if not bot.logged:
                bot.login()

                continue

            bot.handle_messages()
    except Exception as e:  # Only for development purposes
        import traceback

        traceback.print_exception(e)
        print("\n", e.__class__, "\n")

        pass

    if bot:
        bot.close()


if __name__ == "__main__":
    main()
