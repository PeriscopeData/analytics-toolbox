# Aggregating Data by Multiple Fields

## Question

Inspect the attached all_users table from a hypothetical gaming company (also pasted below for reference). Create a table that summarizes the number of users per platform and source.

Original Table:

![original](/SQL/SQL_Interview_Questions/Q1_Aggregating_Data_by_Multiple_Fields/Images/original.png)

Desired Output:

![desired](/SQL/SQL_Interview_Questions/Q1_Aggregating_Data_by_Multiple_Fields/Images/desired.png)

## Solution

Apply a limit and offset with an order by to return the second fastest runner

	select
	  platform
	  , source
	  , count(*)
	from
	  all_users
	group by
	  platform
	  , source
	order by
	  platform
	  , source

Concepts Covered: [Aggregates, Group by](https://docs.aws.amazon.com/redshift/latest/dg/c_Aggregate_Functions.html)

Explanation:

We first want to determine the columns we want shown. Here we want a platform, source, and the number of the users that belong to that platform-source combination. For the first two columns, we call the platform and source fields, separated by a comma. To pull the count, we use the [count aggregate function](https://docs.aws.amazon.com/redshift/latest/dg/r_COUNT.html). Note that the * is shorthand for "count all the rows." The same result can be achieved with count(1).

Since we have a mix of aggregates (the count function) and non aggregates (the platform and source fields) in our select list, we must apply a group by. In the group by, we need to list all the non-aggregated columns from our query. In this case, this is platform and source. The group by can be read as "count all the rows, bucketing them into categories based on their platform and source."

Lastly we applied an [order by](https://docs.aws.amazon.com/redshift/latest/dg/r_ORDER_BY_clause.html) so all the rows of the same platform are grouped together in a more readable format.