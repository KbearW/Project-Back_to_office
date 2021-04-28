"""An interactive, REPL-style quizzer for SQL problems."""

# Author: Joel Burton <joel@hackbrightacademy.com>, based on earlier work by
# Christian Fernandez.

from __future__ import print_function

import os
import pickle

import datetime

import psycopg2
import hashlib
import logging
import readline

log = logging.getLogger(__name__)

MAX_ROWS = 20
PROBLEM_FILE_PATH = "problem_set.pickle"
INTRO = """

Hackbright Academy - SQL Skills
----------------------------------------------

You will write a series of SQL queries accomplishing different tasks.

Type '\\help' without quotes for a list of the available commands.

It may be helpful to refer to the list of tables, found by typing in '\\dt,'
or view the schema of a given table, (ex: '\\d orders') while formulating
your queries. If you get very stuck each problem includes a hint on how to
formulate your query, accessed by typing '\\hint.'

To skip a question, type '\\next.'

DON'T FORGET TO END SQL STATEMENTS WITH A SEMICOLON!

"""

HELP = """
The following commands are available:

    \\help    - Display this message
    \\hint    - Show a hint about how to formulate the query
    \\next    - Skip the current problem
    \\problem - Show the current problem statement
    \\quit    - Quit the program
    \\dt      - List the tables
    \\d <tbl> - Show the schema used to create named table

Any other commands will be interpreted as a SQL query and executed against the
problem set database."""

# SQL to get a list of all tables for \dt command
SQL_ALL_TABLES = """
SELECT
  n.nspname as "Schema",
  c.relname as "Name",
  CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' END as "Type",
  pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
FROM pg_catalog.pg_class c
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','v','m','S','f','')
      AND n.nspname <> 'pg_catalog'
      AND n.nspname <> 'information_schema'
      AND n.nspname !~ '^pg_toast'
  AND pg_catalog.pg_table_is_visible(c.oid)
ORDER BY 1,2;
"""

# SQL to find a table oid, used for \d <tbl>
SQL_FIND_TABLE = """
SELECT c.oid
FROM pg_catalog.pg_class c
WHERE c.relname ~ '^({})$'
  AND pg_catalog.pg_table_is_visible(c.oid)
"""

# SQL to get detail on a table, used for \d <tbl>
SQL_DESCRIBE_TABLE = """
SELECT a.attname AS "Column",
  pg_catalog.format_type(a.atttypid, a.atttypmod) as "Type",
  CASE WHEN a.attnotnull THEN 'not null' ELSE '' END AS "Modifiers"
FROM pg_catalog.pg_attribute a
WHERE a.attrelid = '{}' AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY a.attnum;
"""

# What's the minimum length a col should show given it's PG type?
COL_TYPE_TO_LEN = {
    23: 5,  # int
    1043: 2,  # string
    1700: 8,  # numeric
    1082: 10,  # date
    16: 5,  # boolean
    25: 2,  # text
    705: 2,  # text
    1042: 2,  # char
}


class Problem(object):
    """SQL Problem."""

    def __init__(self, num, instruction, task, hint, solution):
        self.num = num
        self.instruction = instruction
        self.task = task
        self.hint = hint
        self.solution = solution
        self.solution_hash = None

    def check_solution(self, result):
        """Check if result (as string table) matches hashed solution."""

        digest = hashlib.md5(str(result).encode('utf-8')).hexdigest()
        return self.solution_hash == digest

    @staticmethod
    def hash_solution(result):
        """Return hash of solution to store."""

        return hashlib.md5(str(result)).hexdigest()


class StudentAnswer(object):
    """Correct answer from student."""

    PARTS_SPLIT = "\n\n-----\n\n"

    def __init__(self, num, task, solution):
        self.num = num
        self.task = task
        self.solution = solution

    @classmethod
    def from_string(cls, s):
        """Create student answer from string."""

        num, task, solution = s.split(cls.PARTS_SPLIT)
        return StudentAnswer(num=int(num), task=task, solution=solution)

    def to_string(self):
        """Marshall student answer as string."""

        return self.PARTS_SPLIT.join([str(self.num), self.task, self.solution])


