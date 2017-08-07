import sys
from GA import GA
from optparse import OptionParser
from server import SATServer

default_port = 55555
default_host = "localhost"


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class SATController:
    def __init__(self):
        self.GA = None

    def has_ga_instance(self):
        return self.GA is not None

    def create_ga(self, ga_parameters):
        self.GA = GA(**ga_parameters)

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

    if len(argv) == 0:
        # Start the interface
        server_thread = SATServer(default_host, default_port)
        server_thread.start()
    else:
        parser = OptionParser()
        parser.add_option("-p", "--port", dest="port", type="int", help="Port number on which the server should run.",
                          metavar="<port>")
        parser.add_option("-f", "--file", dest="file", type="string", help="The CNF source.", metavar="<filename>")
        parser.add_option("--tabu-list-length", dest="tabu_list_length", type="int", help="",
                          metavar="<tabu list length>")
        parser.add_option("--max-false", dest="max_false", type="int", help="", metavar="<max false>")
        parser.add_option("--rec", dest="rec", type="int", help="", metavar="<rec>")
        parser.add_option("-k", dest="k", type="int", help="", metavar="<k>")
        parser.add_option("--max-generations", dest="max_generations", type="int", help="", metavar="<max generations>")
        parser.add_option("--population-size", dest="population_size", type="int", help="", metavar="<population size>")
        parser.add_option("--sub-population-size", dest="sub_population_size", type="int", help="",
                          metavar="<sub population size>")
        parser.add_option("--crossover-operator", dest="crossover_operator", type="string", help="",
                          metavar="<crossover operator>")
        parser.add_option("--max-flip", dest="max-flip", type="int", help="", metavar="<max flip>")
        parser.add_option("--rvcf", dest="is_rcvf", type="string", help="")
        parser.add_option("--diversification", dest="is_diversification", type="string", help="")
        parser.add_option("--method", dest="method", type="string", help="", metavar="<method>")

        (options, args) = parser.parse_args()
        options = vars(options)
        if options["port"] is not None:
            # Port has been specified start server
            server_thread = SATServer(default_host, options["port"])
            server_thread.start()
        else:
            f = open("example.cnf", "r")  # TODO: Get filename passed in
            formula, number_of_variables, number_of_clauses = controller.parse_formula(f.readlines())
            # TODO: Create the headless, local GA instance here
            print("Server not wanted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
