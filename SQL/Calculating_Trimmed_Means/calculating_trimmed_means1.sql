with t2 as (select
      case
        when amt_paid <= PERCENTILE_DISC(0.1) WITHIN group(order by amt_paid) over()
          then null
        when amt_paid >= PERCENTILE_DISC(1-0.1) WITHIN group(order by amt_paid) over()
          then null
        else amt_paid end as trimmed_vals
  from
    t1)
  select avg(trimmed_vals) from t2 