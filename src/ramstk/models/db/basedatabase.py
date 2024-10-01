# -*- coding: utf-8 -*-
#
#       ramstk.models.db.basedatabase.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Base Database Module."""

# Standard Library Imports
import contextlib
import sqlite3
from typing import Any, Dict, List, Optional, Sequence, TextIO, Tuple

# Third Party Imports
import psycopg2  # type: ignore
from psycopg2 import sql  # type: ignore
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pubsub import pub
from sqlalchemy import Row, create_engine, exc
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import query, scoped_session, sessionmaker  # type: ignore
from sqlalchemy.orm.exc import FlushError  # type: ignore
from sqlalchemy.sql import text

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError


def do_create_postgres_db(database: Dict[str, str], sql_file: TextIO) -> None:
    """Create a postgres database.

    :param dict database: the database connection information.
    :param TextIO sql_file: the file containing the SQL statements used to
        create the database.
    :return: None
    """

    def _connect_to_db(database_: Dict[str, str]) -> psycopg2.extensions.connection:
        """Create a database connection.

        :param database_: dictionary with database connection information.
        :type database_: dict
        :return: a psycopg2 connection.
        :rtype: psycopg2.extensions.connection
        """
        return psycopg2.connect(
            host=database_["host"],
            database=database_["database"],
            user=database_["user"],
            password=database_["password"],
        )

    try:
        # Step 1: Connect to the default 'postgres' database and create a new one.
        _conn = _connect_to_db(
            {
                "host": database["host"],
                "user": database["user"],
                "password": database["password"],
                "database": "postgres",
            }
        )
        _conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with _conn.cursor() as _cursor:
            _cursor.execute(
                sql.SQL("DROP DATABASE IF EXISTS {}").format(
                    sql.Identifier(database["database"])
                )
            )
            _cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database["database"])
                )
            )
        _conn.close()

        # Step 2: Connect to the newly created database and populate it.
        _conn = _connect_to_db(database)
        _conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with _conn.cursor() as _cursor:
            _cursor.execute(sql_file.read())
        _conn.close()

    except psycopg2.Error as _error:
        if _conn:
            _conn.close()
        _error_msg = (
            f"Error occurred while creating or populating the database: {_error}"
        )
        pub.sendMessage(
            "do_log_error_msg",
            logger_name="ERROR",
            message=_error_msg,
        )
        raise DataAccessError(_error_msg)


def do_create_sqlite3_db(database: Dict[str, str], sql_file: TextIO) -> None:
    """Create a SQLite3 database.

    :param dict database: the database connection information.
    :param TextIO sql_file: the file containing the SQL statements used to
        create the database.
    :return: None
    """
    conn = sqlite3.connect(database["database"])
    conn.executescript(sql_file.read().strip())

    conn.close()


def do_open_session(database: str) -> Tuple[Engine, scoped_session]:
    """Create a session to be used with an instance of the BaseDatabase."""
    engine: Engine = create_engine(database)

    # Test the connection by attempting to connect
    connection = engine.connect()
    connection.close()

    # Return the engine and a scoped session for handling database interactions
    return (
        engine,
        scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        ),
    )


