class RecordDict(dict):
    """
    Dictionary that acts like a class with keys accessed as attributes.
    `inst['foo']` and `inst.foo` is the same.
    """
    def __init__(self, **kwargs):
        super(RecordDict, self).__init__(**kwargs)
        self.__dict__ = self

    def exclude(self, *args):
        for key in args:
            del self[key]
        return self

    @classmethod
    def from_list(cls, container, key, val):
        kwargs = dict((s[key], s[val]) for s in container)
        return cls(**kwargs)
