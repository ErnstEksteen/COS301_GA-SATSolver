import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
print(myPath)
sys.path.insert(0, myPath + '/../SATSolver')

from unittest import TestCase
from individual import Factory


class TestFactory(TestCase):
    """
    Test class for Factory
    """
    
    def test_create(self):
        factory = Factory()
        population = factory.create(10, None, 50)
        self.assertEqual(50, len(population))
        for individual in population:
            self.assertEqual(individual.length, 10)
