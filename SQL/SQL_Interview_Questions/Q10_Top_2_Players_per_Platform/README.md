# Top 2 Players per Platform

## Question

Inspect the table logged_plays attached to this community post. Write a query that pulls the top 2 users with the largest number of plays in each platform. Avoid using unions in your final solution.

Original Table:

![original](/SQL/SQL_Interview_Questions/Q10_Top_2_Players_per_Platform/Images/original.png)

Desired Output:

![desired](/SQL/SQL_Interview_Questions/Q10_Top_2_Players_per_Platform/Images/desired.png)

## Solution

	select
	 user_id
	 , platform
	 , number_plays
	from
	 (
	   select
	     *
	     , rank() over(partition by platform order by number_plays desc) as user_rank
	   from
	     logged_plays
	 ) ranked_users
	where
	 user_rank <= 2

Concepts Covered: Subquery Logic, Window Functions

Explanation:

We first start the explanation with the subquery ranked_users. Here, we are assigning a number to each user based on the value in the number_plays column. The top user in each category gets a value of 1, the runner up in each category gets a value of 2, and so on.

Taking a closer look at the frame clause of the window function (this is the section in parenthesis after “over.” Notice that we partition by the platform to assign ranks within each platform, and organize the values by “order by number_plays desc” so the highest value gets rank 1.

Why rank()? And not row_number()?

[Rank()](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_RANK.html) works best in this case due to how it manages ties. The [row_number()](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_ROW_NUMBER.html) window function is unable to distinguish ties, and will randomly assign a higher rank to one of the users. Rank() does account for ties. [Dense_rank()](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_DENSE_RANK.html) is a variation of rank() that many users choose to use as well. Note that if there are ties for first place, dense_rank() will also include the runner up’s records.

Now we may want to simply add “where user_rank=2” to this subquery, but note that column aliases cannot be used in the select statement where they are declared. Moreover, SQL doesn’t let us put window functions in WHERE clauses. Thus, we must use a subquery to enclose the window function logic. In the outer query, we can use the column alias user_rank. A CTE is also an acceptable alternative to a subquery.