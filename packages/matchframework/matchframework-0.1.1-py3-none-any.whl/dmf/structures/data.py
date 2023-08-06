from pandas import DataFrame
from src.dmf import Tokenizer


class Dataset():
    """
    Class representing a dataset.
    """

    def __init__(self):
        """

        Args:
            df: DataFrame
        """

        self.df = DataFrame()
        """Dataframe contain a dataset has been read by Reader"""

    def get_list_features(self):
        """
        Method to get list of features from Dataframe.

        Returns: List
        """
        return self.df.columns.values

    def entities(self):
        """
        Method to get list of entities from Dataframe

        Returns: List
        """

        list_of_entities = []
        for row in self.df[self.get_list_features()].iterrows():
            entity = row[1]
            list_of_entities.append(dict(entity))
        return list_of_entities

    # def initiate_list_of_records(self, records, ids):
    #     for col in self.df.columns[records]:
    #         for id in ids:


class MappingFeature:

    def __init__(self):
        """

        Args:
            join_features: Dict
            feature_left: List
            feature_right: List
        """
        self.join_features = []
        """
        A List stores the feature objects.
        This represents the mapping of features from feature_left and feature_right.
        """

        self.left_features = []
        """A list of left dataset features is used for matching."""

        self.right_features = []
        """A list of right dataset features is used for matching."""


class Feature:

    def __init__(self, field_name, weight,
                 tokenizer = Tokenizer()):
        """

        """
        self.field_name = field_name
        self.weight = weight
        self.tokenizer = tokenizer

    def __hash__(self):
        return hash((self.field_name, self.weight))
