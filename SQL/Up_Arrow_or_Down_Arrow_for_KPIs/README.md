# Up Arrow or Down Arrow for KPIs

Use this case statement to add up and down arrows to your metrics, for instance:

![arrows](/SQL/Up_Arrow_or_Down_Arrow_for_KPIs/Images/arrows.png)

	case
	   when [value_field] < lag([value_field]) over(order by [order_field])
	     then '▲ '
	   when [value_field] = lag([value_field]) over(order by [order_field])
	     then 'no change'
	   else '▼ '
	 end || [value_field] as [value_field]