# SQL Division

## Problem

You have written the query below, using the attached user_summary table. The fourth column of your output is supposed to show the percent active users (which is the second column divided by the third column)

	select
	  platform
	  , active_users
	  , total_users
	  , active_users / total_users as percent_active_users
	from
	  user_summary

However, the division returns 0 for all rows. Looking at columns 2 and 3 this should not be the case.

![incorrect](/SQL/SQL_Interview_Questions/Q6_SQL_Division/Images/incorrect.png)

How can we correct this?

## Solution

Multiply the numerator by 1.0

	select
	  platform
	  , active_users
	  , total_users
	  , active_users * 1.0 / total_users as percent_active_users
	from
	  user_summary

![solution](/SQL/SQL_Interview_Questions/Q6_SQL_Division/Images/solution.png)

Concepts Covered: Integer Division

Explanation:

In SQL, dividing 2 integers returns an integer. A quick way to resolve this is to multiply the numerator by 1.0. This divides a float by an integer, returning a float output.