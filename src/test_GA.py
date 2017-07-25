from src.GA import GA
from BitVector import BitVector
from unittest import TestCase
from src.individual import Individual


class TestGA(TestCase):
    def test_sat(self):
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(GA.sat(ind, [9, -5]), True)
        self.assertEqual(GA.sat(ind, [1, 3, 6]), False)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(GA.sat(ind, [-6, -4]), False)

    def test_sat_crossover(self):
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        ind.defined = BitVector(bitlist=[0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(GA.sat_crossover(ind, [9, -5]), False)
        ind.set_defined(9)
        self.assertEqual(GA.sat_crossover(ind, [9, -5]), True)

    def test_evaluate(self):
        ga = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(ga.evaluate(ind), 1)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 0])
        self.assertEqual(ga.evaluate(ind), 2)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 0])
        self.assertEqual(ga.evaluate(ind), 2)

    def test_improvement(self):
        ga = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(ga.improvement(ind, 1), 1)
        self.assertEqual(ga.improvement(ind, 6), 1)
        ind.flip(6)
        self.assertEqual(ga.improvement(ind, 6), -1)

    def test_corrective_clause(self):
        self.assertEqual(1, 1)

    def test_corrective_clause_with_truth_maintenance(self):
        self.assertEqual(1, 1)

    def test_standard_tabu_choose(self):
        self.assertEqual(1, 1)

    def test_standard_tabu(self):
        self.assertEqual(1, 1)

    def test_choose_rvcf(self):
        self.assertEqual(1, 1)

    def test_weight(self):
        self.assertEqual(1, 1)

    def test_degree(self):
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(GA.degree(ind, [9, -5]), 0)
        self.assertEqual(GA.degree(ind, [1, 3, 6]), 1)
        ind.data = BitVector(bitlist=[0, 0, 1, 0, 0, 0, 1, 1, 0])
        self.assertEqual(GA.degree(ind, [7, 8, -3]), 3)


    def test_tabu_with_diversification(self):
        self.assertEqual(1, 1)

    def test_check_flip(self):
        self.assertEqual(1, 1)

    def test_fluerent_and_ferland(self):
        self.assertEqual(1, 1)

    def test_select(self):
        self.assertEqual(1, 1)

    def test_create_population(self):
        self.assertEqual(1, 1)

    def test_is_satisfied(self):
        self.assertEqual(1, 1)

    def test_replace(self):
        self.assertEqual(1, 1)

    def test_gasat(self):
        self.assertEqual(1, 1)

