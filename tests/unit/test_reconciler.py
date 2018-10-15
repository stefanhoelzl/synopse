from synopse.reconciler import Reconciler


class ValueMock:
    def __init__(self, eq=False):
        self.equals = eq
        self.updated_with = None
        self.created = False
        self.destroyed = False

    def __eq__(self, other):
        return self.equals

    def update(self, new):
        self.updated_with = new

    def create(self):
        self.created = True

    def destroy(self):
        self.destroyed = True


class DifferentValueMock(ValueMock):
    pass


class TestReconciler:
    def test_keep_old_if_eq(self):
        old = ValueMock(eq=True)
        assert old is Reconciler.reconcile(old, ValueMock())
        assert old.updated_with is None

    def test_update_if_same_class_but_not_eq(self):
        old, new = ValueMock(), ValueMock()
        assert old is Reconciler.reconcile(old, new)
        assert new is old.updated_with

    def test_replace_if_different_classes(self):
        new = ValueMock()
        assert new is Reconciler.reconcile(DifferentValueMock(), new)

    def test_call_lifecycle_on_replace(self):
        old, new = ValueMock(), DifferentValueMock()
        Reconciler.reconcile(old, new)
        assert old.destroyed
        assert new.created
