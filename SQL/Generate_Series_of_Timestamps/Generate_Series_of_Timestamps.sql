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