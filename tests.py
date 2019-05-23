import pytest
from trie import *


phone_list = ["380935746965", "380935746966", "380935746967", "380935746968", "380935746969", "380935746970",
              "490635746965", "490645746965", "490655746965", "490665746965", "490635946965", "490636046965"]


@pytest.fixture()
def root_setup():
    root = Trie()
    yield root


@pytest.fixture()
def phones_setup(root_setup):
    root = root_setup
    for str in phone_list:
        add(root, str)
    yield root


def test_add_empty(root_setup):
    print("test add(\"\") -- adding empty entry makes root an entry")
    root = root_setup
    assert ((add(root, "") == root) and
            root.isLeaf and
            (root.char == '') and
            (len(root.children) == 0))


def test_add_one(root_setup):
    print("test add(\"\")")
    root = root_setup
    node = add(root, "te")
    assert ((not root.isLeaf) and
            (root.char == '') and
            (len(root.children) == 1) and
            (not root.children[0].isLeaf) and
            (root.children[0].char == 't') and
            (len(root.children[0].children) == 1) and
            (root.children[0].children[0].isLeaf) and
            (root.children[0].children[0].char == 'e') and
            (len(root.children[0].children[0].children) == 0) and
            (root.children[0].children[0] == node))


@pytest.mark.parametrize("n", [0, 1, 2, 10])
@pytest.mark.parametrize("prefix", ["", "380935746965", "3", "38059"])
def test_first_n_all(phones_setup, n, prefix):
    print("n: %d, prefix: %s" % (n, prefix))
    root = phones_setup
    filtered_list = list(filter(lambda x: x.startswith(prefix), phone_list))
    num = 0
    for val in find_first_n_after_prefix(root, n, prefix):
        print(val)
        num += 1
        assert val in filtered_list
    assert (num == n or num == len(filtered_list))