# noinspection PyUnresolvedReferences
class BaseDatabase:
    """The Base Database model."""

    # Define private class dictionary attributes.

    # Define private class list attributes.
    _known_dialects = ["sqlite", "postgres"]
    _system_databases = ["postgres", "template0", "template1"]

    # Define private class scalar attributes.

    # Define public class dict attributes.

    # Define public class list attributes.

    # Define public class scalar attributes.
    sqlstatements: Dict[str, str] = {
        "select": "SELECT {0:s} ",
        "from": "FROM {0:s} ",
        "order": "ORDER BY {0:s} DESC LIMIT 1",
    }

    def __init__(self) -> None:
        """Initialize an instance of the Base database model."""
        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.cxnargs: Dict[str, str] = {
            "dialect": "",
            "user": "",
            "password": "",
            "host": "",
            "port": "",
            "database": "",
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.engine: Optional[Engine] = None  # type: ignore
        self.session: scoped_session = None  # type: ignore
        self.database: str = ""

    def do_add_user(
        self,
        user_class: object,
        user_info: Dict[str, str],
        user_id: int = 0,
        user_group_id: int = 1,
    ) -> None:
        """Add a generic user to the database.

        :param user_class: the class representing the user record.
        :param user_info: a dictionary containing user details.
        :param user_id: the user ID (default is 0 for admin).
        :param user_group_id: the user group ID (default is 1 for admin).
        """
        _user = user_class()
        _user.user_id = user_id
        _user.user_group_id = user_group_id
        _user.user_lname = user_info["lname"]
        _user.user_fname = user_info["fname"]
        _user.user_email = user_info["email"]
        _user.user_phone = user_info["phone"]

        self.session.add(_user)
        self.session.commit()

    def do_build_databases_query(self) -> str:
        """Build the SQL query to retrieve available databases."""
        return self.sqlstatements["select"].format("datname") + self.sqlstatements[
            "from"
        ].format("pg_database;")

    def do_build_database_url(self, database: Dict[str, str]) -> str:
        """Build the URL for the database.

        :return: URL string for connecting to the selected database.
        :rtype: str
        """
        _required_keys = [
            "host",
            "port",
            "database",
            "user",
            "password",
        ]
        if any(_key not in database for _key in _required_keys):
            self.do_handle_db_error(
                "Missing required database configuration keys",
                "",
            )
        if database["dialect"] not in self._known_dialects:
            self.do_handle_db_error(
                f"Unknown dialect in database connection: {database['dialect']}",
                "",
            )
        if not isinstance(database["database"], str) or not database["database"]:
            self.do_handle_db_error(
                f"Non-string or blank string value in database connection:"
                f" {database['database']}.",
                "",
            )
        if database["dialect"] == "sqlite":
            return f"sqlite:///{database['database']}"
        if database["dialect"] == "postgres":
            return (
                f"postgresql://{database['user']}:{database['password']}@"
                f"{database['host']}:{database['port']}/{database['database']}"
            )

    def do_build_postgres_databases_query(self) -> str:
        """Build the SQL query to retrieve available databases."""
        return "{0}{1}".format(
            self.sqlstatements["select"].format("datname"),
            self.sqlstatements["from"].format("pg_database;"),
        )

    def do_connect(self, database: Dict) -> None:
        """Connect to the database.

        :param database: the connection information for the database to connect to.
        :return: None
        :rtype: None
        :raise: sqlalchemy.exc.OperationalError if passed an invalid database
            URL.
        :raise: ramstk.exceptions.DataAccessError if passes an unsupported database
            SQL dialect.
        """
        try:
            # Set connection arguments from the provided database dictionary
            self.cxnargs.update(
                {
                    "dialect": database.get("dialect"),
                    "user": database.get("user"),
                    "password": database.get("password"),
                    "host": database.get("host"),
                    "port": database.get("port"),
                    "database": database.get("database"),
                }
            )

            # Attempt to open the session using the constructed database connection
            self.engine, self.session = self.get_database_session(self.cxnargs)

        except OperationalError as _error:
            _context_msg = f"{str(_error.orig).capitalize()}: {self.cxnargs}"
            self.do_handle_db_error(_error, _context_msg)

    def do_create_database(
        self,
        database: Dict[str, str],
        sql_file: str,
    ) -> None:
        """Create a database from the passed parameters.

        :param dict database: the dictionary containing the parameters for
            connecting to the database server.
        :param str sql_file: the file containing the SQL statements used
        to create the database.
        :return: None
        :rtype: None
        """
        try:
            with open(sql_file, "r", encoding="utf-8") as _sql_file:
                _dialect = database.get("dialect")
                _dialect_actions = {
                    "postgres": do_create_postgres_db,
                    "sqlite": do_create_sqlite3_db,
                }
                _dialect_action = _dialect_actions.get(_dialect)
                if _dialect_action:
                    _dialect_action(database, _sql_file)
                else:
                    raise DataAccessError(f"Unknown dialect: {_dialect}")

                self.do_connect(database)

            pub.sendMessage("succeed_create_database", database=database)
        except FileNotFoundError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=f"SQL file {sql_file} could not be found.",
            )

    def do_delete(self, item: object) -> None:
        """Delete a record from the RAMSTK Program database.

        :param item: the item to remove from the RAMSTK Program database.
        :type item: Object()
        :return: None
        :rtype: None
        """
        try:
            self.session.delete(item)
            self.session.commit()
        except SQLAlchemyError as _error:
            _context_message = (
                "Database error when attempting to delete a record. Error details: "
            )
            self.do_handle_db_error(_error, _context_message)

    def do_disconnect(self) -> None:
        """Close the current session.

        :return: None
        :rtype: None
        """
        self.session.close()
        self.engine.dispose()
        # noinspection PyTypeChecker
        self.session = None  # type: ignore
        self.database = ""

    def do_execute_query(
        self, query: str, session: scoped_session = None
    ) -> Sequence[Row[tuple[Any, ...] | Any]] | Any:
        """Execute the given SQL query and return the results."""
        if not session:
            return self.session.scalars(query)
        return session.execute(text(query)).fetchall()

    def do_filter_system_databases(self, databases: List[Tuple[Any, ...]]) -> List[str]:
        """Filter out system databases and return only those relevant to RAMSTK."""
        return [_db[0] for _db in databases if _db[0] not in self._system_databases]

    def do_handle_db_error(self, error, context_message) -> None:
        """Handle errors raised by other methods.

        :param error:
        :type error:
        :param context_message:
        :type context_message: str
        :return: None
        :rtype: None
        :raises: DataAccessError
        """
        with contextlib.suppress(AttributeError):
            self.session.rollback()

        _error_msg = f"{context_message}: {error}" if context_message else error
        pub.sendMessage(
            "do_log_error_msg",
            logger_name="ERROR",
            message=_error_msg,
        )
        raise DataAccessError(_error_msg)

    def do_insert(self, record: object) -> None:
        """Add a new record to a database table.

        :param record: the object to add to the RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            self.session.add(record)
            self.session.commit()
        except (
            FlushError,
            exc.DataError,
            exc.IntegrityError,
            exc.InternalError,
            exc.StatementError,
        ) as _error:
            _context_message = "Database error while adding a record. Error details: "
            self.do_handle_db_error(
                _error.orig.pgerror.split(":")[2].strip(),
                _context_message,
            )
        except AttributeError as _error:
            _context_message = "Database error while adding a record. Error details: "
            self.do_handle_db_error(
                _error,
                _context_message,
            )

    def do_insert_many(self, records: List[object]) -> None:
        """Add a group of new records to a database table.

        :param list records: the list of objects to add to the RAMSTK database.
        :return: None
        :rtype: None
        """
        for _record in records:
            self.do_insert(_record)

    def do_select_all(self, table, **kwargs) -> query.Query:
        """Select all records from the RAMSTK database for table.

        :param table: the database table object to select all from.
        :return: a list of table instances; one for each record.
        """
        _keys = kwargs.get("key", [])
        _values = kwargs.get("value", [])
        _order: Optional[str] = kwargs.get("order", None)
        _all: bool = kwargs.get("_all", True)

        # Ensure keys and values are provided in pairs.
        if _keys and len(_keys) != len(_values):
            raise ValueError("The number of keys and values must match.")

        # Build the filter criteria dynamically if filters are provided.
        _filters = (
            {key: _values[idx] for idx, key in enumerate(_keys)} if _values else {}
        )

        # Start the query with filtering if applicable.
        _query = self.session.query(table).filter_by(**_filters)

        # Apply ordering if provided.
        if _order:
            if isinstance(_order, list):
                _query = _query.order_by(*_order)
            else:
                _query = _query.order_by(_order)

        # Return all results or just the first, based on the _all flag.
        return _query.all() if _all else _query.first()

    def do_update(self, record: object = None) -> None:
        """Update the RAMSTK database with any pending changes.

        :keyword record: the record to update in the database.
        :return: None
        :rtype: None
        """
        if record is not None:
            self.session.add(record)

        try:
            self.session.commit()
        except (
            exc.DataError,
            exc.IntegrityError,
            exc.InvalidRequestError,
            exc.ProgrammingError,
        ) as _error:
            _context_message = (
                f"Database error during record update. SQL statement:\n\t"
                f"{getattr(_error, 'statement', 'No statement available')}.\n"
                f"Parameters:"
                f"\n\t{getattr(_error, 'params', 'No parameters available')}."
            )
            self.do_handle_db_error(
                _error,
                _context_message,
            )

    def get_database_list(self, database: Dict[str, str]) -> List:
        """Retrieve the list of program databases available to RAMSTK.

        This method is used to create a user-selectable list of databases when
        using the postgresql or MariaDB (MySQL) backend.  SQLite3 simply uses
        an open file dialog.

        :param database: the connection information for the dialect's
            administrative database.
        :return: the list of databases available to RAMSTK for the selected
            dialect.
        :rtype: list
        """
        _databases: List[str] = []

        if database["dialect"] == "postgres":
            _query = self.do_build_databases_query()
            __, _session = self.get_database_session(database)

            # Fetch the list of databases and filter them.
            _databases = self.do_execute_query(_query, _session)
            return self.do_filter_system_databases(_databases)

        raise DataAccessError(f"Unsupported dialect: {database['dialect']}")

    def get_database_session(
        self, database: Dict[str, str]
    ) -> Tuple[Engine, scoped_session]:
        """Create and return a session for interacting with the database.

        :param database: dictionary with database connection parameters.
        :type database: dict
        :return: engine, scoped session
        :rtype: tuple
        """
        _connection_url = self.do_build_database_url(database)
        return do_open_session(_connection_url)

    def get_last_id(self, table: str, id_column: str) -> Any:
        """Retrieve the last used value of the ID column.

        .. hint:: This method could be used to select the last used value from
            any column in a table.

        :param table: the name of the table to get the last ID from.
        :param id_column: the name of the field to use as the ID column.
        :return: _last_id; the last used value of the ID column.
        :rtype: int
        :raise: :class:`sqlalchemy.exc.OperationalError` if passed an unknown
            table or unknown column name.
        """
        # Ensure the ID column name starts with "fld_".
        if not id_column.startswith("fld_"):
            id_column = f"fld_{id_column}"

        # Construct the SQL statement to retrieve the last ID.
        _sql_statement = (
            self.sqlstatements["select"].format(id_column)
            + self.sqlstatements["from"].format(table)
            + self.sqlstatements["order"].format(id_column)
        )

        try:
            # Execute the SQL query and get the first result.
            _last_id = self.session.execute(text(_sql_statement)).first()
            return _last_id[0] if _last_id else 0
        except (
            exc.ProgrammingError,
            TypeError,
        ) as _error:
            _context_message = f"Error retrieving last ID from {table}: "
            self.do_handle_db_error(
                _error,
                _context_message,
            )

    @staticmethod
    def _get_user_input(fields: Dict[str, str]) -> Dict[str, str]:
        """Get user input for any user record.

        :param fields: a dict of field names and prompts.
        :return: a dict of user input for the fields.
        """
        return {key: input(prompt) for key, prompt in fields.items()}
