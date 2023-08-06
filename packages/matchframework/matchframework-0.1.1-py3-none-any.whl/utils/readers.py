import abc
from src.dmf.structures import (
    Dataset,
)


class Reader():
    """
    Abstract class for reading data in dataset format.
    """

    @abc.abstractmethod
    def __init__(self):
        """

        Args:
            dataset: Dataset
        """
        self.dataset = Dataset()

    @abc.abstractmethod
    def read_func(self):
        """
        Function to read dataset.
        """
        return

    def read(self):
        """
        Method to read dataset

        Returns: Dataset
        """
        self.dataset.df = self.read_func()
        return self.dataset


class FileReader(Reader):
    """
    Class reader for read data from file.
    """

    def __init__(self, file_name):
        """

        Args:
            file_name: String
        """
        super().__init__()
        self.file_name = file_name
        """Name of file that contains a dataset"""


class DBReader(Reader):
    """
    Class reader for read data from database.
    """

    def __init__(self, db_host, db_user, db_passwd, db_name, sql):
        """

        Args:
            db_host: String
            db_user: String
            db_passwd: String
            db_name: String
        """
        super().__init__()
        self.db_host = db_host
        """Database host name to connect"""
        self.db_user = db_user
        """Database user name to connect"""
        self.db_passwd = db_passwd
        """Database password to connect"""
        self.db_name = db_name
        """Database name to connect"""
        self.sql = sql
        """Query to select data from MySQL database"""
        # self.connect()

    @abc.abstractmethod
    def connect(self):
        """
        Method for create a connection to the database.
        """
        return
