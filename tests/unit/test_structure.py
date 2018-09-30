import pytest

from pricky import Structure, Blueprint
from pricky.lifecycle import Lifecycle


class TestStructure:
    def test_init_with_dict(self):
        assert {"key": Blueprint()} == Structure({"key": Blueprint()})

    def test_init_with_dict_containing_positional(self):
        assert {"key": Blueprint(), 0: Blueprint(), 1: Blueprint()} \
               == Structure({"key": Blueprint(),
                             "__positional__": (Blueprint(), Blueprint())})

    def test_init_with_none(self):
        assert {} == Structure(None)

    def test_init_with_object(self):
        assert {0: Blueprint()} == Structure(Blueprint())

    def test_init_with_iterable(self):
        assert {0: Blueprint(), 1: Blueprint()} \
               == Structure((Blueprint(), Blueprint()))

    def test_eq_with_dict(self):
        assert {"0": Blueprint(), "key": Blueprint()} \
               == Structure({"0": Blueprint(), "key": Blueprint()})

    def test_getitem_keyword(self):
        assert Blueprint() == Structure({"key": Blueprint()})["key"]

    def test_getitem_keyword_default(self):
        assert Structure()["key"] is None

    def test_getitem_positional(self):
        assert Blueprint() == Structure((None, Blueprint(), None))[1]

    def test_getitem_positional_default(self):
        assert Structure((Blueprint(),))[1] is None

    def test_setitem_keyword(self):
        structure = Structure()
        structure["key"] = Blueprint()
        assert {"key": Blueprint()} == structure

    def test_setitem_append_to_positionals(self):
        structure = Structure()
        structure[0] = Blueprint()
        assert {0: Blueprint()} == structure

    def test_setitem_insert_before_if_index_already_used(self):
        structure = Structure((Blueprint(), Blueprint()))
        structure[1] = Blueprint()
        assert {0: Blueprint(), 1: Blueprint(), 2: Blueprint()} == structure

    def test_setitem_raises_indexerror_when_key_gt_len(self):
        structure = Structure()
        with pytest.raises(IndexError):
            structure[1] = Blueprint()

    def test_delitem_from_positional(self):
        structure = Structure((None, Blueprint(), None))
        del structure[1]
        assert {0: None, 1: None} == structure

    def test_delitem_from_keywords(self):
        structure = Structure({"key": Blueprint(), "another": None})
        del structure["another"]
        assert {"key": Blueprint()} == structure

    def test_keys_return_keywords_as_set(self):
        assert {"key", "another"} \
               == Structure({"key": Blueprint(), "another": Blueprint()}).keys()

    def test_keys_return_positional_indexes_as_set(self):
        assert {0, 1} == Structure((Blueprint(), Blueprint())).keys()

    def test_key_return_mixed(self):
        structure = Structure(
            {"k": Blueprint(), "__positional__": (Blueprint(),)}
        )
        assert {"k", 0} == structure.keys()


class LifecycleMock(Lifecycle):
    def __init__(self):
        self.called_hooks = []

    def mount(self):
        self.called_hooks.append("mount")

    def unmount(self):
        self.called_hooks.append("unmount")


class TestStructureLifecycleHooks:
    def test_mount_on_setitem(self):
        structure = Structure()
        lifecycle = LifecycleMock()
        structure["key"] = lifecycle
        assert ["mount"] == lifecycle.called_hooks

    def test_unmount_on_delitem(self):
        lifecycle = LifecycleMock()
        structure = Structure(lifecycle)
        del structure[0]
        assert ["unmount"] == lifecycle.called_hooks