class StudentProgress(dict):
    """Track student progress and handle reading/writing answer file.

    Is a dictionary of answers given by students, along with methods for
    reading and writing out to disk.
    """

    ANSWER_FILE_PATH = 'answers.sql'
    PROBLEM_SPLIT = "\n\n\n==========\n"

    def __init__(self):
        super(StudentProgress, self).__init__(self)
        self.read_answers()

    def read_answers(self):
        """Read student answers from file."""

        if not os.path.isfile(self.ANSWER_FILE_PATH):
            return

        with open(self.ANSWER_FILE_PATH, 'r') as f:
            for problem in f.read().split(self.PROBLEM_SPLIT):
                if not problem:
                    continue
                answer = StudentAnswer.from_string(problem)
                self[answer.num] = answer

        log.info("Read {} answers".format(len(self)))

    def save_answers(self):
        """Save student answers to a file."""

        with open(self.ANSWER_FILE_PATH, 'w') as f:
            f.write(self.PROBLEM_SPLIT.join(
                    v.to_string() for k, v in sorted(self.items())))

        log.info("Saved {} answers".format(len(self)))

    def mark_solved(self, num, task, solution):
        """Note that a problem has been solved and save it."""

        self[num] = StudentAnswer(num, task, solution)
        self.save_answers()


class Database(object):
    """Database proxy.

    Handles connecting, executing functions, and DB utilities.
    """

    def __init__(self):
        self.cursor, self.conn = self.connect()

    @staticmethod
    def connect():
        """Connect to DB and return cursor."""

        conn = psycopg2.connect("dbname=cars")
        conn.autocommit = True
        cursor = conn.cursor()
        return (cursor, conn)

    @staticmethod
    def result_to_str(description, results):
        """Return formatted results like psql

        Args:
            description (list): List of column metadata
            results (list): Result tuples

        Returns:
            string: Result text
        """

        results = list(results)

        if not results:
            return ""

        # Make dictionary of column-name, length-of-column
        cols = []
        for col in description:
            cols.append({'name': col.name,
                         'len': max(len(col.name), COL_TYPE_TO_LEN.get(col.type_code, 10))})

        # Figure out the maximum length of the data in a column
        for row in results[:MAX_ROWS]:
            for i, col in enumerate(row):
                if isinstance(col, str):
                    cols[i]['len'] = max(cols[i]['len'], len(col))

        out = "\n"

        # Print column names
        for i, col in enumerate(cols):
            out += " " + ("{:^" + str(col['len']) + "}").format(col['name']) + " "
            if i == len(cols) - 1:
                out += "\n"
            else:
                out += "|"

        # Print border below column names
        for i, col in enumerate(cols):
            out += "-" * (col['len'] + 2)
            if i == len(cols) - 1:
                out += "\n"
            else:
                out += "+"

        # Print rows of cols
        for row in results[:MAX_ROWS]:
            for i, col in enumerate(row):
                if col is None:
                    col = ""
                if col is True:
                    col = "True"
                if col is False:
                    col = "False"
                if isinstance(col, datetime.date):
                    col = col.strftime("%Y-%m-%d")

                out += " " + ("{:" + str(cols[i]['len']) + "}").format(col) + " "
                if i == len(cols) - 1:
                    out += "\n"
                else:
                    out += "|"

        # Print count of rows
        if len(results) <= MAX_ROWS:
            out += "({} rows)".format(len(results))
        else:
            out += "({} rows, truncated for display at {})".format(len(results), MAX_ROWS)

        return out

    def get_raw_result(self, attempt, error_on_empty=False):
        """Execute SQL and return results.

        Args:
            attempt (str): SQL
            error_on_empty (bool): do we raise error (Else print msg) for errors/empty?

        Returns:
            list: description metadata list
            list: tuples of results
        """

        try:
            self.cursor.execute(attempt)
            results = self.cursor.fetchall()

        except psycopg2.DatabaseError as e:
            err = "There was a problem with your SQL syntax:\n\n\t{}\n".format(e)
            if error_on_empty:
                raise ValueError(err)
            else:
                print(err)
                return [], []

        if results:
            return self.cursor.description, results

        else:
            err = "(your syntax was legal but your query returned no results)"
            if error_on_empty:
                raise ValueError(err)
            else:
                print(err)
                return [], []

    def show_tables(self):
        """Show tables."""

        self.cursor.execute(SQL_ALL_TABLES)
        results = self.cursor.fetchall()
        print(self.result_to_str(self.cursor.description, results))

    def show_schema(self, tokens):
        """Show schema for given table."""

        if len(tokens) < 2:
            return self.show_tables()

        table_name = tokens[1]
        self.cursor.execute(SQL_FIND_TABLE.format(table_name))
        results = self.cursor.fetchall()

        if not results:
            print("No such table:", table_name)
            return

        oid = results[0][0]
        self.cursor.execute(SQL_DESCRIBE_TABLE.format(oid))
        results = self.cursor.fetchall()

        output = self.result_to_str(self.cursor.description, results)

        if not output:
            print("No such table:", table_name)
        else:
            print(output)


