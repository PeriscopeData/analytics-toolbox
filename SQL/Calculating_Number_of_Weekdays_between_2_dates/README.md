# Calculating Number of Weekdays between 2 Dates (Redshift and Postgres)


The parameterized snippet below can be used to find the number of weekdays between 2 dates. We named this one **difference_in_weekdays(start_date,end_date)**

## Redshift

    (DATEDIFF('day', [start_date], [end_date]))
    -(DATEDIFF('week',[start_date], [end_date]) * 2)
    -(CASE WHEN DATE_PART(dow, [start_date]) = 0 THEN 1 ELSE 0 END)
    -(CASE WHEN DATE_PART(dow, [end_date]) = 6 THEN 1 ELSE 0 END)
    
## Postgres

    DATE_PART('day',[[end_date]:week]::timestamp - [[start_date]:week]::timestamp) -
     (TRUNC(DATE_PART('day', [[end_date]:week]::timestamp - [[start_date]:week]::timestamp )/7) * 2)
      - (CASE WHEN EXTRACT (dow from [start_date]::timestamp) NOT IN (0) THEN EXTRACT (dow from [start_date]::timestamp) - 1 ELSE 5 END)
      + (CASE WHEN EXTRACT (dow from [end_date]::timestamp) NOT IN (0) THEN EXTRACT (dow from [end_date]::timestamp) - 1 ELSE 5 END)
      
The snippet can then be called in a query as shown below:

    select [difference_in_weekdays('2017-06-20','2018-07-16')]
    
Which returns 279.

Source: Based off the solution [here](https://stackoverflow.com/questions/252519/count-work-days-between-two-dates).
