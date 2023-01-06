import psycopg2
from contextlib import contextmanager
from typing import Any

from .Logger import Logger
from constants import DB_CONFIG

from traceback import print_exception  # Only for development purposes


class Database:
    # Private values
    __connection: Any

    # Public values
    connected: bool

    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        self.connected = False

        if not all(DB_CONFIG.values()):
            return self.__logger.log(
                f"Please add the database credentials in '.env' file!", "ERROR"
            )

        self.__logger.log("Initializing Database...", "DEBUG")

        self.__connection = psycopg2.connect(**DB_CONFIG)
        self.connected = True

        self.__logger.log("Database initialized.", "EVENT")

    @contextmanager
    def __get_cursor(self):
        cursor = self.__connection.cursor()

        try:
            yield cursor
        finally:
            cursor.close()

    def is_number_banned(self, number: str) -> bool | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(f"SELECT * FROM banned_users WHERE number = '{number}';")
                is_banned = cursor.fetchone()

                self.__connection.commit()

                return bool(is_banned)
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

                return

    def get_user_role(self, number: str) -> str | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"SELECT role_name FROM user_roles WHERE number = '{number}';"
                )
                data = cursor.fetchone()
                if not data:
                    return

                self.__connection.commit()

                return data[0]
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

                return

    def register_user(self, number: str, name: str) -> None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        INSERT INTO users (number, user_name)
                        SELECT '{number}', '{name}'
                        WHERE NOT EXISTS (
                            SELECT number FROM users WHERE number = '{number}'
                        );
                    """
                )

                self.__connection.commit()
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

                return

    def executed_command(self, number: str, name: str, command_name: str) -> None:
        with self.__get_cursor() as cursor:
            try:
                self.register_user(number, name)

                cursor.execute(
                    f"""
                        INSERT INTO executed_commands (number, command_name)
                        VALUES ('{number}', '{command_name}');
                    """
                )

                self.__connection.commit()
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

                return

    def close(self) -> None:
        self.__logger.log("Closing Database session...", "CLOSE")

        self.__connection.close()
