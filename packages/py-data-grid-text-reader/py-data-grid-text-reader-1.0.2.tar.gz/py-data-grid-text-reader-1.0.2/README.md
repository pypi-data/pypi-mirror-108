# Data Grid Text Reader

``py-data-grid-text-reader`` is a library that reads a string representing a
database record set (that resembles the output of a call to the Apache Spark
DataFrame.show() command) and converts it to a different representation, such
as a list of dictionaries or a set of SQL CREATE TABLE and INSERT statements
that can be used to persist the data to a database.

This library is based on the `py-dataframe-show-reader` library
(see https://github.com/internetsystemsgroup/py-dataframe-show-reader/) and
reuses much code from that project. It is intended that this library can read
and parse the same data record set strings that the `py-dataframe-show-reader`
library can.

The primary intended use of the functions in this library is to be used to
enable writing more concise and easy-to-read tests of data transformations than
would otherwise be possible.

Imagine we are working on a database query, function or stored procedure that
performs a data transformation that is complex enough that we would like to
quickly verify that it performs as intended, and also have tests to help ensure
that a developer modifying the query in the future does not inadvertently break
the query for an overlooked edge case.

```sql
SELECT  CAST(STRFTIME('%W', sale_date) AS INT) + 1 AS week_of_year,
        AVG(units_sold) AS avg_units_sold,
        SUM(gross_sales) AS gross_sales
FROM    sales_by_day
GROUP BY 1
ORDER BY 1
```

This is not a complex query, but perhaps we would like to verify that:

1. Dates are in fact grouped into different weeks.
1. Units sold are truly averaged and not summed.
1. Gross sales are truly summed and not averaged.

A unit testing purist might argue that each of these assertions should be
covered by a separate test method, but there are at least two reasons why one
might choose not to do that.

1. Practical experience tells us that detectable overhead is incurred for
each separate database transformation test, so we may want to limit the number
of separate tests in order to keep our full test suite running in a
reasonable duration.

1. When working with data sets in SQL, particularly when
using aggregate, grouping and window functions,
interactions between different rows can be easy to overlook. Tweaking a
query to fix an aggregate function like a summation might inadvertently break
the intended behavior of a windowing function in the query.
A change to the query might allow a summation-only unit test to pass while
leaving broken window function behavior undetected because we have neglected to
update the window-function-only unit test.  

If we accept that we'd like to use a single test to verify the three
requirements of our query, we need three rows in our input data set.

Using unadorned pytest, our test might look like this:

```python
def test_without_data_grid_text_reader():
    with create_engine('sqlite://').connect() as connection:
        connection.execute("""
        CREATE TABLE sales_by_day (
            sale_date DATE,
            units_sold INT,
            gross_sales DOUBLE
        );""")

        connection.execute("""
        INSERT INTO sales_by_day
        (sale_date, units_sold, gross_sales) VALUES
        ('2019-01-01', 10, 100),
        ('2019-01-02', 20, 200),
        ('2019-01-08', 80, 800);""")

        actual_rows = [dict(row) for row in connection.execute("""
        SELECT  CAST(STRFTIME('%W', sale_date) AS INT) + 1 AS week_of_year,
                AVG(units_sold) AS avg_units_sold,
                SUM(gross_sales) AS gross_sales
        FROM    sales_by_day
        GROUP BY 1
        ORDER BY 1
        """)]

        assert 2 == len(actual_rows)  # Number of rows
        assert 3 == len(actual_rows[0])  # Number of columns
        assert 1 == actual_rows[0]['week_of_year']
        assert 15 == actual_rows[0]['avg_units_sold']
        assert 300 == actual_rows[0]['gross_sales']
        assert 2 == actual_rows[1]['week_of_year']
        assert 80 == actual_rows[1]['avg_units_sold']
        assert 800 == actual_rows[1]['gross_sales']
```

Using the Data Grid Text Reader, our test could instead look like this:

```python
def test_using_data_grid_text_reader():
    with create_engine('sqlite://').connect() as connection:
        reader = DataGridTextReader()
        reader.save_as_table('sales_by_day', """
        +----------+----------+-----------+
        |sale_date |units_sold|gross_sales|
        [date      |int       |double     |
        +----------+----------+-----------+
        |2019-01-01|10        |100        |
        |2019-01-02|20        |200        |
        |2019-01-08|80        |800        |
        +----------+----------+-----------+
        """, connection)

        actual_rows = [dict(row) for row in connection.execute("""
        SELECT  CAST(STRFTIME('%W', sale_date) AS INT) + 1 AS week_of_year,
                AVG(units_sold) AS avg_units_sold,
                SUM(gross_sales) AS gross_sales
        FROM    sales_by_day
        GROUP BY 1
        ORDER BY 1
        """)]

        expected_rows = reader.data_grid_text_to_list("""
        +------------+--------------+-----------+
        |week_of_year|avg_units_sold|gross_sales|
        [int         |int           |double     |
        +------------+--------------+-----------+
        |1           |15            |300        |
        |2           |80            |800        |
        +------------+--------------+-----------+
        """)
        assert_equal(expected_rows, actual_rows)
```

In the second test example, the `save_as_table` function accepts some data grid
text and persists it to a table called `sales_by_day`. Then the
`data_grid_text_to_list` function accepts some different data grid text and
creates a list of dict that can be compared to the `actual_rows` value
returned by executing the data transformation query.

In the first version, the setup portion of the test contains twelve lines,
and it may take a few moments to digest the contents of the input rows.
In the second version, the setup portion contains eleven lines and displays the
input data in a more concise tabular form that may be easier for other
programmers (and our future selves) to digest when we need to maintain this
code down the road.

If the method under test was more complicated and required more rows and/or
columns in order to adequately test, the length of the first test format would
grow much more quickly than that of the test using the DataFrame Show Reader.

The `data_grid_text_to_list` function gives us a convenient way to create an
`expected_rows` list to pass to the `assert_equal` function (to check
list equality) that is included in the package.

## Running the Tests

1. Clone the git repo.
1. `cd` into the root level of the repo.
1. At a terminal command line, run `python3 -m venv venv`
1. Run `source venv/bin/activate`
1. Run `pip install -r requirements_dev.txt`
1. Run `pytest`
1. When finished with your session, deactivate your virtual environment with
   `deactivate`.
 
## How to Build the Python Package for Distribution on PyPI

`python setup.py sdist bdist_wheel`

## How to Publish the Package to PyPI

Publish to the PyPI test site:

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

Confirm that the test is successfully uploaded:

1. View the package at https://test.pypi.org/project/py-data-grid-text-reader/
2. Try installing the project like so:
   `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple py-data-grid-text-reader`

After confirming that the package has successfully been published to test.pypi,
publish to the official PyPI:

`twine upload dist/*`

Confirm that the distribution package is successfully uploaded:

1. View the package at https://pypi.org/project/py-data-grid-text-reader/
2. Install the project like so:
   `pip install py-data-grid-text-reader`

## Installation

To install the package for use in your own package, run:

`pip install py-data-grid-text-reader`

## Who Maintains Data Grid Text Reader?

Data Grid Text Reader is the work of the community. The core committers and
maintainers are responsible for reviewing and merging PRs, as well as steering
conversation around new feature requests. If you would like to become a
maintainer, please contact us.
