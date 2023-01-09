import os

from .Language import Language
from languages import English, French, German, Italian, Portuguese, Spanish
from constants import VERSION

LANGUAGES: list[Language] = [
    English(),
    French(),
    German(),
    Italian(),
    Portuguese(),
    Spanish(),
]


class LanguageHandler:
    @staticmethod
    def get_language() -> Language:
        try:
            languages_length = len(LANGUAGES)
            while True:
                print(f"Welcome to WhatsApp bot v{VERSION} by AgusjkDev!")
                print("Please select your desired language and press [ENTER]:")
                print(
                    "\n".join(
                        [
                            f"{i}. {language}"
                            for i, language in enumerate(LANGUAGES, start=1)
                        ]
                    )
                )

                try:
                    option = int(input("\n>> "))
                except ValueError:
                    option = None

                if not option or (option < 1 or option > languages_length):
                    print("Invalid option, try again...")
                    os.system("pause")
                    os.system("cls")

                    continue

                os.system("cls")

                return LANGUAGES[option - 1]

        except:
            exit(-1)
