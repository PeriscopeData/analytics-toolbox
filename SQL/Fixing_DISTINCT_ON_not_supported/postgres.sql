with dataset as (
select 'bart' as name, 'first bart' as text_value, 1 as ordering
  union all select 'homer', 'second homer', 2
  union all select 'bart', 'second bart', 2
  union all select 'homer', 'first homer', 1
)
select distinct on (name)
    name
    , text_value
  from
    dataset
  order by
    name
    , ordering