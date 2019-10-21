# Manipulating Dates, Datetimes, Unix Timestamps, and other date formatting tricks in Redshift


Dates aren't stored in the database in the format you want to display? You can use the Redshift TO_CHAR() function to create a string-formatted extract in order to display dates however you want! 

Note that in Redshift, there are DATE (no timestamp), TIMESTAMP (timestamp, no timezone) and TIMESTAMPTZ (timestamp with time zone) types. Another common datetime type you'll find is the UNIX timestamp, which is usually a 10 digit integer, representing the number of seconds passed since 1970-01-01 00:00:00 UTC (midnight). Less commonly you may find them with 13 digits (3 extra digits for millisecond precision) or 16 digits (microsecond precision). I've not seen a 19-digit nanosecond precision UNIX timestamp out in the wild, but if you happen to find one let me know. 

Reference Documents:

 
Redshift Datetime types - https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html

Redshift formatters - https://docs.aws.amazon.com/redshift/latest/dg/r_FORMAT_strings.html

Postgres - https://www.postgresql.org/docs/9.5/static/functions-formatting.html



    SELECT to_char(getdate(), 'Mon') -> 'Feb'

    SELECT to_char(getdate(), 'MON') -> 'FEB'

    SELECT to_char(getdate(), 'Month') -> 'February'

    SELECT to_char(getdate(), 'Mon DD HH12:MI:SS') -> 'Feb 27 12:39:12' (12-hour clock)

    SELECT to_char(getdate(), 'Mon DD, HH24:MI:SS.MS') -> 'Feb 27, 00:39:12.331' (24-hour clock, milliseconds)
    
How about something like grabbing the week number out of 52?
 
    select to_char(getdate(), 'WW') -> 09
    
try 'DDD' for day number, 'D' for day of week (Sunday =1), or maybe you just really want the month number in Roman numerals; use 'RM' (or 'rm' lower case) for that. 

What if you have a unix timestamp i.e. 1519692428 ? Redshift doesn't have a native 'timestamp_to_datetime' type function.  Luckily, you can use our [Periscope Date Aggregators](https://doc.periscopedata.com/article/sql-formatters-date-aggregation), here we'll use the :ts aggregator which turns a unix timestamp into a datetime:

    SELECT to_char([1519716997:ts] , 'W')  -> 4 (week of month)

What if you want to display the dates in the format 'Q1 - 2018'?

    select to_char([1519692428:ts], 'YYYY') || ' - Q' || to_char([1519692428:ts], 'Q')
    
But what if you're running this directly on your Redshift cluster (outside of periscope) and don't have access to our handy SQL formatters? 

    SELECT to_char(TIMESTAMP 'epoch' + 1519692428 * interval '1 second', 'DD-Mon-YY HH24:MM:SS') -> 27-Feb-18 00:02:08
    
More generally:

    SELECT to_char(TIMESTAMP 'epoch' + YOUR_UNIX_TIMESTAMP_COLUMN * interval '1 second', '<formatter string>')

And the reverse, taking a date/datetime, and converting to unix timestamp (remember to account for timezone conversions if you have a TIMESTAMPTZ - unix timestamps are always defined in UTC) 

    SELECT extract(epoch from getdate()) -> 1520205318
    
If you have a 13-digit timestamp (instead of the standard 10-digit), your timestamp is in milliseconds. Divide by 1000 (or if you don't care about the precision, just take the leftmost 10 digits) and use the above function. Same procedure for 16-digit microsecond timestamps.

Between CAST/CONVERT, EXTRACT, TO_CHAR, and the date formatters, you can take any kind of date field and display it however you'd like! 

The examples above use the current-datetime-returning GETDATE() function; in Postgres, you'll use NOW(). You can pass any date or datetime column in for these examples, although you'll ned to make sure your underlying column has the necessary precision (i.e. a DATE type doesn't have time precision).

Maybe your data is a bit messier and you have the date field stored as a string with mixed dates and datetimes. (if anyone has unix timestamps and nulls mixed in with their date/datetimes, buy your DBA a drink and ask them to fix it. But really, if someone is actually facing this issue, let me know in the comments and I'll whip up a solution... then ask your DBA to fix it).  Or maybe you just need more manual control over over the output, like perhaps you wish to capitalize month names, but only if they're 31 days long, and also include the number of days in the month. The tried-and-true CASE WHEN never fails:  

    CASE WHEN  extract(MONTH from date_column::date) = 1 then 'JANUARY (31 Days)'
     WHEN date_part(month, date_column::date) = 2 then 'February (28 Days)'
     WHEN extract(month from date_column::date) = 3 then 'MARCH (31 Days)'
     WHEN date_part(month, date_column::date) = 4 then 'April (30 Days)'
    ...
    END as month_name
    
and so on. You can use what you prefer between EXTRACT and DATE_PART here. If you're working with time precision, make sure to cast using ::timestamp instead of ::date. 

Finally, you probably don't want to type that in every time, so use a [Periscope SQL Snippet](https://doc.periscopedata.com/article/snippets) to save and reuse!