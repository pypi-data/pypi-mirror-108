"""Make an Autocomplete class to autocomplete incomplete words using a dictionary tree."""

from functools import lru_cache
from ._node import _Node as Node


class Autocomplete:
    """Make an Autocomplete class to autocomplete incomplete words using a dictionary tree.

    The Autocomplete class receives a Dictionary tree in its __init__ method. To get the Dictionary tree,
    we need to use the DictionaryGenerator class.

    To generate word suggestions, you need to call the .autocomplete method. Look at the example below to
    understand everything.

    Code Example:
        .. code-block:: python

            from pcy.rule_based.dictionary import Autocomplete

            # here the tree is the dictionary
            auto = Autocomplete(tree)

            # calling the method to get complete words based on the incomplete word
            # here the word "hous" is the incomplete word and 10 is the number of suggestions to return
            words = auto.autocomplete("hous", 10)

            # printing the words
            print(words)

            # --> ['housage', 'housal', 'housatonic', 'house', 'houseball', 'houseboat', 'houseboating', 'houseboats',
            # 'houseboy', 'houseboys', 'housebote']

    :param dictionary: Instance of the node class. It can be created using the DictionaryGenerator class.
    :type dictionary: node
    :raises ValueError: When the provided dictionary is not valid
    """

    def __init__(self, dictionary):
        """Constructor method."""
        if not isinstance(dictionary, Node):
            raise ValueError("Please provide a valid dictionary")

        self.__dictionary = dictionary

    @lru_cache(maxsize=4096)
    def autocomplete(self, incomplete_word, no_of_suggestions):
        """Return an array of suggestions.

        It returns the suggestions based on incomplete_word and no_of_suggestions.

        :param incomplete_word: Incomplete word to autocomplete
        :type incomplete_word: str
        :param no_of_suggestions: Number of suggestions (words) to provide
        :type no_of_suggestions: int
        :raises ValueError: When the incomplete_word is not valid string
        :raises ValueError: When incomplete_word is empty
        :raises ValueError: When the no_of_suggestions is less than zero
        :return: An array of strings containing suggestions
        :rtype: str[]
        """
        if not isinstance(incomplete_word, str):
            raise ValueError("Please provide a valid incomplete_word")

        if not incomplete_word:
            raise ValueError("Invalid incomplete_word, please provide at least once character")

        if no_of_suggestions < 1:
            raise ValueError("Please provide a valid no_of_suggestions")

        return self.__dictionary.autocomplete_incomplete_word(incomplete_word, no_of_suggestions)
