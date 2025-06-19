import pandas as pd
import logging
from sqlalchemy import create_engine, text
import os
from typing import Tuple, Optional, Union, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self, db_url=None, logger=None, use_test_db=False):
        
        if db_url:
            # If a specific URL is provided, use it
            self.db_url = db_url
        elif use_test_db:
            # Use test database
            self.db_url = os.getenv("TEST_DB_URL")
            if not self.db_url:
                raise ValueError("Test database URL not specified. Set TEST_DB_URL in your .env file.")
        else:
            # Use regular database
            self.db_url = os.getenv("DB_URL")
            if not self.db_url:
                raise ValueError("Database URL not specified. Set DB_URL in your .env file or pass it to DatabaseManager.")
        
        self.engine = create_engine(self.db_url)
        self.logger = logger or logging.getLogger(__name__)
        self.is_test_db = use_test_db

    def fetch_dataframe(self, query: str, params: Optional[Union[Tuple, Dict]] = None) -> pd.DataFrame:
        try:
            # Use SQLAlchemy's text() to properly handle the query
            with self.engine.connect() as connection:
                effective_params = params if params is not None else {}
                df = pd.read_sql_query(text(query), connection, params=effective_params)
                return df
        except Exception as e:
            self.logger.error(f"Database query failed: {e}")
            return pd.DataFrame()

    def fetch_one(self, query: str, params: Optional[Union[Tuple, Dict]] = None) -> Optional[Tuple]:
        """
        Fetches a single row from the database.

        Args:
            query: The SQL query to execute.
            params: A tuple for positional parameters or a dictionary for named parameters, or None.

        Returns:
            A tuple representing the row, or None if no row is found.
        """
        try:
            with self.engine.connect() as connection:
                # Handle parameters - use empty tuple if None
                effective_params = params if params is not None else ()
                result = connection.execute(text(query), effective_params).fetchone()
                return result
        except Exception as e:
            self.logger.error(f"Database fetch_one failed: {e}")
            return None 