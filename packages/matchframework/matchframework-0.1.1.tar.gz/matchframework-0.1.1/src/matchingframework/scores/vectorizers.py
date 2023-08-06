import abc


class Vectorizer:
    """
       Abstract class for convert a collection of record's data to a matrix of features.
    """

    def add_matcher(self, matcher):
        """
                Add the match object on the Vectorizer.

                Args:
                    matcher: matchingframework.match.matchers.Matcher

                Returns: None

                """
        self.matcher = matcher
        """The matcher object"""

    @abc.abstractmethod
    def vectorize_matrix(self, feature, records):
        """
        Convert list of data to a matrix of features.

        Returns:
        -------
        vectorized_matrix: array
            A matrix after vectorize.
        """

    def vectorize(self):
        """
        Get each data by for loop and call method vectorized_matrix()

        Returns:
        -------
        vectorized_dict: dict
            A dictionary with feature as key and vectorized_matrix as value.
        """
        vectorized_dict = {}
        for feature, records in self.matcher.records_join.items():
            vectorized_dict[feature] = self.vectorize_matrix(feature, records)
        self.matcher.vectorized_dict = vectorized_dict


class FrequencyVectorizer(Vectorizer):

    def __init__(self,
                 max_df=1,
                 min_df=1,
                 stop_words=[],
                 ngram_range=(1, 1)):
        """

        Args:
            max_df: float or int
            min_df: Float or int
            stop_words: list
            ngram_range: array
        """
        self.max_df = max_df
        """ignore terms in vocabulary that have frequency or proportion higher than max_df"""
        self.min_df = min_df
        """ignore terms in vocabulary that have frequency or proportion lower than min_df"""
        self.stop_words = stop_words
        """terms that were ignored"""
        self.ngram_range = ngram_range
        """the lower and upper boundary of n-grams"""
