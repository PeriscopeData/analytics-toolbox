## SQL Order of Operations

The first thing you' learn in SQL is the order in which we write various clauses in our queries (SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, then LIMIT). However, the order in which the database interprets the query is slightly different. Understanding this order will allow you to better understand how to construct more complex queries as well as optimize your queries for speed and performance. 
 

1. FROM

The first part of the query the database will read is the FROM clause. These are the table(s) we are pulling data from. Any joins that are done are executed first by the query planner.  Joining on many rows can often be costly. As a strategy for optimization we can filter down the rows before joining the tables. Because the FROM clause comes before the WHERE clause we will want to filter the results with a CTE before joining them in our final query.  This might look like,

    with
      american_companies as (
        select
          *
        from
          company
        where
          country = 'USA'
      )
      , current_users as (
        select
          *
        from
          users
        where
          deleted_at is null
      )
    select
      *
    from
      t1
      join t2 on
        american_companies.id = current_users.company_id

2. WHERE

The where clause is where we filter down the rows from the table. We can filter on any supported data type. You may notice that column aliases and aggregates cannot be used in the where clause. This is because they are established later in SQL's order of operations. 

    where price > 200
    and product_name ilike '%iphone%'
    and purchase_date > '2018-01-01' 

3. GROUP BY

The group by clause is often used in conjunction with aggregate functions to return an aggregation of results grouped by one or more columns. 

4.  HAVING

As touched on previously, putting an aggregate function in the WHERE clause will throw an error. That is why we have the HAVING clause. The HAVING clause allows us to filter down a result set after the data is grouped and aggregated. Here is an example query that filters on an aggregate, 

    select
      user_id
      , count(transaction_id)
    from
      transactions
    where
      transaction_amount > 50
    group by
      user_id
    having
      count(transaction_id) > 10

5. Window Functions

Window functions come after the having clause. As such, they can only be used in the SELECT and ORDER BY clause. You can also use aggregate functions inside of the window function. 

6. SELECT 

The SELECT statement is where we define the columns and aggregate functions we want to return as columns on our table. 

7. DISTINCT

GROUP BY and DISTINCT can be essentially used the same when not utilizing an aggregate function. DISTINCT comes later in the order of operations, because it removes duplicate rows after all rows have been selected. However, in many cases, DISTINCT and GROUP BY will have the same query plan. This is because most databases are smart enough to recognize both have the same outcome and will choose the most efficient plan of execution. 

8. UNION

A union takes two queries that can both stand alone as valid queries and stacks them on top of each-other to combine as one. 

9. ORDER BY 

Once all of our data has been grouped and aggregated the ORDER BY clause will sort the resulting set of rows.  Because it comes so late in the order of operations we can order by aggregates, window functions, and column aliases. We can also re-order unioned tables. 

10. LIMIT

The LIMIT clause is where we can define the amount of rows we want returned by our query. It can also be used in conjunction with order by to return the top or bottom x amount of rows. We can also use OFFSET to return a given number of rows past a given row position.  