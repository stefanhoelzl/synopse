from pricky import Structure


class TestStructure:
    def test_init_with_dict(self):
        assert {"key": True} == Structure({"key": True})

    def test_init_with_dict_cast_keys_to_string(self):
        assert {"0": True} == Structure({0: True})

    def test_init_with_dict_containing_iterable(self):
        assert {"key": True, 0: 1, 1: 2, 2: 3} == Structure(
            {"key": True, "__positional__": (1, 2, 3)}
        )

    def test_init_with_none(self):
        assert {} == Structure(None)

    def test_init_with_object(self):
        assert {0: True} == Structure(True)

    def test_init_with_iterable(self):
        assert {0: 0, 1: 1, 2: 2} == Structure((0, 1, 2))

    def test_eq_with_dict(self):
        assert {"0": 0, "key": 1} == Structure({0: 0, "key": 1})

    def test_getitem_keyword(self):
        assert Structure({"key": True})["key"]

    def test_getitem_keyword_default(self):
        assert Structure()["key"] is None

    def test_getitem_positional(self):
        assert 2 == Structure((1, 2, 3))[1]

    def test_getitem_positional_default(self):
        assert Structure((1,))[1] is None

    def test_setitem_keyword(self):
        structure = Structure()
        structure["key"] = True
        assert {"key": True} == structure

    def test_setitem_append_to_positionals(self):
        structure = Structure()
        structure[0] = True
        assert {0: True} == structure

    def test_delitem_from_positional(self):
        structure = Structure((1, 2, 3))
        del structure[1]
        assert {0: 1, 1: 3} == structure

    def test_delitem_from_keywords(self):
        structure = Structure({"key": 1, "another": 0})
        del structure["another"]
        assert {"key": 1} == structure

    def test_keys_return_keywords_as_set(self):
        assert {"key", "another"} == Structure({"key": 0, "another": 1}).keys()

    def test_keys_return_positional_indexes_as_set(self):
        assert {0, 1} == Structure((1, 2)).keys()

    def test_key_return_mixed(self):
        assert {"k", 0} == Structure({"k": True, "__positional__": (1,)}).keys()
