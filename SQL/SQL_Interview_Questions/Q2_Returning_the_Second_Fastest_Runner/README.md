# Returning the Second Fastest Runner

## Question

Return the second fastest runner from the list of runners below. The .csv of this data can be found attached to this post.

Original Table:

![original](/SQL/SQL_Interview_Questions/Q2_Returning_the_Second_Fastest_Runner/Images/original.png)

Desired Output:

![desired](/SQL/SQL_Interview_Questions/Q2_Returning_the_Second_Fastest_Runner/Images/desired.png)

## Solution

Apply a limit and offset with an order by to return the second fastest runner

	select
	  name
	  , seconds
	from
	  runners
	order by
	  seconds
	limit 1 offset 1

Concepts Covered: [Order by, Limit, Offset](https://docs.aws.amazon.com/redshift/latest/dg/r_ORDER_BY_clause.html)

Explanation:

We first need to arrange runners from fastest to slowest. This is done by applying "order by seconds." By default, SQL arranges numerical values from lowest to highest. If we had wanted to arrange numerical values from highest to lowest, we would run "order by second desc"

Then we apply a limit 1 to ensure our output only returns 1 row. If we wanted to return the fastest runner, we would be done! However, we need to apply an offset 1 to have SQL skip the first row and return the second. If we wanted to return the third fastest runner, we would have applied an offset 2. For the fourth fastest runner, we would have applied an offset 3, and so on.