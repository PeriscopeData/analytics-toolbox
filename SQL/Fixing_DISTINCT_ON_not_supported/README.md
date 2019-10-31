# Implementing SELECT DISTINCT ON in other SQL Dialects

Ever seen the following error when materializing a view?

    SELECT DISTINCT ON is not supported

The [DISTINCT ON](https://www.postgresql.org/docs/9.5/sql-select.html#SQL-DISTINCT) clause is a Postgres function which selects the first value for a group given the order by clause. With no order by clause, it gives a random value! 

So how can we do this in Redshift or Snowflake? *Window functions!*

Redshift: https://docs.aws.amazon.com/redshift/latest/dg/r_WF_first_value.html

Snowflake: https://docs.snowflake.net/manuals/sql-reference/functions/first_value.html

Here are some equivalent examples in Postgres, Redshift, and Snowflake:

#### Postgres

    with dataset as (
    select 'bart' as name, 'first bart' as text_value, 1 as ordering
      union all select 'homer', 'second homer', 2
      union all select 'bart', 'second bart', 2
      union all select 'homer', 'first homer', 1
    )
    select distinct on (name)
        name
        , text_value
      from
        dataset
      order by
        name
        , ordering
        
#### Snowflake

    with dataset as (
    select 'bart' as name, 'first bart' as text_value, 1 as ordering
      union all select 'homer', 'second homer', 2
      union all select 'bart', 'second bart', 2
      union all select 'homer', 'first homer', 1
    )
    select distinct
        name
        , first_value(text_value) over (partition by name order by ordering) as text_value
      from
        dataset

#### Redshift

    with dataset as (
    select 'bart' as name, 'first bart' as text_value, 1 as ordering
      union all select 'homer', 'second homer', 2
      union all select 'bart', 'second bart', 2
      union all select 'homer', 'first homer', 1
    )
    select distinct
      name
      , first_value(text_value) over(partition by name order by ordering rows between unbounded preceding and unbounded following) as text_value
    from
      dataset



   