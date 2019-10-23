# Generate Series of Dates in Snowflake

As Snowflake doesn't have a native generate_series function, here is our solution to generating a table of incrementing dates, starting from the current date, in Snowflake. It is currently set to generate 1095 rows (3 years) of dates.

	select
	  dateadd(day, '-' || seq4(), current_date()) as dte
	from
	  table
	    (generator(rowcount => 1095))

