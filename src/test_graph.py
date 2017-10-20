# -*- coding: utf-8 -*-
"""Tests for a weighted, undirected graph."""
import pytest


@pytest.fixture
def empty_graph():
    """An empty graph for testing."""
    from graph import Graph
    g = Graph()
    return g


def test_can_insert_value_into_graph(empty_graph):
    empty_graph.insert('person1')
    assert empty_graph.size == 1
    assert empty_graph._container['person1']


def test_when_value_inserted_has_neighbor_dict(empty_graph):
    empty_graph.insert('person1')
    assert empty_graph._container['person1'] == []


def test_contains_method_returns_bool_if_contains_val(empty_graph):
    assert 'person1' not in empty_graph
    empty_graph.insert('person1')
    assert 'person1' in empty_graph


def test_add_edge_adds_either_value_if_not_exist(empty_graph):
    empty_graph.add_edge('person1', 'person2')
    assert 'person1' in empty_graph
    assert 'person2' in empty_graph


def test_add_edge_defaults_weight_to_1_for_new_edge(empty_graph):
    empty_graph.add_edge('person1', 'person2')
    assert empty_graph._container['person1']['person2'] == 1
    assert empty_graph._container['person2']['person1'] == 1


def test_add_edge_increments_edge_weight_for_repeats(empty_graph):
    empty_graph.add_edge('person1', 'person2')
    empty_graph.add_edge('person2', 'person1')
    assert empty_graph._container['person1']['person2'] == 2
    assert empty_graph._container['person2']['person1'] == 2


def test_remove_deletes_val_and_any_references(empty_graph):
    empty_graph.add_edge('person1', 'person2')
    empty_graph.add_edge('person3', 'person2')
    empty_graph.remove('person2')
    assert 'person2' not in empty_graph
    assert 'person2' not in empty_graph._container['person1']
    assert 'person2' not in empty_graph._container['person3']
