import unittest

from partialize import partialize


class TestPartialize(unittest.TestCase):

    def test_partialize(self):

        expected_value = "hello"
        
        @partialize
        def test_function(a, b, *, d, c='kwarg0'):
            return "hello"

        # we can call the function with full argument compliment
        p = test_function(0, 1, d="foo", c="bar")
        self.assertTrue(p == expected_value)
        # we can call function without keyword arguments with defaults
        p = test_function(0, 1, d="foo")
        self.assertTrue(p == expected_value)

        # we can "lock in" parameters for later use.
        p = test_function(c="still")
        self.assertTrue(p(0, 1, d="here") == expected_value)
        p = test_function(d="flames", c="slimes")
        p = p(0)
        self.assertTrue(p(1) == expected_value)


if __name__ == "__main__":
    unittest.main()
