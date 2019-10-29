# Get Yesterday's Date


Often times, we want to analyze data with the date from yesterday. How do we auto-populate yesterday's date? There are a few formats that we can use!

 

The syntax below lets us get yesterday's date with timestamp:

    select dateadd(day,-1,getdate())
    
![yesterday1](/SQL/Get_Yesterdays_Date/Images/yesterday1.png "yesterday1")

To only get yesterday's date at 00:00:00: 

    select dateadd(day,-1,trunc(getdate()))

![yesterday2](/SQL/Get_Yesterdays_Date/Images/yesterday2.png "yesterday2")

If you wish to get the date and ditch the timestamp completely, you can use the SQL formatter!

    select  [dateadd(day,-1,getdate()):date]
    
![yesterday3](/SQL/Get_Yesterdays_Date/Images/yesterday3.png "yesterday3")

You can also use the interval syntax for a more elegant code:

    select [getdate():date] - interval '1 day'
    
![yesterday4](/SQL/Get_Yesterdays_Date/Images/yesterday4.png "yesterday4")



