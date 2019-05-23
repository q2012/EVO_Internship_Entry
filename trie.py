class Trie:
    def __init__(self, char=''):
        self.isLeaf = False
        self.children = []
        self.char = char


def add(root: Trie, word: str):
    node = root
    for char in word:
        found = False
        for child in node.children:
            if child.char == char:
                found = True
                node = child
                break

        if not found:
            new_node = Trie(char)
            node.children.append(new_node)
            node = new_node
    node.isLeaf = True
    return node


def find_prefix_node(root: Trie, prefix: str):
    node = root
    if not root.children:
        return None
    for char in prefix:
        found = False
        for child in node.children:
            if child.char == char:
                found = True
                node = child
                break
        if not found:
            return None
    return node


def traverse_trie(root: Trie, prefix: str):
    if traverse_trie.num <= 0:
        return
    prefix += root.char
    if root.isLeaf:
        traverse_trie.num -= 1
        yield prefix
    for node in root.children:
        yield from traverse_trie(node, prefix)


def find_first_n_after_prefix(root: Trie, n: int, prefix: str):
    node = find_prefix_node(root, prefix)
    if node is not None:
        traverse_trie.num = n
        prefix = prefix[:-1]
        yield from traverse_trie(node, prefix)
