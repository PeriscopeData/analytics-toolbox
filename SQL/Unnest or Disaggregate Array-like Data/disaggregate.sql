with food as (
select '2018-09-03' as date, 'bananas, apples, pears' as food_i_ate
union all
select '2018-09-04', 'pizza, spinach, apples'
union all
select '2018-09-05', 'eggs, pears, sausage'
union all
select '2018-09-06', 'salad, bacon, kabob'
union all
select '2018-09-07', 'sushi, dosa, rice'
)
, numbers as (
  select
  row_number() over()::int as part_number
from
  users
)
select
  date
  , split_part(food_i_ate, ',', part_number) as food
from
  food
  cross join numbers
where
split_part(food_i_ate, ', ', part_number) is not null
and split_part(food_i_ate, ', ', part_number) <> ''
order by 1