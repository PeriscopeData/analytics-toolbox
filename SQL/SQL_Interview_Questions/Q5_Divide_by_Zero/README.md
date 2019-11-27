# Divide by Zero

## Question

Inspect the attached platform_summary table (screenshot below for reference). Our goal is to list each platform, along with our KPI "percent_active_users." We get this KPI by dividing active_users by total_users. However, the Android platform has 0 users, and will throw a divide by zero error in SQL. How can we perform this division without throwing the divide by zero error?

![original](/SQL/SQL_Interview_Questions/Q5_Divide_by_Zero/Images/original.png)

Desired Output:

![desired](/SQL/SQL_Interview_Questions/Q5_Divide_by_Zero/Images/desired.png)

## Solution

	select
	  platform
	  , case
	    when total_users = 0
	      then null
	    else active_users * 1.0 / total_users
	  end as percent_active_users
	from
	  platform_summary

Concepts Covered: SQL Division, Case When Statements

Explanation:

We write a [case when statement](https://docs.aws.amazon.com/redshift/latest/dg/r_CASE_function.html) to check if the denominator is 0. If it is, we return a null result, else we perform the division as normal. Note that we multiply the numerator by 1.0 as we are dividing 2 integers and looking for a float output.