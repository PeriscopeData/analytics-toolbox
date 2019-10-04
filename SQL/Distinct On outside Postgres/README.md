# Implementing SELECT DISTINCT ON in other SQL Dialects

Ever seen the following error when materializing a view?

`SELECT DISTINCT ON is not supported`

The [DISTINCT ON](https://www.postgresql.org/docs/9.5/sql-select.html#SQL-DISTINCT) clause is a Postgres function which selects the first value for a group given the order by clause. With no `order by` clause, it gives a random value! 

So how can we do this in Redshift or Snowflake? Window functions!



- [Redshift First_Value](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_first_value.html)

- [Snowflake First_Value](https://docs.snowflake.net/manuals/sql-reference/functions/first_value.html)

Equivalent examples in Postgres, Redshift, and Snowflake are included