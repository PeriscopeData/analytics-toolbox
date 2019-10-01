#Objective: Create a bubble chart where we can have the ability to set the size of the bubbles
#Dataset: This dataset from Kaggle describes the listing activity and metrics in NYC, NY for 2019

#Columns:
# Primary Key, Numeric: ID --'listing id'
# String: Name --'name of the listing'
# Foreign Key, Numeric: host_id --'host id'
# String: host_name --'name of the host'
# String: neighbourhood_group --'location'
# String: neighbourhood --'area'
# Latitude Coordinates: latitude --'latitude coordinates'
# Longitude Coordinates: longitude --'longitude coordinates'
# String: room_type --'listing space type'
# Numeric: price --'price in dollars'
# Numeric: minimum_nights --'amount of nights minimum'
# Numeric: number_of_reviews --'number of reviews'
# Datetime: last_review --'latest review'
# Numeric: reviews_per_month --'number of reviews per month'
# Numeric: calculated_host_listings_count --'amount of listing per host'
# Numeric: availability_365 --'number of days when listing is avaliable for booking'

#SQL output is imported as a dataframe variable called 'df'
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

#This line shows the periscope data frame, and is primarily used to just visualize the SQL output.
periscope.table(df)

#Next, we are going to create the data points.
data=[go.Scatter(
    x=df['neighborhood'], y=df['average_price'],mode='markers', marker=dict(size=0.1*df['average_price'],color=df['average_price'],showscale=True))]

#Then we will want to label the chart's title, x-axis, y-axis, and also set the margins of the chart.
layout = go.Layout(title='Cost of NYC Airbnbs by Neighborhood', xaxis = {'title':'NYC Neighborhoods'}, yaxis = dict(title = 'Average Cost of Airnbs/Night (Dollars)'), margin=dict(l=50,r=50,b=125,t=25),hovermode='closest')

#Let's create the layout and plot out the data points.
fig = go.Figure(data=data,layout=layout)

#Now, we can visualize the final figure.
periscope.plotly(fig)