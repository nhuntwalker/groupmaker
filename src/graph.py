# -*- coding: utf-8 -*-
"""Graph for use with the pair creator."""


class Graph(object):
    """A weighted, undirected graph."""

    def __init__(self, starter={}):
        """Constructor for the graph."""
        self._container = starter
        self._size = len(starter)

    def insert(self, val):
        """Add a new value to the graph."""
        self._container.setdefault(val, {})
        self._size = len(self._container)

    def add_edge(self, val1, val2):
        """Add an edge between val1 and val2."""
        if val1 not in self:
            self.insert(val1)
        if val2 not in self:
            self.insert(val2)
        self._container[val2][val1] = 1 if val1 not in self._container[val2] else self._container[val2][val1] + 1
        self._container[val1][val2] = 1 if val2 not in self._container[val1] else self._container[val1][val2] + 1

    def remove(self, val):
        """Remove node from graph."""
        for node in self._container[val]:
            self._container[node].remove(val)
        del self._container[val]

    @property
    def size(self):
        return self._size

    def __contains__(self, val):
        return val in self._container
