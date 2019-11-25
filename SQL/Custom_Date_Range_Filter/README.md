# Custom Date Range Filter

**Update:** Periscope Data now allows you the ability to create additional date range filters without having to go through the below workaround. Refer to our docs [here](https://doc.periscopedata.com/article/date-range-filters) under "Additional Date Range Filters"

Sometimes, users would like to apply their own data range filters on top of Periscope Data's default [Date Range filter](https://doc.periscopedata.com/article/date-range-filters). This is useful for cases where there are multiple data columns for a dataset, and different filtering criteria should be applied to each.

The default date range filter has 2 options: either select a pre-determined interval (ex: 1 day, 7 days, 90 days) or enter your own start and end date. We've outlined how to replicate each of these options below:

**Option 1: Show a list of intervals**

Create a new filter and assign names and values for your desired intervals

![daterange1](/SQL/Custom_Date_Range_Filter/Images/daterange1.png)

Select "Match an expression for this filter" and enter the following SQL. Note you would have to tailor this slightly if your intervals differ slightly from the above!

	case
	  when [value] = '365' then [column] between getdate()::date - interval '364 day' and getdate()::date + interval '1 day'
	  when [value] = '180' then [column] between getdate()::date - interval '179 day' and getdate()::date + interval '1 day'
	  when [value] = '90' then [column] between getdate()::date - interval '89 day' and getdate()::date + interval '1 day'
	  when [value] = 'mtd' then [column] >= date_trunc('month', (getdate())::timestamp)::date
	  when [value] = 'ytd' then [column] >= date_trunc('year', (getdate())::timestamp)::date
	else 1=1 end

**Option 2: Allow the User to Select any Start and End Date**

In this case, we need to create 2 filters - one for start date and one for end date. Both will have a generated a list of dates for the user to select from. This would be a comprehensive list of all dates in the dataset.

For both the start and end date filters: In "Get names and values from the database," we want to run the following query on any table with a large number of rows (we derive the dates using the row_number window function)

	select (
	    getdate()::date - row_number() over (order by true)
	  )::date as n
	from table_with_many_rows order by 1 desc 

Then select "Match an expression for this filter"

For the start date filter, use the following expression

	[column]>=[value]

For the end date filter, use the following expression

	[column]<=[value]

The final result will look like the screenshot below. To quickly call a certain date, the user can begin typing in their desired date in the open text field at the top of the filter instead of scrolling through all the options!

![daterange2](/SQL/Custom_Date_Range_Filter/Images/daterange2.png)