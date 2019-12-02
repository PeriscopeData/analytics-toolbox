# CASE WHEN Statements

## Overview
CASE WHEN statements provide great flexibility when dealing with buckets of results or when you need to find a way to filter out certain results. You can think of these almost as IF-THEN statements similar to other coding languages. Below you'll learn the proper syntax, where these can be placed in your query and a few examples that should help get you started. Happy Periscoping! 😊

## Standard Syntax

When using a CASE WHEN statement, it's important to remember you need a condition, what to do when that condition is met, and an END clause. A simple example is below:

```SQL
CASE
    WHEN condition
        THEN result
    ELSE other_result
END
```

More often than not, you'll want multiple buckets, or have multiple conditions for your data! To add these, include more WHEN and THEN statements.

```SQL
CASE
  WHEN  condition
    THEN result
  WHEN  condition_2
    THEN result_2
  ELSE other_result
END
```

**Reminder:** Remember to include one (and only one!) ELSE clause followed by your END statement.


## Organization

So where can these CASE WHEN statements be placed? Almost, anywhere!

If you'd like to change some results in a column to different values, this can be done in the select statement. In this example, let's say North and South Dakota put aside their differences and became one Dakota. You could update the results of your state column with a CASE WHEN statement!

```SQL
SELECT
  CASE
    WHEN state = 'North Dakota'
      THEN 'Dakota'
    WHEN state = 'South Dakota'
      THEN 'Dakota'
    ELSE state
  END
```

If you'd like to filter out specific results, but you have to depend on another value to know which results to filter, a CASE WHEN statement could be helpful in your WHERE clause! A great example of this can be found when using multiple Periscope filters in one query.

```SQL
SELECT *
FROM table
WHERE
CASE
  WHEN 'default' IN ('[name_filter|default]')
    THEN [id_column=id_filter]
  WHEN 'default' IN ('[id_filter|default]')
    THEN [name_column=name_filter]
  ELSE [id_column=id_filter] OR [name_column=name_filter]
END
```

A full explanation of the above can be found here: [filters-in-case-when-statements](https://community.periscopedata.com/t/63166r/filters-in-case-when-statements)

Finally, CASE WHEN statements can be used to help you order rows in the proper way. Let's say in your state's data there are rows that have blank values for states! You can still order those in another way, for instance by city name.

```SQL
SELECT *
FROM table
ORDER BY
(CASE
    WHEN state IS null
      THEN city
    ELSE state
END)
```

The above should help you get up and running with the CASE WHEN statement in no time! Which is your favorite way to use the CASE statement? Any creative use cases for this function while you have been working in Periscope? Post your thoughts below! 😊

Note: Link to filters-in-case-when-statements currently goes to community page not GitHub