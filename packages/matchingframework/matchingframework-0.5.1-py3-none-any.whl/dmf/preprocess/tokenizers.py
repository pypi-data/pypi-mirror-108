import abc


class Tokenizer():
    """
    Abstract class for splitting and tokenizing raw text.
    """

    def add_matcher(self, matcher):
        """
        Add the match object on the Tokenizer.

        Args:
            matcher: matchingframework.match.matchers.Matcher

        Returns: None

        """
        self.matcher = matcher
        """The matcher object"""

    @abc.abstractmethod
    def tokenize_record(self, record):
        """
        An abstract method to tokenize record's data.

        Returns: List

        """
        return

    def tokenize(self):
        """
        Get each data by for loop and call method tokenize_record().
        Returns a dictionary with feature as key and list tokens as value.

        Returns: Dict

        """
        dict_of_list_token = {}
        for feature, records in self.matcher.records_join.items():
            list_token = []
            for record in records.values():
                list_token.append(self.tokenize_string(record))
            dict_of_list_token[feature] = list_token
        return dict_of_list_token

    @abc.abstractmethod
    def normalize_record(self, record):
        """
        An abstract method to normalize record's data.
        """
        return record

    def normalize(self, records):
        """
        Get each data by for loop and call method normalize_record()

        Returns: List

        """
        nomalized_records = []
        for record in records:
            nomalized_records.append(self.normalize_record(record))
        return nomalized_records


class GenericTokenizer(Tokenizer):
    """
    A generic tokenizer use by calling function.
    """

    def __init__(self, splitter):
        self.splitter = splitter
        """Splitter function"""

    def tokenize_record(self, record):
        """
        A function that takes a string as input and returns a list/iterator of tokenized string items

        Args:
            record: String

        Returns: List

        """
        return self.splitter(record)
