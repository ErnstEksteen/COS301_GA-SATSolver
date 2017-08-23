import sys
import abc
from SATSolver.GA import GA
from RequestHandler import *
from optparse import OptionParser
from SATSolver.server import SATServer

default_port = 55555
default_host = "localhost"


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._generation_count = None

    @abc.abstractmethod
    def update(self, arg):
        pass


@singleton
class SATController(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.GA = None
        self.server_thread = None

    def update(self, arg):
        self._generation_count = arg
        if self.server_thread is not None:
            self.send_update(RequestHandler.encode("PROGRESS", [[self._generation_count, self.GA.max_generations]]))
        else:
            print(arg)

    def send_update(self, msg):
        self.server_thread.push_to_all(msg)

    def has_ga_instance(self):
        return self.GA is not None

    def create_ga(self, ga_parameters):

        new_params = {key: ga_parameters[key] for key in ga_parameters.keys() if ga_parameters[key] is not None}
        self.GA = GA(**new_params)
        self.GA.attach(self)

    def parse_formula(self, raw_formula):
        """
        Takes a list of lines read from the input file and 
        """
        # Read all the lines from the file that aren't comments
        lines = [line.replace("\n", "") for line in raw_formula if line[0] != "c" and line.strip() != ""]
        numberOfVariables, numberOfClauses = int(lines[0].split()[2]), int(lines[0].split()[3])
        formula = []

        # Go through the lines and create numberOfClauses clauses
        line = 1
        # for line in range(1, len(lines)):
        while line < len(lines):
            clause = []
            # We need a while loop as a clause may be split over many lines, but eventually ends with a 0
            end_of_clause = False
            while line < len(lines) and not end_of_clause:
                # Split the line and append a list of all integers, excluding 0, to clause
                clause.append([int(variable.strip()) for variable in lines[line].split() if int(variable.strip()) != 0])
                # If this line ended with a 0, we reached the end of the clause
                if int(lines[line].split()[-1].strip()) == 0:
                    end_of_clause = True
                    line += 1
                # Otherwise continue reading this clause from the next line
                else:
                    line += 1
            # clause is now a list of lists, so we need to flatten it and convert it to a list
            formula.append(tuple([item for sublist in clause for item in sublist]))
        return formula, numberOfVariables, numberOfClauses


def main(argv):
    """
        The main method of the program. It is responsible for:
         - Managing the server and request handler
         - Spawning the GA instance
         - Starts the interface or parses command-line arguments
        And finally returns the exit code
    """

    controller = singleton(SATController)()
    message_decoder = RequestHandler()

    if len(argv) == 0:
        # Start the interface
        controller.server_thread = SATServer(default_host, default_port, message_decoder.decode)
        controller.server_thread.start()
    else:
        parser = OptionParser()
        parser.add_option("-p", "--port", dest="port", type="int", help="Port number on which the server should run.",
                          metavar="<port>")
        parser.add_option("-f", "--file", dest="file", type="string", help="The CNF source.", metavar="<filename>")
        parser.add_option("--tabu-list-length", dest="tabu_list_length", type="int", help="",
                          metavar="<tabu list length>")
        parser.add_option("--max-false", dest="max_false", type="int",
                          help='How many times a clause must be false to be considered a "stumble-clause".',
                          metavar="<max false>")
        parser.add_option("--rec", dest="rec", type="int", help="", metavar="<rec>")
        parser.add_option("-k", dest="k", type="int", help="How long an atom in a stumble-clause is prevented from "
                                                           "flipping.", metavar="<k>")
        parser.add_option("--max-generations", dest="max_generations", type="int", help="", metavar="<max generations>")
        parser.add_option("--population-size", dest="population_size", type="int", help="", metavar="<population size>")
        parser.add_option("--sub-population-size", dest="sub_population_size", type="int", help="",
                          metavar="<sub population size>")
        parser.add_option("--crossover-operator", dest="crossover_operator", type="string", help="",
                          metavar="<crossover operator>")
        parser.add_option("--max-flip", dest="max_flip", type="int", help="", metavar="<max flip>")
        parser.add_option("--rvcf", dest="is_rvcf", type="string", help="")
        parser.add_option("--diversification", dest="is_diversification", type="string", help="")
        parser.add_option("--method", dest="method", type="string", help="", metavar="<method>")

        (options, args) = parser.parse_args()
        options = vars(options)
        if options["port"] is not None:
            # Port has been specified start server
            controller.server_thread = SATServer(default_host, options["port"], RequestHandler.decode)
            controller.server_thread.start()
        f = open("../examples/hgen2-a.cnf", "r")  # TODO: Get filename passed in
        formula, number_of_variables, number_of_clauses = controller.parse_formula(f.readlines())
        del options['port']
        del options['file']
        options['formula'] = formula
        options['number_of_variables'] = number_of_variables
        options['number_of_clauses'] = number_of_clauses
        controller.create_ga(options)
        print("Going into the dark GA hole now from which there apparently is no return.")
        print(controller.GA.gasat())


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