class SQLQuiz(object):
    """Quiz application object.

    Handles state of play and is controller for application.
    """

    def __init__(self):
        self.db = Database()
        self.problems = self.read_problems()
        self.progress = StudentProgress()
        self.current_problem = None

    @staticmethod
    def read_problems():
        """Read problems off disk."""

        with open(PROBLEM_FILE_PATH, 'rb') as f:
            return pickle.load(f)

    def play(self):
        """Play quiz."""

        if len(self.progress) == len(self.problems):
            return self.exit("You've already answered all the questions." +
                             "Remove answers.sql to redo the exercise.")

        print(INTRO)
        input("Press RETURN to start> ")
        print()

        self.current_problem = self.problems[0]

        while True:
            if self.current_problem.num in self.progress:
                print("Already answered question", self.current_problem.num)

            else:
                self.show_problem()
                if not self.get_solution():
                    # True is problem skipped/solved
                    # False is request to quit program.
                    self.exit("\nQuitting.")

            if self.current_problem != self.problems[-1]:
                # There are more problems, so go to the next one
                # (this doesn't look like we're advancing, but the problem num is
                # 1-based, whereas in the list, it's zero based, so
                # going to self.problems[6] is our problem numbered 7.)
                self.current_problem = self.problems[self.current_problem.num]

            else:
                print("\n\nEND OF QUIZ REACHED.")
                self.exit("Exiting")
                break

    def exit(self, msg):
        """Hard exit with message."""
        self.db.cursor.close()
        self.db.conn.close()
        print(msg, "\nGoodbye.\n")
        return

    def show_problem(self):
        """Show problem description and task."""

        print("\nProblem {0:.2f} (of {0:2.0f})".format(self.current_problem.num,
                                              len(self.problems)))
        print("------------------\n")
        if self.current_problem.instruction:
            print(self.current_problem.instruction)
            print()
        print("Task:", self.current_problem.task)

    def get_solution(self):
        """Get input from user until they quit or are correct."""

        problem = self.current_problem

        # This accumulates the SQL command they are making
        sql = ""

        while True:
            try:
                if not sql:
                    print()
                    line = input("SQL [{}]> ".format(problem.num))
                else:
                    line = input("... [{}]> ".format(problem.num))
            except EOFError:
                return False

            if not line:
                continue

            tokens = line.split()
            command = tokens[0]

            if command in ["\\q", "\\quit"]:
                return False

            elif command in ["\\problem"]:
                self.show_problem()
                sql = ""

            elif command in ["\\hint"]:
                print(problem.hint)
                sql = ""

            elif command in ["\\dt"]:
                self.db.show_tables()
                sql = ""

            elif command in ["\\d"]:
                self.db.show_schema(tokens)
                sql = ""

            elif command in ["\\help", "\\h", "\\?"]:
                print(HELP)
                sql = ""

            elif command in ["\\next", "\\skip"]:
                print("\nSKIPPING PROBLEM {}".format(problem.num))
                return True

            elif command in ["\\goto", "\\jumpto"]:
                num = int(tokens[1])
                # undocumented commands jumps to that numbered problem
                print("Jumping to {}".format(num))
                # -2 to compensate for:
                #     1 gets added for "successful answering this question"
                #     we number problems from 1, but the python list starts at 0
                self.current_problem = self.problems[num - 2]
                return True

            else:
                sql = sql + "\n" + line
                if sql.strip().endswith(";"):
                    description, result = self.db.get_raw_result(sql)
                    if result:
                        print(self.db.result_to_str(description, result))
                        if problem.check_solution(result) is True:
                            print("\n\tCorrect!")
                            print(sql)
                            print("\n\tMoving on...\n")
                            self.progress.mark_solved(problem.num, problem.task, sql)
                            return True
                        else:
                            print("\n(results do not match answer)\n")
                    sql = ""


def write_pickle():
    """Write out problems file.

    This is only used by instructors, and requires you have the Python module
    called problems.
    """

    from meta.problems import PROBLEMS
    db = Database()

    problems = []
    for i, p in enumerate(PROBLEMS):
        problem = Problem(num=i + 1, **p)
        description, result = db.get_raw_result(problem.solution, error_on_empty=True)
        problem.solution_hash = problem.hash_solution(result)
        problem.solution = None
        problems.append(problem)

    with open(PROBLEM_FILE_PATH, 'w') as f:
        pickle.dump(problems, f)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2 and sys.argv[1] == "--rebuild":
        # If they passed in --rebuild, we'll make the problems file from the text
        write_pickle()
    else:
        quiz = SQLQuiz()
        quiz.play()
