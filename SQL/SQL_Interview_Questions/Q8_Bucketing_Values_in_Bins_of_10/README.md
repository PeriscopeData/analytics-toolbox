# Bucketing Values in Bins of 10

## Question

inspect the numbers table (a screenshot of the first few rows is provided below). Create a table with a count of frequencies, dividing the values in buckets of 10. Ex: 5 entries between 0 and 10, 4 entries between 10 and 20, and so on.

Original Table:

![original](/SQL/SQL_Interview_Questions/Q8_Bucketing_Values_in_Bins_of_10/Images/original.png)

Desired Output:

Note: since the original table was generated using the Random() function, your exact frequencies may differ from the table below.

![desired](/SQL/SQL_Interview_Questions/Q8_Bucketing_Values_in_Bins_of_10/Images/desired.png)

## Solution

Solution:

	select
	 (floor(my_value / 10.0) * 10 )::varchar(3) || ' to ' || (ceil(my_value / 10.0) * 10 )::varchar(3) as bucket
	 , count(*) as frequency
	from
	 numbers
	group by
	 1, (floor(my_value / 10.0) * 10 )
	order by
	 (floor(my_value / 10.0) * 10 )

Concepts Covered: Floor and Ceiling functions, Aggregations, Casting Data Types, Concatenation (Some may opt to use a Case When statement)

Explanation:

Note: since this table was generated using the Random() function, your exact frequencies may differ from the “Desired Output.”

One approach would be to create a [case when](https://docs.aws.amazon.com/redshift/latest/dg/r_CASE_function.html) in the select statement that tests to see if a value is under 10, then assign a value ‘0 to 10’, else if the value is under 20, assign a value ‘10 to 20,’ and so on. However, we can do this much more simply using [floor](https://docs.aws.amazon.com/redshift/latest/dg/r_FLOOR.html) and [ceiling](https://docs.aws.amazon.com/redshift/latest/dg/r_CEILING_FLOOR.html) functions. In the solution above, we use the floor function to find the lower bound of the bucket, and the ceil function to find the upper bound. We then cast the results of the floor and ceiling as a value that can be [concatenated](https://docs.aws.amazon.com/redshift/latest/dg/r_concat_op.html) with a string ‘ to ‘. Note that Redshift and PostgresSQL have a shortcut to cast data types (::). Other flavors of SQL can use a 9Cast function](https://www.w3schools.com/sql/func_sqlserver_cast.asp).

To get the frequency, we run a count(*), grouping by the first column. Note that we also need to group by the same field mentioned in the order by for this query to run in Redshift.