import threading
import abc
import time
from GA import GA
from GA import GAStop
from server import BColors


class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if cls.__singleton_instance is None:
            with cls.__singleton_lock:
                if cls.__singleton_instance is None:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


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


class SATController(Observer, SingletonMixin):

    def __init__(self):
        Observer.__init__(self)
        self.GA = None
        self.server_thread = None
        self.time_started = None
        self.time_finished = None
        self.ga_thread = None

    def update(self, arg):
        from SATSolver.RequestHandler import encode
        self._generation_count = arg

        if self.GA.best_individual is None:
            best_true_clauses = ''
        else:
            best_true_clauses = self.GA.true_clauses(self.GA.best_individual)

        if self.GA.current_child is None:
            new_true_clauses = ''
        else:
            new_true_clauses = self.GA.true_clauses(self.GA.current_child)

        encoded_message = encode("PROGRESS", [[self._generation_count, self.GA.max_generations],
                                              [self.time_started],
                                              [self.GA.best_individual_fitness],
                                              [str(self.GA.best_individual)],
                                              [self.GA.current_child_fitness],
                                              [str(self.GA.current_child)],
                                              [self.GA.numberOfVariables],
                                              [self.GA.numberOfClauses],
                                              [best_true_clauses],
                                              [new_true_clauses]]
                                 )
        if self.server_thread is not None:
            self.server_thread.push_to_all(encoded_message)
        time_elapsed = int(time.time()*1000)-self.time_started
        if time_elapsed >= 1000:
            time_elapsed = str(time_elapsed/1000) + 's'
        else:
            time_elapsed = str(time_elapsed) + 'ms'
        print("Generations: " + str(self._generation_count) + "/" + str(self.GA.max_generations) + "\t|\tElapsed Time: "
              + time_elapsed + "\t|\tBest Individual's Fitness: "
              + str(self.GA.best_individual_fitness))

    def send_update(self, msg):
        self.server_thread.push_to_all(msg)

    def has_ga_instance(self):
        return self.GA is not None

    def create_ga(self, ga_parameters):

        new_params = {key: ga_parameters[key] for key in ga_parameters.keys() if ga_parameters[key] is not None}
        self.GA = GA(**new_params)
        self.GA.attach(self)

    def start_ga(self):
        try:
            self.time_started = int(time.time()*1000)
            result = self.GA.gasat()
            self.time_finished = int(time.time()*1000)
            time_elapsed = self.time_finished - self.time_started
            if time_elapsed >= 1000:
                time_elapsed = str(time_elapsed / 1000) + 's'
            else:
                time_elapsed = str(time_elapsed) + 'ms'
            if result.fitness == 0:
                print(BColors.OKGREEN + "Successfully found a solution in " +
                      time_elapsed + BColors.ENDC)
                print('A solution is: ' + str(result))
            else:
                print(BColors.FAIL + "Could not find a solution in the given amount of generations." + BColors.ENDC)
                print('The best solution found is: ' + str(result))
            if self.server_thread is not None:
                from SATSolver.RequestHandler import encode
                encoded_message = encode("FINISHED", [
                    result.fitness == 0,
                    result.fitness,
                    [self._generation_count, self.GA.max_generations],
                    self.time_started,
                    self.time_finished,
                    str(result),
                    self.GA.true_clauses(result)
                ])
                time.sleep(0.1)
                self.server_thread.push_to_all(encoded_message)

                self.GA = None

        except GAStop:
            self.time_finished = int(time.time() * 1000)
            time_elapsed = self.time_finished - self.time_started
            if time_elapsed >= 1000:
                time_elapsed = str(time_elapsed / 1000) + 's'
            else:
                time_elapsed = str(time_elapsed) + 'ms'

            if self.GA.best_individual is None:
                print(BColors.FAIL + "Could not find a solution, solving stopped by client." + BColors.ENDC)
                if self.server_thread is not None:
                    from SATSolver.RequestHandler import encode
                    encoded_message = encode("FINISHED", [
                        False,
                        None,
                        [0, 0],
                        self.time_started,
                        self.time_finished,
                        '',
                        ''
                    ])
                    self.server_thread.push_to_all(encoded_message)
                self.GA = None
                return

            result = self.GA.best_individual
            if result.fitness == 0:
                print(BColors.OKGREEN + "Successfully found a solution in " +
                      time_elapsed + BColors.ENDC)
                print('A solution is: ' + str(result))
            else:
                print(BColors.FAIL + "Could not find a solution, solving stopped by client." + BColors.ENDC)
                print('The best solution found is: ' + str(result))
            if self.server_thread is not None:
                from SATSolver.RequestHandler import encode
                encoded_message = encode("FINISHED", [
                    result.fitness == 0,
                    result.fitness,
                    [self._generation_count, self.GA.max_generations],
                    self.time_started,
                    self.time_finished,
                    str(self.GA.best_individual),
                    self.GA.true_clauses(self.GA.best_individual)
                ])
                self.server_thread.push_to_all(encoded_message)

                self.GA = None

    def parse_formula(self, raw_formula, local=True):
        """
        Takes a list of lines read from the input file and
        """
        # Read all the lines from the file that aren't comments
        if local:
            lines = [line.replace("\n", "") for line in raw_formula if line[0] != "c" and line.strip() != ""]
            number_of_variables, number_of_clauses = int(lines[0].split()[2]), int(lines[0].split()[3])
        else:
            number_of_variables, number_of_clauses = int(raw_formula[0].split()[2]), int(raw_formula[0].split()[3])
            lines = raw_formula
        formula = []

        # Go through the lines and create numberOfClauses clauses
        line = 1
        # for line in range(1, len(lines)):
        try:
            while line < len(lines):
                clause = []
                # We need a while loop as a clause may be split over many lines, but eventually ends with a 0
                end_of_clause = False
                while line < len(lines) and not end_of_clause:
                    # Split the line and append a list of all integers, excluding 0, to clause
                    clause.append([int(variable.strip()) for variable in lines[line].split()
                                   if int(variable.strip()) != 0])
                    # If this line ended with a 0, we reached the end of the clause
                    if int(lines[line].split()[-1].strip()) == 0:
                        end_of_clause = True
                        line += 1
                    # Otherwise continue reading this clause from the next line
                    else:
                        line += 1
                # clause is now a list of lists, so we need to flatten it and convert it to a list
                formula.append(tuple([item for sublist in clause for item in sublist]))
        except Exception as e:
            raise Exception(str(line) + ' ' + str(e))
        return formula, number_of_variables, number_of_clauses
