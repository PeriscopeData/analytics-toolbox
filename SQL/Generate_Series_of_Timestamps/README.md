# Generate Series of Timestamps (1 second intervals)

There may be several reasons why you want to create a list of dates or timestamps. The primary use case is to left join a dataset that has missing dates onto this full list of dates so you can clearly show where no data is reported.

Postgres has a handy generate_series function, but we need to be more creative with other flavors of SQL. Check out [this blog post](https://www.periscopedata.com/blog/generate-series-in-redshift-and-mysql) to see how to generate a list of dates when you don't have the option to use Postgres's generate_series!

Now, let's say you want to generate a list of timestamps, separated by 1 second instead. The approach is very similar to that in the post, check out the snippet below!

**Note**: The below query is in Redshift syntax

	with
	  numbers as (
	    select
	      row_number() over(order by true) as n
	    from -- use any table that has ample rows
	      users
	  )
	select
	  getdate() - n * interval '1 second'
	from
	  numbers