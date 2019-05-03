from partialize import partialize


def test_func(a, b, c, d=None, *, e=None):
    return [a, b, c, d, e]


test_func_partialize = partialize(test_func)


def time_partialize():
    f = test_func_partialize()
    f(d="foo")(e="bar")("one")("two")("three")


def time_default():
    test_func("one", "two", "three", d="foo", e="bar")
