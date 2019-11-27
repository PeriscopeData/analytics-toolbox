# Why do I have the wrong platform?

## Question

You have written the query below, using the attached all_users and all_platforms table. The goal of this query is to break down the users by platform and source, only focusing on those from the android platform. For reference, the all_platforms table is pasted below.

![original](/SQL/SQL_Interview_Questions/Q7_Why_do_I_have_the_Wrong_Platform/Images/original.png)

	select
	 platform
	 , source
	 , count(*)
	from
	 all_users
	where
	 platform = (
	   select
	     platform
	   from
	     all_platforms
	   limit 1
	 )
	group by
	 1
	 , 2

But wait, I’m seeing that all the platforms are showing up as “web.”

![incorrect](/SQL/SQL_Interview_Questions/Q7_Why_do_I_have_the_Wrong_Platform/Images/incorrect.png)

How can we correct this?

## Solution

Solution:

Add an “order by 1” in the subquery to ensure that the platform names are sorted alphabetically.

	select
	 platform
	 , source
	 , count(*)
	from
	 all_users
	where
	 platform = (
	   select
	     platform
	   from
	     all_platforms
	   order by 1
	   limit 1
	 )
	group by
	 1
	 , 2
 
Concepts Covered: Limits and Order By Clauses

Explanation:

SQL outputs do not have a defined order unless specified in an order by clause.  In other words, "select" returns records in no particular order if there isn't an order by clause. Therefore, the “limit 1” is randomly returning one platform each time the query was run previously. 