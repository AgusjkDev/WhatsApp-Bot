import psycopg2
from psycopg2.errors import ForeignKeyViolation
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from .Language import Language
from .Logger import Logger
from utils import format_date
from constants import DB_CONFIG

from traceback import print_exception  # Only for development purposes


class Database:
    # Private values
    __language: Language
    __logger: Logger
    __connection: Any

    # Public values
    connected: bool

    def __init__(self, language: Language, logger: Logger) -> None:
        self.__language = language
        self.__logger = logger
        self.connected = False

        if not all(DB_CONFIG.values()):
            return self.__logger.log(self.__language.DB_NO_CREDENTIALS, "ERROR")

        self.__logger.log(self.__language.DB_INITIALIZING, "DEBUG")

        try:
            self.__connection = psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError:
            return self.__logger.log(self.__language.DB_COULDNT_INITIALIZE, "ERROR")

        self.connected = True

        self.__logger.log(self.__language.DB_INITIALIZED, "EVENT")

    @contextmanager
    def __get_cursor(self):
        cursor = self.__connection.cursor()

        try:
            yield cursor
        finally:
            cursor.close()

    def is_user_banned(self, number: str) -> bool | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        SELECT * FROM banned_users
                        WHERE number = '{number}';
                    """
                )
                is_banned = cursor.fetchone()

                self.__connection.commit()

                return bool(is_banned)
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def get_user_role(self, number: str) -> str | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        SELECT role_name FROM user_roles
                        WHERE number = '{number}';
                    """
                )
                data = cursor.fetchone()
                if not data:
                    return

                self.__connection.commit()

                return data[0]
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def get_user_command_history(
        self, number: str, limit: int
    ) -> list[tuple[str, str]] | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        SELECT command_name, execution_date
                        FROM executed_commands
                        WHERE number = '{number}'
                        ORDER BY execution_date DESC
                        LIMIT {limit};
                    """
                )
                data = cursor.fetchall()
                if not data:
                    return

                self.__connection.commit()

                return [(col[0], format_date(col[1])) for col in data]
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def get_command_executions(self, command_name: str) -> int | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        SELECT times_executed
                        FROM commands
                        WHERE command_name = '{command_name}';
                    """
                )
                data = cursor.fetchone()
                if not data:
                    return

                self.__connection.commit()

                return data[0]
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def ban_user(self, number: str, reason: str) -> bool | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        INSERT INTO banned_users (number, reason)
                        VALUES ('{number}', '{reason}');
                    """
                )

                self.__connection.commit()

                return True
            except ForeignKeyViolation:
                self.__connection.rollback()

                return False
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def unban_user(self, number: str) -> bool | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        DELETE FROM banned_users
                        WHERE number = '{number}';
                    """
                )

                self.__connection.commit()

                return bool(cursor.rowcount)
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def set_user_role(self, number: str, role_name: str) -> bool | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        UPDATE user_roles
                        SET role_name = '{role_name}'
                        WHERE number = '{number}';
                    """
                )

                self.__connection.commit()

                return bool(cursor.rowcount)
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def get_user_information(self, number: str) -> list[str | int | bool] | list | None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        SELECT u.user_name, u.creation_date, ur.role_name, ur.grant_date, COUNT(ec.command_name) as executed_commands,
                        CASE WHEN bu.number IS NOT NULL THEN TRUE ELSE FALSE END as is_banned
                        FROM users u
                        INNER JOIN user_roles ur ON u.number = ur.number
                        INNER JOIN executed_commands ec ON u.number = ec.number
                        LEFT JOIN banned_users bu ON u.number = bu.number
                        WHERE u.number = '{number}'
                        GROUP BY u.user_name, u.creation_date, ur.role_name, ur.grant_date, bu.number
                        LIMIT 1;
                    """
                )
                data = cursor.fetchone()
                if not data:
                    return []

                self.__connection.commit()

                return [
                    col if type(col) != datetime else format_date(col) for col in data
                ]
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def register_user(self, number: str, user_name: str) -> None:
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    f"""
                        INSERT INTO users (number, user_name)
                        SELECT '{number}', '{user_name}'
                        WHERE NOT EXISTS (
                            SELECT number FROM users WHERE number = '{number}'
                        );
                    """
                )

                self.__connection.commit()
            except BaseException as e:
                print_exception(e)

                self.__connection.rollback()

    def executed_command(self, number: str, user_name: str, command_name: str) -> None:
        with self.__get_cursor() as cursor:
            try:
                self.register_user(number, user_name)

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

    def close(self) -> None:
        self.__logger.log(self.__language.DB_CLOSING, "CLOSE")

        self.__connection.close()
