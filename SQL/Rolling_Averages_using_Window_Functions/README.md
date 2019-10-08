# Rolling Averages using Window Functions


![Rolling Average](/SQL/Rolling_Averages_using_Window_Functions/images/rolling_average.png)

#### Background

Want to show a rolling average for your data, but not the granular breakdown? We can use the average window function to run this calculation.

First, I created a CTE that contains the number of new users per day on a fictional gaming platform. If you want to read more on CTEs, check out our post here!
 
#### Code

      new_users as (
        select
          [created_at:date] as created_date
          , count(*) as number_users
        from
          users
        group by
          1
        order by
          1
      )

Next, we run this window function to get a rolling average from the preceding 9 rows to the current row. To read more on window function, check out this post here!

    avg(number_users) over(order by created_date rows 9 preceding) as rolling_avg
    
Putting everything together: 

Want to show a rolling average for your data, but not the granular breakdown? We can use the [average window function](https://docs.aws.amazon.com/redshift/latest/dg/r_Examples_of_avg_WF.html) to run this calculation.

First, I created a CTE that contains the number of new users per day on a fictional gaming platform. If you want to read more on CTEs, check out our post [here](https://community.periscopedata.com/t/x1pz4j/everything-about-ctes)

with
  new_users as (
    select
      [created_at:date] as created_date
      , count(*) as number_users
    from
      users
    group by
      1
    order by
      1
  )
Next, we run this window function to get a rolling average from the preceding 9 rows to the current row. To read more on window function, check out this post [here](https://community.periscopedata.com/t/63278y/window-functions)!

    avg(number_users) over(order by created_date rows 9 preceding) as rolling_avg

Putting everything together: 

    with
      new_users as (
        select
          [created_at:date] as created_date
          , count(*) as number_users
        from
          users
        group by
          1
        order by
          1
      )
    select
      created_date
      , number_users
      , avg(number_users) over(order by created_date rows 9 preceding) as rolling_avg
    from
      new_users

Now, we can plot only the rolling average line, as shown here:

![Rolling Average](/SQL/Rolling_Averages_using_Window_Functions/images/rolling_average.png)

Tip: If you want to display both the raw data and the rolling average, Periscope's built-in visualizations has a quick "Show Rolling Average" check box that you can toggle on. 

![Format Chart](/SQL/Rolling_Averages_using_Window_Functions/images/format_chart.png)

If your version of SQL doesn't support window functions, then you can use [Periscope Data's Python/R integration to run the same calculation in R](https://doc.periscopedata.com/article/r-and-python#article-title) (as shown [here](https://community.periscopedata.com/t/36ba3d/using-r-to-plot-only-the-rolling-average-line)), or using Python (shown [here](https://community.periscopedata.com/t/63baxv)).

