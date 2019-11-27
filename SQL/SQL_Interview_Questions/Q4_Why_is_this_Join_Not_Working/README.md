# Why is this Join Not Working?

## Question

Inspect the attached all_platforms and july_data tables (screenshots below for reference). Our goal is to list each platform, along with its associated number_of_plays for the month of July. If a platform is not in the july_data table, we can assume the number of gameplays is 0. 

Original Tables:

![original1](/SQL/SQL_Interview_Questions/Q4_Why_is_this_Join_Not_Working/Images/original1.png)

![original2](/SQL/SQL_Interview_Questions/Q4_Why_is_this_Join_Not_Working/Images/original2.png)

Desired Output:

![desired](/SQL/SQL_Interview_Questions/Q4_Why_is_this_Join_Not_Working/Images/desired.png)

Problem:

Currently, you have the query below, but it isn't showing the iOS and android fields despite the join. In fact, this result looks exactly like the july_data table.

	select
	  all_platforms.platform
	  , july_data.number_of_plays
	from
	  all_platforms
	  join july_data on
	    all_platforms.platform = july_data.platform

![incorrect](/SQL/SQL_Interview_Questions/Q4_Why_is_this_Join_Not_Working/Images/incorrect.png)

How can you modify this query to get the desired output?

## Solution

Use a left join to preserve all the records from the all_platforms table. Also apply a coalesce function to fill in null values with 0 in the number_of_plays column.

	select
	  all_platforms.platform
	  , coalesce(july_data.number_of_plays,0) as number_of_plays
	from
	  all_platforms
	  left join july_data on
	    all_platforms.platform = july_data.platform

Concepts Covered: Left Joins, Join Logic, Coalesce

Explanation:

Joins by default are inner joins. In other words, the result will only contain records where all columns referenced in the join condition exist. In the original question, there are no rows for "iOS" or "android" in the july_data table. Therefore, these rows were omitted from the final result when using the default inner join.

To remedy this, use a [left join](https://www.w3schools.com/sql/sql_join_left.asp). Left joins preserve all the values in the first table referenced (in the example above, all_platforms). If the value does not show up in the second table, any columns from the second table in the result will contain a null value.

![incorrect](/SQL/SQL_Interview_Questions/Q4_Why_is_this_Join_Not_Working/Images/solution.png)

Now, we want to fill in a 0 for all the null values. This is where [coalesce](https://www.w3schools.com/sql/func_sqlserver_coalesce.asp) comes into play. If the first argument is null, coalesce replaces it with the second argument. In the code above, we fill in nulls with the integer 0.