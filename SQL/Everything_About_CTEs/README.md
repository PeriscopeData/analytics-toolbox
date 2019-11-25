# Everything About CTEs

CTEs (common table expressions - also commonly referred to as "with clauses") are an extremely powerful tool in SQL! Similar to subqueries, they can pull "a query in a query," but can be called multiple times within the same query especially easily! This is because CTEs are defined and named upfront.

Important note for MySQL Users: CTEs are only available in MySQL 8.0. For earlier versions of MySQL, use subqueries

Below are some FAQs on CTEs, post any further questions below!

1. When do I use a CTE?

CTEs are useful for running a query in a query (similar to subqueries!). CTEs come handy when we need to leverage a generated column in a query. For instance, the below instance would fail:

    select
      id
      , first_name || ' ' || last_name as full_name
    from
      users
    where
    len(full_name)>20

In the above example, we only defined full_name in this select statement itself. Therefore, we cannot use the column alias name until this select statement has run completely

To get this query to work, we need to wrap the above in a CTE. More info on CTE set up in FAQ 2!

	with
	  user_cte as (
	    select
	      id
	      , first_name || ' ' || last_name as full_name
	    from
	      users
	  )
	select
	  *
	from
	  user_cte
	where len(full_name)>20

2. How do I set up a CTE?

The basic structure of a CTE looks like this:

	with <cte_name> as (
	<query for CTE here>
	)
	select <columns> from <cte_name>
	...

Here's an example!

	with
	  user_cte as (
	    select
	      id
	      , first_name || ' ' || last_name as full_name
	    from
	      users
	  )
	select
	  *
	from
	  gameplays
	  join user_cte on
	    user_cte.id = gameplays.user_id

3. Can I use multiple CTEs in a query?

Absolutely! We can chain together CTEs as follows. Note that subsequent CTEs can call prior CTEs (in other words, we don't need to "nest" the CTEs)

	with
	  <cte_name_1> as (
	    <query for CTE 1 here>
	  )
	  , <cte_name_2> as (
	    <query for CTE 2 here>
	  )
	select
	  <columns>
	from
	  <cte_name_1> join <cte_name_2>. . .

Note that we only use "with" to open the first CTE, with commas linking subsequent CTEs.

More information on CTEs can be found on [AWS's documentation page](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html): 

Feel free to comment with any more questions or use cases for CTEs! And as always... Happy SQL :)