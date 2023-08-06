"""Node in the dictionary tree.

A node contains the key, the word, it;s parent, and its children.

Raises:
    ValueError: If the added child is not valid

Returns:
    node: Node in the tree
"""


class _Node:
    """Node in the dictionary tree.

    A node contains the key, the word, it;s parent, and its children.

    Raises:
        ValueError: If the added child is not valid

    Returns:
        node: Node in the tree
    """

    @staticmethod
    def __find_key_in_level(node, key):
        """Find a key in the level.

        Args:
            node (node): Node to search
            key (string): Key to search

        Returns:
            node: Found node
        """
        for child in node.children:
            if child.key == key:
                return child

        return False

    @staticmethod
    def __search_tree(word, index=0, node=None):
        """Search a word from tree.

        Args:
            word (str): Word to search
            index (int, optional): Index to track the recursive loop. Defaults to 0.
            node (node, optional): Node to search. Defaults to None.

        Returns:
            node: Node in the tree
        """
        if index + 1 > len(word):
            return node

        current_key = word[index]

        child_node = _Node.__find_key_in_level(node, current_key)

        if not child_node:
            return False

        return _Node.__search_tree(word, index + 1, child_node)

    def __find_nth_words(self, node, no_of_words):
        """Find suggestions from the tree.

        Args:
            node (node): Node to search.
            no_of_words (int): Number of words to find.

        Returns:
            words: Suggested words
        """
        if self.__found_words > no_of_words:
            return []

        words = []

        if node.word:
            words.append({"word": node.word, "data": node.data})
            self.__found_words += 1

        if len(node.children) > 0:
            for child in node.children:
                words += self.__find_nth_words(child, no_of_words)

        return words

    @staticmethod
    def __print_tree(node, level=0):
        """Print the tree.

        Args:
            node (node): Node to print.
            level (int, optional): To track levels. Defaults to 0.

        Returns:
            str: String representation of the tree.
        """
        level += 1
        message = ""

        dash = "--" * level
        message += f"{dash}{node.__key}({node.__word})"

        if len(node.children) < 1:
            return message

        for child in node.children:
            message += f"\n{_Node.__print_tree(child, level)}"

        return message

    # Getters
    @property
    def key(self):
        """Getter for key.

        Returns:
            str: Key value
        """
        return self.__key

    @property
    def word(self):
        """Getter for word.

        Returns:
            str: Word of the node.
        """
        return self.__word

    @property
    def data(self):
        """Getter for data.

        Returns:
            any: Data of the node.
        """
        return self.__data

    @property
    def parent(self):
        """Getter for parent.

        Returns:
            node: Returns the parent node
        """
        return self.__parent

    @property
    def children(self):
        """Getter for children.

        Returns:
            node[]: Returns a list of children
        """
        return self.__children

    def __init__(self, key, word=None, parent=None, data=None):
        """Node in the dictionary tree.

        A node contains the key, the word, it;s parent, and its children.

        Args:
            key (str): Key for the node
            word (str, optional): Word to store the node. Defaults to None.
            parent (node, optional): Parent node for the node. Defaults to None.
        """
        self.__key = key
        self.__word = word
        self.__parent = parent
        self.__children = []
        self.__found_words = 0
        self.__data = data

    def add_child(self, node):
        """Add a child to the node.

        Args:
            node (node): Node to add

        Raises:
            ValueError: If the node is not valid.
        """
        if isinstance(node, _Node):
            self.__children.append(node)
        else:
            raise ValueError("Please provide a valid node to append")

    def is_child_exists(self, key):
        """Check if child exists.

        Args:
            key (key): Key to check

        Returns:
            bool: Returns true if node exists.
        """
        return True if _Node.__find_key_in_level(self, key) else False

    def get_child_node(self, key):
        """Get the node based on key.

        Args:
            key (str): Key to find.

        Returns:
            node: Returns the node
        """
        return _Node.__find_key_in_level(self, key)

    def add_word(self, word, data=None):
        """Add word in the node.

        Args:
            word (str): Word to add.
        """
        self.__word = word
        self.__data = data

    def autocomplete_incomplete_word(self, incomplete_word, no_of_words):
        """Complete the word based on incomplete_word.

        Args:
            incomplete_word (str): Incomplete word.
            no_of_words (int): No of words to return

        Returns:
            str[]: Suggested words based on the node.
        """
        root_node = _Node.__search_tree(incomplete_word.lower(), node=self)

        if not root_node:
            return False

        return self.__find_nth_words(root_node, no_of_words)

    def print_tree(self):
        """Print a string representation for the node."""
        print(_Node.__print_tree(self))
