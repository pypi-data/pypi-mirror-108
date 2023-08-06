import abc
from src.dmf.structures import (
    Dataset,
)


class Writer():
    """
    Abstract class for writing data.
    """

    @abc.abstractmethod
    def __init__(self, dataset=Dataset()):
        """

        Args:
            dataset: Dataset
        """
        self.dataset = dataset

    @abc.abstractmethod
    def write(self):
        """
        Method to write data
        """


class FileWriter(Writer):
    """
    Class writer for write dataset to file.
    """

    def __init__(self, file_name, dataset):
        """

        Args:
            file_name: String
        """
        super(FileWriter, self).__init__(dataset=dataset)
        self.file_name = file_name
        """Name of file to writing the dataset"""


class DBWriter(Writer):
    """
        Class writer for write dataset to database.
    """

    def __init__(self, db_host, db_user, db_passwd, db_name, dataset):
        """

        Args:
            db_host: String
            db_user: String
            db_passwd: String
            db_name: String
        """
        super(DBWriter, self).__init__(dataset=dataset)
        self.db_host = db_host
        """Database host name to connect"""
        self.db_user = db_user
        """Database user name to connect"""
        self.db_passwd = db_passwd
        """Database password to connect"""
        self.db_name = db_name
        """Database name to connect"""

    @abc.abstractmethod
    def connect(self):
        """
        Method for create an engine to connect to the database.
        """
        return

    @abc.abstractmethod
    def write(self, table_name):
        return
