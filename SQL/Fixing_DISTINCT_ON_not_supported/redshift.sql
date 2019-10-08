with dataset as (
select 'bart' as name, 'first bart' as text_value, 1 as ordering
  union all select 'homer', 'second homer', 2
  union all select 'bart', 'second bart', 2
  union all select 'homer', 'first homer', 1
)
select distinct
  name
  , first_value(text_value) over(partition by name order by ordering rows between unbounded preceding and unbounded following) as text_value
from
  dataset