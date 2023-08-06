import abc


class DataPreprocessor:
    """
    Abstract class to process and standardize data of the dataset.
    """

    def add_matcher(self, matcher):
        """
        Add the match object on the Dataprocess.

        Args:
            matcher: matchingframework.match.matchers.Matcher

        Returns: None

        """
        self.matcher = matcher
        """The matcher object"""

    @abc.abstractmethod
    def data_preprocess(self):
        """
        Do data preprocessing.
        """
        self.drop_record_with_none_value_in_feature()
        self.id_preprocess()
        self.initiate_match_record()

    def id_preprocess(self):
        """
        Method to process the IDs of two dataset.

        Returns: None

        """
        self.add_id(self.matcher.left_data.df, "left")
        self.add_id(self.matcher.right_data.df, "right")

    def add_id(self, df, side):
        """
        Static method of DataPreprocessor to add new IDs into the dataset if it is not has IDs

        Args:
            dataset: DataFrame
            side: String

        Returns: None

        """
        id_side = "id_" + side
        id_list = ["{}_{}".format(i, side) for i in range(0, len(df))]
        df[id_side] = id_list

    def initiate_match_record(self):
        """
        Initialize the list of records according to the feature is used for matching
        """
        list_records_left = self.matcher.get_records_by_fields(self.matcher.left_data, self.matcher.features_left, 'id_left')
        list_records_right = self.matcher.get_records_by_fields(self.matcher.right_data, self.matcher.features_right, 'id_right')
        self.matcher.records_join = {}
        for i in range(0, len(self.matcher.join_features)):
            join_record = {}
            join_record.update(list_records_left[i])
            join_record.update(list_records_right[i])
            self.matcher.records_join[self.matcher.join_features[i]] = join_record

    def drop_record_with_none_value_in_feature(self):
        """
        remove records with None feature
        """
        self.matcher.left_data.df = self.matcher.left_data.df.dropna(subset=self.matcher.features_left)
        self.matcher.right_data.df = self.matcher.right_data.df.dropna(subset=self.matcher.features_right)
