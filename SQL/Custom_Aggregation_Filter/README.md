# Custom Aggregation Filter

Aggregating data by various periods of time is made easy with Periscope's built-in date [aggregation filter]((https://doc.periscopedata.com/article/sql-formatters-date-aggregation#article-title). Sometimes, however, you may wish to group your data by different periods of time. In this post, we'll look at how to create a custom filter that builds on the existing filter aggregation functionality in Redshift syntax.

With this filter, you'll be able to group by the following:

- Second
- Minute
- 5-Minute Interval
- Hour
- Day
- Week (starting on Sunday)
- Week starting on Monday
- Semi-Month*
- Month
- Bi-month (every two months)
- Quarter
- Year
- Decade
- Century
- Millennia
- All Time

Note: Semi-month defines the first half of the month as the 1st through the 15th and the second half as the 16th through the end of the month

Here's what we need to do:

1. Create and name the filter
2. Define filter values and names
3. Set the filter to radio buttons
4. Implement the matching expression
5. Use the filter in your charts!

## 1. Create and name the filter

This should be familiar to you if you've made a filter before! If not, check out [these instructions](https://doc.periscopedata.com/article/custom-filters#article-title)!

![Filter 1](/SQL/Custom_Aggregation_Filter/Images/create_filter.png)

## 2. Define filter values and names

For this filter, we'll need to manually input the names and values of the aggregation periods we want. We'll look at how to handle these values in step 4.

![Filter 2](/SQL/Custom_Aggregation_Filter/Images/names_and_vals.png)

## 3. Set the filter to radio buttons

To ensure only one filter value is selected at a time, we should enable the 'radio button' setting.

![Filter 3](/SQL/Custom_Aggregation_Filter/Images/filter_options.png)

## 4. Implement the matching expression

This code will execute in place of the filter in the chart query. Note that it doesn't evaluate to a boolean expression, instead, it directly produces dates that are used, typically in the select statement. See the example in the next step!

	case
	  when [value] = '5minute'
	    then TIMESTAMP 'epoch' + 5*60*floor(date_part('epoch', [column])/(5*60)) *INTERVAL '1 second'
	  when [value] = 'week_monday'
	    then date_trunc('week', [column] + '1 day'::interval)::date - '1 day'::interval
	  when [value] = 'total'
	    then '4713-1-1 BC'::datetime
	  when [value] = 'bimonthly'
	    then TO_DATE(date_part(year, [column]) || '-' || ceiling(date_part(month, [column])::numeric/2) * 2 - 1 || '-1', 'YYYY-MM-DD')
	  when [value] = 'semimonthly'
	    then TO_DATE(date_part(year, [column]) || '-' || date_part(month, [column]) || '-' || floor(sqrt(date_part(day, [column])::numeric/4+1)) * 15 - 14, 'YYYY-MM-DD')
	  when [value] is not null
	    then date_trunc([value] ,([column])::timestamp)::datetime
	  else date_trunc('date' ,([column])::timestamp)::datetime
	end

## 5. Use the filter in your charts!

Once you've implemented this filter, try creating a chart with the following code:

	select [mydate=custom_aggregation], count(*)
	from
	(select '1999-12-31 23:59:59'::datetime as mydate
	union all select '1999-12-31 23:59:59'::datetime
	union all select '2000-1-1 10:00:00'::datetime
	union all select '2000-1-1 10:03:00'::datetime
	union all select '2000-1-1 10:06:00'::datetime
	union all select '2000-1-1 10:07:00'::datetime
	union all select '2000-1-6 10:06:00'::datetime
	union all select '2000-1-7 10:06:00'::datetime
	union all select '2000-1-8 10:06:00'::datetime
	union all select '2000-1-9 10:06:00'::datetime
	union all select '2000-1-9 10:06:00'::datetime
	union all select '2000-1-9 10:06:00'::datetime
	union all select '2000-2-9 10:06:00'::datetime
	union all select '2000-2-13 10:00:00'::datetime
	union all select '2000-2-16 10:00:00'::datetime
	union all select '2000-2-17 10:00:00'::datetime
	union all select '2001-2-16 10:00:00'::datetime
	union all select '2001-6-16 10:00:00'::datetime
	union all select '2001-7-16 10:00:00'::datetime
	union all select '2001-8-16 10:00:00'::datetime
	union all select '2101-9-16 10:00:00'::datetime) mytable
	group by 1
	order by 1

After saving the chart, you should be able to use the filter you just created in the dashboard to explore groupings by different time periods! This query explicitly defines the values in the date column, so it's very easy to debug and practice working with datetimes in this chart!

## 6. Can you expand it to add another type?
Some of these periods are automatically handled by Redshift, and others are computed through SQL code we write ourselves in the matching expression. Can you tell which date aggregations are manually calculated and handled?

As another bonus question, take a look at how we handle 5-minute intervals. Can you update the filter so that it can handle 6 hour intervals?

Answers below:

1. We manually create the 5-minute interval, week-starting-Monday, All-Time, Semi-Monthly, and Bi-Monthly aggregation periods!

2. Code below

	```when [value] = '6hours' then TIMESTAMP 'epoch' + 6*60*60*floor(date_part('epoch', [column])/(6*60*60)) * INTERVAL '1 second'```

Note: Here is how to do bi-weekly on Redshift. 

	case
      when DATEDIFF(week, DATE_TRUNC('week', [column]), '7/27/2014') % 2 = 0
        then DATEADD(week, 2, DATE_TRUNC('week', [column])) -1
      else DATEADD(week, 1, DATE_TRUNC('week', [column])) -1
    end
