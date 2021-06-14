"""
    Module to validate the game
    Instantiates with
        - N : Integer, size of the board (NxN)
        - constraints : List of nested tuples containing Integers
        - solution : Board represented as nested list
        - loglevel : optional. INFO is default
    Special considerations/assumptions:
        - constraints are expected to be given in greater then order
         : example (a>b is given if b<a is represented in the board)
"""
import logging

class Puzzle:
    """
        Contains constructors for validating the puzzle
    """
    def __init__(self, N, constraints, solution, loglevel='INFO') -> None:
        """

        """
        # logging
        logging.basicConfig(filename="puzzle_logging.txt", filemode='a',
                            format='%(levelname)s: %(asctime)s: %(message)s',
                            level=loglevel)
        logging.info("** Loglevel set to {}".format(loglevel))
        # values
        self.n_value = N
        self.constraints = constraints
        self.solution = solution
        # columns store
        self.columns_store = {}
        # method to store input validation flag and populate columns store
        self.input_validation = self.__validate_inputs__()
        # validation values
        self._valid_expected_sum = self._expected_sum__(isrange=True)

    def __check_tuple__(self, tuple_value):
        """
            Method to check and return if the incoming value is of type Tuple
        """
        if not isinstance(tuple_value, tuple):
            return False

    def __validate_inputs__(self)-> bool:
        """
            Validates data structure of the inputs given
            1) value of N should be >=1
            2) Neither solution nor constraint should be None or empty
            3) constraints are expected to be in a list of nested tuples [((a,b), (c,d))]

            returns boolean
        """
        # check for valid n value
        if self.n_value is None:
            logging.error("Value for N cannot be None")
            return False
        # check for positive n value
        if  self.n_value <= 0:
            logging.error("Value for N is expected to be 1 or higher")
            return False
        # check type for solution
        if self.solution is None or self.constraints is None:
            logging.error("None is not a valid input. solution:{}, constraints:{}".format(self.solution, self.constraints))
            return False
        # check for empty
        if not self.solution or not self.constraints:
            logging.error("empty data structures found. solution:{}, constraints:{}".format(self.solution, self.constraints))
            return False
        # check constraints type
        if isinstance(self.constraints, list):
            logging.debug("Constraints validation : List found as expected")
            for tuplevalue in self.constraints:
                if isinstance(tuplevalue, tuple):
                        if False in set(map(self.__check_tuple__, tuplevalue)):
                            logging.error("Invalid constraint found {}".format(tuplevalue))
                            return False
                else:
                    logging.exception("expected nested tuples of length 2 and found {}".format(type(tuplevalue)))
                    return False
        else:
            logging.exception("list of tuples expected, found {}".format(type(self.constraints)))
            return False
        # block to prepare columns for validation
        for row in self.solution:
            column_count = 1
            for j in row:
                self.columns_store.setdefault(column_count, []).append(j)
                column_count = column_count+1
        return True

    def _expected_sum__(self, iter_input=None, isrange=True)->int:
        """
            Calculate sum from 1 to N
            returns = cumulative sum from 1 to N
        """
        cumsum = 0
        try:
            if isrange:
                for i in range(1, self.n_value+1):
                    cumsum = cumsum+i
            else:
                for i in iter_input:
                    cumsum = cumsum+i
        except:
            (logging.error("Error calculating expected sum."
                "check values for self.n_value:{}, iter_input={}, isrange={}".format(self.n_value, iter_input, isrange)))
            return False
        return cumsum

    def _adjust_index(self, index_value: int)->int:
        """
            returns index_value-1
        """
        try:
            return index_value-1
        except:
            logging.exception("Expects Integer, found {}".format(type(index_value)))
            return False

    def sudoku_validation(self):
        """
            Initial validation before constraints are validated
            validation 1 = sum of rows equals expected sum
            validation 2 = sum of columns equals expected sum
        """
        # Block to validate rows
        for row in enumerate(self.solution):
            if self._expected_sum__(iter_input=row[1], isrange=False) == self._valid_expected_sum:
                logging.info("Row validation for {} passed".format(row[0]+1))
            else:
                return False
        # Block to validate columns
        for column_number, column_list in self.columns_store.items():
            if self._expected_sum__(iter_input=column_list, isrange=False) == self._valid_expected_sum:
                logging.info("Column validation for {} passed".format(column_number))
            else:
                return False
        return self._constraint_validation()

    def _constraint_validation(self):
        """
            derive constraint tuples as x,y points with suffix.
            assumption for the validation - x1,y1 > x2y2
        """
        for constraint in enumerate(self.constraints):
            first_constraint, second_constraint = constraint[1]
            logging.debug(constraint)
            x1, y1 = map(self._adjust_index, first_constraint)
            x2, y2 = map(self._adjust_index, second_constraint)
            logging.debug("validation for constraints {}".format(constraint[0]))
            logging.debug(constraint)
            logging.debug("Adjusted constraints")
            logging.debug((x1, y1, x2, y2))
            if self.solution[x1][y1] > self.solution[x2][y2]:
                logging.info("Constraint {} passed".format(constraint[0]+1))
                logging.debug("Constraint passed for {}".format(constraint))
            else:
                return False
        return True

    def validate(self)-> bool:
        """
            Method to be called to validate the puzzle
            - Invokes Sudoku Validation method if input validation is successful

            returns boolean
        """
        if self.input_validation:
            result = self.sudoku_validation()
        else:
            return False
        return result

