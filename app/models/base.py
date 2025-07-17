"""
Base Database Operations

Contains the core DatabaseManager class for database operations.
"""

import pandas as pd
import logging
from sqlalchemy import create_engine, text
import os
from typing import Tuple, Optional, Union, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseManager:
    """
    Database manager for handling database connections and operations.
    
    This class provides a centralized interface for database operations
    using SQLAlchemy and pandas for data manipulation.
    """
    
    def __init__(self, db_url=None, logger=None, use_test_db=False):
        """
        Initialize the DatabaseManager.
        
        Args:
            db_url: Database URL. If None, uses environment variables.
            logger: Logger instance. If None, creates a new logger.
            use_test_db: Whether to use test database configuration.
        """
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
        """
        Execute a SQL query and return results as a pandas DataFrame.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            
        Returns:
            pandas.DataFrame: Query results
        """
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
        Execute a SQL query and return the first row.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            
        Returns:
            Optional[Tuple]: First row of results or None
        """
        try:
            with self.engine.connect() as connection:
                effective_params = params if params is not None else {}
                result = connection.execute(text(query), effective_params)
                return result.fetchone()
        except Exception as e:
            self.logger.error(f"Database query failed: {e}")
            return None

    def fetch_all(self, query: str, params: Optional[Union[Tuple, Dict]] = None) -> list:
        """
        Execute a SQL query and return all rows.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            
        Returns:
            list: All rows of results
        """
        try:
            with self.engine.connect() as connection:
                effective_params = params if params is not None else {}
                result = connection.execute(text(query), effective_params)
                return result.fetchall()
        except Exception as e:
            self.logger.error(f"Database query failed: {e}")
            return []

    def execute(self, query: str, params: Optional[Union[Tuple, Dict]] = None) -> bool:
        """
        Execute a SQL query that doesn't return results (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.engine.connect() as connection:
                effective_params = params if params is not None else {}
                connection.execute(text(query), effective_params)
                connection.commit()
                return True
        except Exception as e:
            self.logger.error(f"Database execution failed: {e}")
            return False

    def get_connection(self):
        """
        Get a database connection for transaction management.
        
        Returns:
            SQLAlchemy connection object
        """
        return self.engine.connect()

    def close(self):
        """Close the database engine."""
        if hasattr(self, 'engine') and self.engine:
            self.engine.dispose() 