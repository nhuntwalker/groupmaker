
import os
import json
import faker
import pytest
from copy import deepcopy
from creator import choose_pairs, get_past_pairs, write_past_pairs


fake = faker.Faker()
STUDENT_LIST = [fake.name() for _ in range(31)]
CACHE_PATH = 'pairs_test.json'
# STRAGLER_LIMIT is the maximum iterations before an excess partner (a third)
# has to be grouped with a pair one of which they've already been with.
STRAGLER_LIMIT, LIMIT = 13, 23


@pytest.fixture
def past_pairs():
    """Give past_pairs then clear cache after test."""
    yield get_past_pairs(CACHE_PATH)
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)


def test_each_student_assigned_to_one_group(past_pairs):
    """Test every student is only assigned to one group."""
    for i in range(LIMIT):
        pairs, past_pairs = choose_pairs(STUDENT_LIST, past_pairs)
        assigned = [n for pair in pairs for n in pair]
        assert len(assigned) == len(set(assigned)) == len(STUDENT_LIST)


def test_always_new_partners(past_pairs):
    """Test students are never assigned partners they've already had."""
    for i in range(STRAGLER_LIMIT):
        pairs, new_past_pairs = choose_pairs(STUDENT_LIST, deepcopy(past_pairs))
        for pair in pairs:
            for student in pair:
                for partner in pair:
                    assert student not in past_pairs[partner]
        past_pairs = new_past_pairs


def test_past_pairs_updated(past_pairs):
    """Test that the cache gets updated."""
    for i in range(LIMIT):
        pairs, new_past_pairs = choose_pairs(STUDENT_LIST, deepcopy(past_pairs))
        write_past_pairs(new_past_pairs, CACHE_PATH)
        with open(CACHE_PATH) as f:
            new_past_pairs = json.load(f)
        for student in new_past_pairs:
            group = list(next(x for x in pairs if student in x))
            partners = [s for s in group if s != student]
            assert past_pairs[student] + partners == new_past_pairs[student]
        past_pairs = new_past_pairs
