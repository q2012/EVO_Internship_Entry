class Trie:
    def __init__(self, char: str):
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

def traverse_trie(root: Trie, num: int, prefix: str):
    if num == 0:
        return
    prefix += root.char
    if root.isLeaf:
        num -= 1
        yield prefix
    for node in root.children:
        yield from traverse_trie(node, num, prefix)

def find_first_n_after_prefix(root: Trie, n: int, prefix: str):
    node = find_prefix_node(root, prefix)
    if node is not None:
        yield from traverse_trie(node, n, prefix)


if __name__ == "__main__":

    root = Trie('')
    add(root, "kek")
    add(root, "kek212")
    add(root, "kekasd")
    add(root, "kek3")

    for s in find_first_n_after_prefix(root, 10, "keka"):
        print(s)
