class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False
        self.words = []


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.words.append(word)
        node.isEnd = True

    def search_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.isEnd

    def prefix_search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def suffix_search(self, word):
        rev_word = word[::-1]
        node = self.root
        for char in rev_word:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def top_suggested_words(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        sorted_words = sorted(node.words)
        return sorted_words[:5]
