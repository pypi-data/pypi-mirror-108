# cheesefactory_postgres/__init__.py

import logging
from typing import List, Union
import psycopg2
from psycopg2 import extras as pg_extras

logger = logging.getLogger(__name__)


class CfPostgres:
    def __init__(self, autocommit: bool = False):
        self.connection = None
        self.cursor = None
        self.autocommit = autocommit

    #
    # CLASS METHODS
    #
    @classmethod
    def connect(cls, host: str = None, port: Union[int, str] = None, database: str = None, user: str = None,
                password: str = None, autocommit: bool = False):
        """Connect to PostgreSQL database.

        Args:
            host: Postgres database hostname/IP
            port: Postgres database port.
            database: Postgres database.
            user: Postgres database username.
            password: Postgres database password.
            autocommit: Enable PostgreSQL autocommit.
        """
        postgres = cls()
        postgres.autocommit = autocommit
        postgres._connect(host=host, port=port, database=database, user=user, password=password)
        return postgres

    #
    # PROTECTED METHODS
    #

    def _connect(self, host: str = None, port: Union[int, str] = None, database: str = None, user: str = None,
                 password: str = None):
        """Connect to PostgreSQL database."""
        logger.debug(f'Connecting to {user}@{host}:{port}/{database}')
        self.connection = psycopg2.connect(
            f'host={host} port={str(port)} dbname={database} user={user} password={password}'
        )
        self.connection.set_session(autocommit=self.autocommit)
        self.cursor = self.connection.cursor()

    #
    # PUBLIC METHODS
    #

    def close(self):
        """Close cursor and connection."""
        self.cursor.close()
        self.connection.close()

    def commit(self):
        """Commit changes. Only useful if autocommit=False."""
        self.connection.commit()

    def execute(self, query: str = None, dict_cursor: bool = False, fetch: bool = False,
                query_vars: dict = None) -> List:
        """Execute SQL and optionally fetch results.

        Args:
            dict_cursor: Use a psycopg2 dict cursor?
            fetch: Fetch the results?
            query: PostgreSQL query
            query_vars: If query contains variable placeholder, these are the values
        """
        results = None

        # Cursor type needs to be set before execute
        cursor = self.cursor
        if fetch is True and dict_cursor is True:
            cursor = self.connection.cursor(cursor_factory=pg_extras.DictCursor)

        cursor.execute(query, query_vars)

        if fetch is True:
            results = cursor.fetchall()

        return results
