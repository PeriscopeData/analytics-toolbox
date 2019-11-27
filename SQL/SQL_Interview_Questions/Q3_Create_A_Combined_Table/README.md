# Create a Combined Table

## Question

Inspect the attached managers and associates tables (also pasted below for reference). Create a combined table that contains all the data from all employees. 

Original Tables:

![original1](/SQL/SQL_Interview_Questions/Q3_Create_A_Combined_Table/Images/original1.png)

![original2](/SQL/SQL_Interview_Questions/Q3_Create_A_Combined_Table/Images/original2.png)

Desired Output:

![desired](/SQL/SQL_Interview_Questions/Q3_Create_A_Combined_Table/Images/desired.png)

## Solution

Use a union to combine records vertically / add rows from two separate tables together. The combined tables must have the same number of columns with the same data types.

We also added an order by employee_id to control the ordering of the output. Note that order by clauses must be added to the last select statement of a union clause.

	select * from managers
	union
	select *, null from associates
	order by employee_id

Concepts Covered: [Unions](https://www.w3schools.com/sql/sql_union.asp)

Explanation:

Unions vertically append rows from separate tables. Columns must match up in order by data type. In the example above, we have an integer, followed by a string, followed by an integer, followed by another integer field. The associates table being appended onto the managers table must also have the same format. Since we are missing a number_reports field from the associates table, we use "null" as a stand in