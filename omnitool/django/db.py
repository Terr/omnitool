"""Helper functions for working with database connections within Django."""
from django.db import connection, transaction

from ..console.tables import pprint_table

def dictfetchall(cursor):
    """Returns all rows from a cursor as a dict.

    Taken from Django documentation (https://docs.djangoproject.com/en/dev/topics/db/sql/#transactions-and-raw-sql)
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def profile_mysql_queries(func):
    """Decorator which profiles MySQL queries via MySQL's internal profiling
    tool.

    The decorator initiates the profiling, stops it after the function and
    prints out the result in a table to the console.

    If the `verbosity` option (function or management command
    argument) is 2 or higher, then extensive details are shown for each query.
    """

    def wrap(*args, **kwargs):
        verbose = int(kwargs.get('verbosity', 0))
        cursor = connection.cursor()
        cursor.execute('SET profiling = 1')

        func(*args, **kwargs)

        cursor.execute('SET profiling = 0')
        cursor.execute('SHOW PROFILES')
        if verbose >= 2:
            rows = dictfetchall(cursor)
            for row in rows:
                cursor.execute('SHOW PROFILE CPU FOR QUERY %s', [row['Query_ID']])
                query_rows = cursor.fetchall()
                # Add column headers
                query_rows = list(query_rows)
                query_rows.insert(0, [x[0] for x in cursor.description])

                print row['Query']
                pprint_table(query_rows)
        else:
            rows = cursor.fetchall()
            pprint_table(rows)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap




