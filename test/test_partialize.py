import unittest
import logging

from partialize import partialize


class TestPartialize(unittest.TestCase):

    def test_partialize_args_kwargs(self):

        @partialize
        def test_function(a, b, *args, c='kwarg0'):
            return (a, b, *args, c)

        p = test_function(0, 1, 2)
        self.assertTrue(p == (0, 1, 2, 'kwarg0'))
        p = test_function(c="kwarg1")
        self.assertTrue(p(0, 1) == (0, 1, "kwarg1"))
        # self.assertTrue(p(0, 1, "a") == self.expected_value)

    # @unittest.skip("")
    def test_partialize_args_required_kwarg(self):

        @partialize
        def test_function(a, *args, b, c="kwarg0"):
            return (a, *args, b, c)

        p = test_function(0, 1, b="foo")
        self.assertTrue(p == (0, 1, "foo", "kwarg0"))
        p = test_function(b="foo", c="kwarg1")
        self.assertTrue(p(0) == (0, "foo", "kwarg1"))

    # @unittest.skip("")
    def test_partialize_required_kwarg(self):

        @partialize
        def test_function(a, b, *, d, c='kwarg0'):
            return (a, b, d, c)

        # we can call the function with full argument compliment
        p = test_function(0, 1, d="foo", c="bar")
        self.assertTrue(p == (0, 1, "foo", "bar"))
        # we can call function without keyword arguments with defaults
        p = test_function(0, 1, d="foo")
        self.assertTrue(p == (0, 1, "foo", "kwarg0"))

        # we can "lock in" parameters for later use.
        p = test_function(c="still")
        self.assertTrue(p(0, 1, d="here") == (0, 1, "here", "still"))
        p = test_function(d="flames", c="slimes")
        p = p(0)
        self.assertTrue(p(1) == (0, 1, "flames", "slimes"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
