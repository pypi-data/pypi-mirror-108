"""Generate a dictionary tree based on words."""

import pickle

from py_progress import progressbar
from ._node import _Node as Node


class DictionaryGenerator:
    """Generate a dictionary tree based on words.

    The DictionaryGenerator class generates a dictionary tree that can be used by the Autocomplete class to
    autocomplete incomplete words.

    Code Example:
        .. code-block:: python

            from pcy.rule_based.dictionary import DictionaryGenerator

            # words list
            words = [{"words": "Apple", "data": {"color": "red"}}, {"words": "Anaconda", "data": {"color": "black"}}]

            # initializing the DictionaryGenerator class
            gen = DictionaryGenerator(words)

            # generating the tree
            tree = gen.generate_dictionary()

    :raises ValueError: When the words are not a valid list
    :raises ValueError: When there are no words in the words list
    :raises ValueError: When the word is not a valid string
    :raises ValueError: When the word is not a valid
    :raises ValueError: When there is no dictionary tree
    :raises ValueError: When the path to save the tree is not valid
    :raises ValueError: When the path to save the tree is not valid
    :return: Returns the tree
    :rtype: Node
    """

    @staticmethod
    def __generate_tree(word, data=None, index=0, node=None):
        """Generate a tree based on the word."""
        current_chr = word[index]

        current_word = None
        if len(word) == index + 1:
            current_word = word

        is_child_node_exists = node.get_child_node(current_chr)

        if is_child_node_exists:
            child_node = is_child_node_exists

            child_node.add_word(current_word, data)
        else:
            child_node = Node(current_chr, word=current_word, parent=node, data=data)
            node.add_child(child_node)

        if len(word) > index + 1:
            DictionaryGenerator.__generate_tree(word, data, index=index + 1, node=child_node)

    @classmethod
    def load_dictionary(cls, path):
        """Load a dictionary from the local file.

        :param path: Path where the dictionary stored in the filesystem
        :type path: str
        :raises ValueError: When the path to the saved dictionary is not valid
        :return: Returns a new dictionary tree
        :rtype: Node
        """
        if not isinstance(path, str) and not path:
            raise ValueError("Please provide a valid path to load the data")

        with open(path, "rb") as f:
            return pickle.load(f)

    def __init__(self, words):
        """Constructor method for the class DictionaryGenerator"""
        if not isinstance(words, list):
            raise ValueError("Please provide a valid dictionary list with words and data")

        if len(words) < 1:
            raise ValueError("There is no words in the list")

        self.__words = words
        self.__tree = None

    def generate_dictionary(self):
        """Generate a new dictionary based on the words list.

        :return: New dictionary tree
        :rtype: Node
        """
        tree = Node("ROOT")

        for index, word in enumerate(self.__words):
            progressbar(
                index,
                len(self.__words),
                f"{index+1}/{len(self.__words)}",
                f"Current Char: {word['words'][0]}",
            )
            DictionaryGenerator.__generate_tree(word["words"].lower(), data=word["data"], node=tree)

        print("")

        self.__tree = tree

        return self.__tree

    def add_word_to_dictionary(self, word, data=None):
        """Add word to generated dictionary.

        :param word: Word that needed to be added
        :type word: str
        :param data: Data that needed to be added with the word
        :type word: any
        :raises ValueError: When the word is not valid string
        :raises ValueError: When the word is not a valid word
        :raises ValueError: When there is no dictionary generated.
        :return: New dictionary tree
        :rtype: Node
        """
        if not isinstance(word, str):
            raise ValueError("Please provide a valid word")

        if not word:
            raise ValueError("Please provide a word to add")

        if not self.__tree:
            raise ValueError("Please create a dictionary first")

        self.__generate_tree(word, data=data, node=self.__tree)

        return self.__tree

    def save_dictionary(self, path):
        """Save dictionary to the local filesystem.

        :param path: Path to store the dictionary
        :type path: str
        :raises ValueError: When the path is not valid
        """
        if not isinstance(path, str) and not path:
            raise ValueError("Please provide a valid path to save the data")

        with open(path, "wb") as f:
            pickle.dump(self.__tree, f)
