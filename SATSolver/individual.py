"""
    Module: Individual
    Description: Defines classes related to the creation and manipulation of
    an Individual for use in the genetic algorithm.
"""

from BitVector import BitVector
from bitarray import bitarray
import random


class Individual:
    """ Encapsulates an Individual in the GA. """

    BIT_VECTOR = 0
    BIT_ARRAY = 1

    def __init__(self, length=0, method=None, defined=False, value=None):

        """ Creates a bit string of a certain length, using a certain underlying
        implementation.  """

        self.length = length

        if method not in [0, 1]:
            self.method = Individual.BIT_VECTOR
        else:
            self.method = method

        if self.method == Individual.BIT_VECTOR:
            self.data = BitVector(size=length)
            self.data = self.data.gen_random_bits(length)
            self.defined = BitVector(size=length)
            
            if defined:
                self.defined = None
            else:
                self.defined.reset(0)

            if value is not None:
                self.data = BitVector(bitlist=value)

        elif self.method == Individual.BIT_ARRAY:
            self.defined = bitarray(length)
            self.data = bitarray(length)

            if defined:
                self.defined = None
            else:
                self.defined.setall(False)

            if value is not None:
                self.data = [bool(X) for X in value]

    def __str__(self):

        """ Creates a consistent string method across implementations. """

        if self.method == Individual.BIT_VECTOR:
            return str(self.data)
        elif self.method == Individual.BIT_ARRAY:
            return self.data.to01()
        return ""

    def __call__(self, b):
        return self.get(b)

    def get(self, b):

        """ Returns the value at position b, that is either 1 or 0. """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            return self.data[b]
        elif self.method == Individual.BIT_ARRAY:
            return int(self.data[b])

    def set(self, b, v):

        """ Sets the bit at position b to value v. """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.data[b] = v
        elif self.method == Individual.BIT_ARRAY:
            self.data[b] = bool(v)

    def flip(self, b):

        """ Flips the bit at position b. """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.data[b] ^= 1
        elif self.method == Individual.BIT_ARRAY:
            self.data[b] = not self.data[b]

    def set_defined(self, b):

        """ Sets a certain bit b as defined. """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.defined[b] = 1
        elif self.method == Individual.BIT_ARRAY:
            self.defined[b] = not self.data[b]

    def get_defined(self, b):

        """ Gets whether a certain bit is defined or not (boolean) """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            return True if self.defined[b] == 1 else False
        else:
            return self.defined[b]

    def allocate(self, first, second):

        """ Allocates uniformly from either first or second parent. """

        # causes all unset bits not to be set
        # for i in range(1, self.length+1):
        #     self.set_defined(i)
        for i in range(self.length):
            #i is inconsistently indexed in comparison to other places get_defined and set are called thus 1 must be added
            index = i + 1
            if not self.get_defined(index):
                if bool(random.getrandbits(1)):
                    self.set(index, first.get(index))
                else:
                    self.set(index, second.get(index))
                self.set_defined(index)


class Factory:
    """ A factory class for creating individuals in bulk. """

    @staticmethod
    def create(length, method, amount):
        """ Creates an array of individuals. """

        array = [Individual(length, method, True) for _ in range(amount)]
        return array
