from pricky import Structure


class TestStructure:
    def test_rebuild_structure_from_dict(self):
        assert {0: True} == Structure({0: True})

    def test_rebuild_structure_from_none(self):
        assert {} == Structure(None)

    def test_rebuild_structure_from_blueprint(self):
        assert {0: True} == Structure(True)

    def test_rebuild_structure_from_iterable(self):
        assert {0: 0, 1: 1, 2: 2} == Structure((0, 1, 2))
