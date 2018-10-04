import pytest

from synopse import Structure, Component
from synopse.lifecycle import Lifecycle


class TestStructure:
    def test_init_with_args_and_kwargs(self):
        assert {"key": Component(), 0: Component(), 1: Component()} \
               == Structure(Component(), Component(), key=Component())

    def test_init_with_none(self):
        assert {} == Structure(None)

    def test_init_with_none_as_keyword(self):
        assert {} == Structure(key=None)

    def test_init_with_object(self):
        assert {0: Component()} == Structure(Component())

    def test_init_with_iterable(self):
        assert {0: Component(), 1: Component()} \
               == Structure((Component(), Component()))

    def test_init_with_nested_iterable(self):
        assert {0: Component(), 1: Component()} \
               == Structure((Component(), (Component(),)))

    def test_eq_with_dict(self):
        assert {0: Component(), "key": Component()} \
               == Structure(Component(), key=Component())

    def test_getitem_keyword(self):
        assert Component() == Structure(key=Component())["key"]

    def test_getitem_keyword_default(self):
        assert Structure()["key"] is None

    def test_getitem_positional(self):
        assert Component() == Structure(None, Component(), None)[0]

    def test_getitem_positional_default(self):
        assert Structure(Component())[1] is None

    def test_setitem_keyword(self):
        structure = Structure()
        structure["key"] = Component()
        assert {"key": Component()} == structure

    def test_setitem_append_to_positionals(self):
        structure = Structure()
        structure[0] = Component()
        assert {0: Component()} == structure

    def test_setitem_insert_before_if_index_already_used(self):
        structure = Structure(Component(), Component())
        structure[1] = Component()
        assert {0: Component(), 1: Component(), 2: Component()} == structure

    def test_setitem_raises_indexerror_when_key_gt_len(self):
        structure = Structure()
        with pytest.raises(IndexError):
            structure[1] = Component()

    def test_delitem_from_positional(self):
        structure = Structure(Component(), Component())
        del structure[1]
        assert {0: Component()} == structure

    def test_delitem_from_keywords(self):
        structure = Structure(key=Component(), another=Component())
        del structure["another"]
        assert {"key": Component()} == structure

    def test_keys_return_keywords_as_set(self):
        assert {"key", "another"} \
               == Structure(key=Component(), another=Component()).keys()

    def test_keys_return_positional_indexes_as_set(self):
        assert {0, 1} == Structure(Component(), Component()).keys()

    def test_key_return_mixed(self):
        structure = Structure(Component(), k=Component())
        assert {"k", 0} == structure.keys()


class LifecycleMock(Lifecycle):
    def __init__(self):
        self.called_hooks = []

    def mount(self):
        self.called_hooks.append("mount")

    def unmount(self):
        self.called_hooks.append("unmount")

    def update(self, target=None):
        self.called_hooks.append("update")


class TestStructureLifecycleHooks:
    def test_mount_on_setitem(self):
        structure = Structure()
        lifecycle = LifecycleMock()
        structure["key"] = lifecycle
        assert ["mount", "update"] == lifecycle.called_hooks

    def test_unmount_on_delitem(self):
        lifecycle = LifecycleMock()
        structure = Structure(lifecycle)
        del structure[0]
        assert ["unmount"] == lifecycle.called_hooks
