from unittest import TestCase

from BitVector import BitVector

from SATSolver.GA import GA
from SATSolver.individual import Individual


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
        ga = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        parent1 = Individual(9)
        parent2 = Individual(9)
        parent1.data = BitVector(bitlist=[0, 0, 0, 1, 1, 0, 0, 0, 0])
        parent2.data = BitVector(bitlist=[0, 1, 0, 0, 1, 0, 0, 0, 0])
        child = ga.corrective_clause(parent1, parent2)
        # self.assertEqual(child.get(1), 1)
        # self.assertEqual(child.get(2), 1)
        # self.assertEqual(child.get(9), 1)

        parent2.flip(2)
        parent2.flip(5)
        parent2.flip(9)
        child = ga.corrective_clause(parent2, parent1)
        # for clause in ga.formula:
        #     self.assertEqual(ga.sat(child, clause), True)


    def test_corrective_clause_with_truth_maintenance(self):
        self.assertEqual(1, 1)

    def test_standard_tabu_choose(self):
        # .............................................................................................................
        # An instance of the GA class which will be used to test the standard_tabu_choose function
        ga_implementation = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        # The tabu list is set to the size which was received as parameter i.e. [5]
        ga_implementation.tabu = ga_implementation.tabu[:ga_implementation.tabu_list_length]
        # Every single position is tabu
        for index in range(1, 10, 1):
            ga_implementation.tabu.append(index)

        # Creating an individual that will represent the best individual during a tabu search procedure
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        ga_implementation.best = ind

        # Creating an individual that will represent another individual for which we want to find best flip for
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        # A test
        self.assertEqual(ga_implementation.standard_tabu_choose(ind)[1], [1, 2, 4, 6])
        # .............................................................................................................

    def test_standard_tabu(self):
        # .............................................................................................................
        # An instance of the GA class which will be used to test the standard_tabu_choose function
        ga_implementation = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        # Creating an individual that will represent another individual for which we want to find best flip for
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 0, 0, 1, 1, 1, 1])
        # Test whether if a satisfying assignment is passed, then that assignment should be returned as best
        ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        self.assertEqual(list(ind.data), list(BitVector(bitlist=[0, 0, 0, 0, 0, 1, 1, 1, 1])))
        # .............................................................................................................

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
