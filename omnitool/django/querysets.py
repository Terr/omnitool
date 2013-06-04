"""Helper functions for working with Django QuerySets."""
import re

from ..console.tables import pprint_table

from django.db import connections
from django.db.models.query import QuerySet


def explain(queryset):
    """Executes explain query for queryset and prints the result.

    Inspired by: guidoism @ http://stackoverflow.com/a/11478262/390441
    """
    cursor = connections[queryset.db].cursor()
    cursor.execute('EXPLAIN %s' % quote_dates(str(queryset.query)))
    r = cursor.fetchall()
    r = map(list, r)

    # Make all strings non-empty to avoid errors in texttable/textwrap
    for x in xrange(len(r)):
        for y in xrange(len(r[x])):
            if r[x][y] == '':
                r[x][y] = ' '

    return pprint_table(r)


def quote_dates(text):
    """Quotes date strings (YYYY-MM-DD HH:MM:SS) in, for example, queries produced by Django
    QuerySets.
    """
    return re.sub('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', '"\\1"', text)

