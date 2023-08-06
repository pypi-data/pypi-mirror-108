import abc
import numpy as np


class SimilarityScorer:
    """
    Abstract class for compute the similarity of the entities.
    """

    def add_matcher(self, matcher):
        """
                Add the match object on the SimilarityScorer.

                Args:
                    matcher: matchingframework.match.matchers.Matcher

                Returns: None

                """
        self.matcher = matcher
        """The matcher object"""

    @abc.abstractmethod
    def similarity_score(self, vector_matrix):
        """
        Compute similarity.

        Returns:
        -------
        similarity_matrix : dict
            An arary with shape of input array
        """

    def score(self):
        """
        Get each vectorized matrix by for loop and calling similarity_score().
        Normalize matrixes by calling normalize_matrixes().
        """
        similarity_dict = {}
        for feature, vector_matrix in self.matcher.vectorized_dict.items():
            similarity_dict[feature] = self.similarity_score(vector_matrix)
        self.matcher.similarity_matrix = self.normalize_matrixes(similarity_dict)

    def normalize_matrixes(self, similarity_dict):
        """
        Normalize similarity matrixes into one with it's weight.

        Args:
            similarity_dict: dict

        Returns:
        -------
        similarity_matrix: array
            Similarity matrix of records.
        """
        shape = self.matcher.get_count_records()
        similarity_matrix = np.zeros((shape, shape))
        for feature, distance in similarity_dict.items():
            similarity_matrix += similarity_dict[feature] * feature.weight
        return similarity_matrix
