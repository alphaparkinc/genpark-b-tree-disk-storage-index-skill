"""B+ Tree Indexing & Range Query Engine
100% Python Standard Library (bisect).
"""

import bisect

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None

class BPlusTreeIndex:
    """M-way search tree with linked leaf pagination."""
    def __init__(self, order=4):
        self.order = order
        self.root = BPlusTreeNode(is_leaf=True)

    def search(self, key):
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]
        idx = bisect.bisect_left(node.keys, key)
        if idx < len(node.keys) and node.keys[idx] == key:
            return node.children[idx]
        return None

    def insert(self, key, value):
        root = self.root
        if len(root.keys) >= self.order - 1:
            new_root = BPlusTreeNode(is_leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _split_child(self, parent, idx):
        child = parent.children[idx]
        mid = len(child.keys) // 2
        new_node = BPlusTreeNode(is_leaf=child.is_leaf)

        if child.is_leaf:
            new_node.keys = child.keys[mid:]
            new_node.children = child.children[mid:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid]
            new_node.next = child.next
            child.next = new_node
            parent.keys.insert(idx, new_node.keys[0])
            parent.children.insert(idx + 1, new_node)
        else:
            promoted_key = child.keys[mid]
            new_node.keys = child.keys[mid + 1:]
            new_node.children = child.children[mid + 1:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid + 1]
            parent.keys.insert(idx, promoted_key)
            parent.children.insert(idx + 1, new_node)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            if idx < len(node.keys) and node.keys[idx] == key:
                node.children[idx] = value
            else:
                node.keys.insert(idx, key)
                node.children.insert(idx, value)
        else:
            idx = bisect.bisect_right(node.keys, key)
            child = node.children[idx]
            if len(child.keys) >= self.order - 1:
                self._split_child(node, idx)
                if key >= node.keys[idx]:
                    idx += 1
            self._insert_non_full(node.children[idx], key, value)

    def range_query(self, min_key, max_key):
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_right(node.keys, min_key)
            node = node.children[idx]
        results = []
        while node is not None:
            for k, v in zip(node.keys, node.children):
                if k > max_key:
                    return results
                if k >= min_key:
                    results.append((k, v))
            node = node.next
        return results