if __name__ == "__main__":

    solution = [[2, 1, 4, 3], [1, 4, 3, 2], [3,2,1,4], [4,3,2,1]]
    constraints = [((1,1),(1,2)), ((2,3),(3,3)), ((4,2), (3,2)), ((4,1),(4,2))]
    N = 4
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is True

    solution = [[1,2], [1,2]]
    constraints = [(1,2),(1,2)]
    N = 2
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is False

    solution = [[1,2], [1,2]]
    constraints = [(1,2,1,2)]
    N = 2
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is False

    solution = []
    constraints = []
    N = 1
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is False

    solution = None
    constraints = None
    N = 1
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is False

    solution = [[9,3,5,1,8,6,7,2,4],[2,1,3,4,7,5,9,8,6],[8,4,9,6,5,2,3,7,1],
            [5,7,1,8,9,3,4,6,2],[4,2,7,5,6,9,1,3,8],[7,6,8,9,2,1,5,4,3],
            [3,9,2,7,4,8,6,1,5],[6,8,4,3,1,7,2,5,9],[1,5,6,2,3,4,8,9,7]]
    constraints = [((1,1),(1,2)),((1,7),(1,6)),((2,1),(2,2)),
                ((2,4),(2,3)), ((1,5),(2,5)), ((1,6), (2,6)),((2,7),(2,6)),
                ((2,9),(1,9)),((2,5),(3,5)),((2,8),(3,8)),((3,3),(3,4)),
                ((3,4),(3,5)),((3,7),(3,6)), ((2,8),(3,8)),((4,5),(3,5)),((4,7),(3,7)),((3,8),(4,8)),((4,9),(3,9)),
                ((4,1), (5,1)), ((4,4),(5,4)), ((4,5),(5,5)), ((4,7),(4,6)), ((4,8),(4,7)), ((4,8), (4,9)),
                ((6,3),(5,3)), ((5,5),(6,5)), ((6,8),(5,8)),((6,1),(7,1)), ((6,4),(7,4)), ((6,5), (6,6)), ((6,7),(6,8)),
                ((6,8),(6,9)),((7,2),(8,2)), ((7,5), (8,5)),((7,6),(8,6)), ((7,7),(7,8)),
                ((8,8),(7,8)), ((8,3),(8,4)), ((8,9),(8,8)),((9,3),(9,2)), ((9,5),(9,4)), ((9,7),(8,7))]
    N = 9
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is True

    solution = [None]
    constraints = [None]
    N = 1
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is False

    solution = [None]
    constraints = [None]
    N = None
    puzzle_test = Puzzle(N, constraints, solution, 'DEBUG')
    assert puzzle_test.validate() is False