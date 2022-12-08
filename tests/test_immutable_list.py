import pytest

from unmodifiable import UnsupportedOperationException


def test_get_immutable_list(get_order_obj):
    items = get_order_obj.get_order_items()
    with pytest.raises(UnsupportedOperationException):
        items.append("new")

    assert items == ["New Order 1", "New Order 2"]


def test_regenerate_immutable_list(get_order_obj):
    get_order_obj._Orders__order_items.append("fake")

    items = get_order_obj.get_order_items()
    with pytest.raises(UnsupportedOperationException):
        items.append("new")

    assert items == ["New Order 1", "New Order 2", "fake"]


def test_reset_list(get_order_obj):
    get_order_obj._Orders__order_items = []
    items = get_order_obj.get_order_items()
    assert items == []


def test_if_lists_are_different_objects(get_order_obj):
    assert hex(id(get_order_obj._Orders__order_items)) != hex(
        id(get_order_obj.get_order_items())
    )
    assert get_order_obj._Orders__order_items is not get_order_obj.get_order_items()


def test_if_private_list_has_no_corresponding_public_list(get_order_obj):
    with pytest.raises(AttributeError):
        get_order_obj.get_failed_items()


def test_if_public_list_has_wrong_type(get_order_obj):
    with pytest.raises(AttributeError):
        get_order_obj.get_old_items()


def test_check_global_public_list_not_from_the_context_manager(get_order_obj):
    items = get_order_obj.get_removed_order_items()
    assert items == ["Removed 1", "Removed 2"]
    with pytest.raises(UnsupportedOperationException):
        items.append("new")
