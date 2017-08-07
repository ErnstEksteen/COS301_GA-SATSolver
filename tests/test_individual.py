from unittest import TestCase
from individual import Individual
from BitVector import BitVector
from bitarray import bitarray


class TestIndividual(TestCase):
    """
    Testing class for Individual.
    """

    def test_get(self):
        ind = Individual(9, Individual.BIT_VECTOR)

        # BitVector implementation

        ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
        ind.method = Individual.BIT_VECTOR
        self.assertEqual(ind.get(5), 1)
        self.assertEqual(ind.get(1), 0)
        self.assertEqual(ind.get(10), None)

        # bittarray implementation

        ind.data = bitarray("011010100")
        ind.method = Individual.BIT_ARRAY
        self.assertEqual(ind.get(5), 1)
        self.assertEqual(ind.get(1), 0)
        self.assertEqual(ind.get(10), None)

    def test_set(self):
        ind = Individual(9, Individual.BIT_VECTOR)

        ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
        ind.method = Individual.BIT_VECTOR
        ind.set(2, 1)
        self.assertEqual(ind.get(2), 1)
        ind.set(7, 0)
        self.assertEqual(ind.get(7), 0)
        ind.set(6, 1)
        self.assertEqual(ind.get(6), 1)

        # bittarray implementation

        ind.data = bitarray("011010100")
        ind.method = Individual.BIT_ARRAY
        ind.set(2, 1)
        self.assertEqual(ind.get(2), 1)
        ind.set(7, 0)
        self.assertEqual(ind.get(7), 0)
        ind.set(6, 1)
        self.assertEqual(ind.get(6), 1)

    def test_flip(self):
        ind = Individual(9, Individual.BIT_VECTOR)

        # BitVector implementation

        ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
        ind.method = Individual.BIT_VECTOR
        ind.flip(1)
        self.assertEqual(ind.get(1), 1)
        ind.flip(8)
        self.assertEqual(ind.get(8), 1)
        ind.flip(4)
        self.assertEqual(ind.get(4), 1)

        # bittarray implementation

        ind.data = bitarray("011010100")
        ind.method = Individual.BIT_ARRAY
        ind.flip(1)
        self.assertEqual(ind.get(1), 1)
        ind.flip(8)
        self.assertEqual(ind.get(8), 1)
        ind.flip(4)
        self.assertEqual(ind.get(4), 1)

    def test_set_defined(self):
        ind = Individual(9, Individual.BIT_VECTOR)
        for x in range(1, 10):
            self.assertEqual(ind.get_defined(x), False)
        for x in range(1, 10):
            ind.set_defined(x)
            self.assertEqual(ind.get_defined(x), True)

    def test_get_defined(self):
        ind = Individual(9, Individual.BIT_VECTOR)
        for x in range(1, 10):
            self.assertEqual(ind.get_defined(x), False)
        for x in range(1, 10):
            ind.set_defined(x)
            self.assertEqual(ind.get_defined(x), True)

    def test_allocate(self):
        ind = Individual(9, Individual.BIT_VECTOR)
        ind.allocate(ind, ind)
        for x in range(1, 10):
            self.assertEqual(ind.get_defined(x), True)
