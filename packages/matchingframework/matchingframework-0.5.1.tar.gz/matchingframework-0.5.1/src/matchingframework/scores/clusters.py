import abc


class Clustering:

    def add_matcher(self, matcher):
        """
        Add the match object on the Clustering.

        Args:
            matcher: matchingframework.match.matchers.Matcher

        Returns: None

        """
        self.matcher = matcher
        """The matcher object"""

    @abc.abstractmethod
    def analyze(self):
        """
        Analyze data using Cluster Analysis.
        """

    def add_cluster(self):
        """
        Adding cluster results to two matcher's dataset
        """
        cluster_left, cluster_right = self.split_list_records()
        self.matcher.left_data.df['match_cluster_id'] = cluster_left
        self.matcher.right_data.df['match_cluster_id'] = cluster_right

    def split_list_records(self):
        """
        Get the split point.
        """
        part = len(self.matcher.left_data.df['id_left'])
        return self.matcher.clusters[:part], self.matcher.clusters[part:]
