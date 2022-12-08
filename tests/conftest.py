import pytest

from unmodifiable import ImmutableList, unmodifiable_list


class Orders:

    order_items: ImmutableList = []
    old_items = []  # no type hint or wrong type hint provided
    removed_order_items: ImmutableList = []

    def __init__(self):
        self.__order_items = ["New Order 1", "New Order 2"]
        self.__failed_items = ["Failed Order 1", "Failed Order 2"]
        self.__old_items = ["Old Item 1", "Old Item 2"]
        self.__removed_order_items = ["Removed 1", "Removed 2"]

    def get_order_items(self):
        with unmodifiable_list(self, "__order_items") as unmodifiable:
            return unmodifiable

    def get_failed_items(self):
        # This should fail as there is no corresponding public name
        with unmodifiable_list(self, "__failed_items") as unmodifiable:
            return unmodifiable

    def get_old_items(self):
        # This should fail as the corresponding public name has no type hint - it should be ImmutableList
        with unmodifiable_list(self, "__old_items") as unmodifiable:
            return unmodifiable

    def get_removed_order_items(self):
        # This is the same as data from context manager
        with unmodifiable_list(self, "__removed_order_items"):
            return self.removed_order_items


@pytest.fixture
def get_order_obj():
    return Orders()
