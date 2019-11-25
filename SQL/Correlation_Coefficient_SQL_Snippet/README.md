# Correlation Coefficient SQL Snippet

Want to create a convenient Periscope SQL Snippet which emulates a function and returns the (Pearson) correlation coefficient between two variables?

Create a [Parameterized SQL Snippet](https://doc.periscopedata.com/article/parameterized-sql-snippets#article-title) called 'correlation_calc(metric_1 , metric2)' and insert the following SQL: 

	(avg([metric_1]*[metric_2]) - (avg([metric_1]) * avg([metric_2]))) / ( stddev_pop([metric_1]) * stddev_pop([metric_2]) )

To call this function (for example, say between a 'height' and 'weight' column), simply call in your select field: 

	correlation_calc(height,weight) as correlation_betweeen_height_and_weight

to return the correlation coefficient (which ranges from -1 to +1) between your two variables! 

Share your convenient statistical snippets - covariance, autocorrelation, there are many useful snippets to create!

Note - this uses the stddev_pop Redshift function. If you're working with samples, use stddev_samp() instead. 