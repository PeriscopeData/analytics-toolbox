# Average Salary of a Manager's Direct Reports

## Question

Inspect the table employee_data attached to this community post. Write a query that shows the average salary of each manager’s direct reports.

Original Table:

![original](/SQL/SQL_Interview_Questions/Q9_Average_Salary_of_a_Managers_Direct_Reports/Images/original.png)

Desired Output:

![final](/SQL/SQL_Interview_Questions/Q9_Average_Salary_of_a_Managers_Direct_Reports/Images/final.png)

## Solution

	select
	 managers.employee_name
	 , [avg(employees.salary):$] as avg_report_salary
	from
	 employee_data employees
	 join employee_data managers on
	   employees.manager_id = managers.employee_id
	group by
	 managers.employee_name

Concepts Covered: Self Joins

Explanation:

Now we can easily write a query where we aggregate the average salary by manager_id, but that doesn’t give us the names of the managers. For the output to be more reader friendly, we need to implement a [self join](https://www.w3schools.com/Sql/sql_join_self.asp).

In the process of a self join, we create 2 copies of this table. One is named employees, and the other is named managers. We join the managers copy on the criteria that the manager_id in the employees table matches the employee_id of the managers table. In other words, we are joining the manager information using the manager_id field in the original table.

For formatting the currencies, we used a handy [Periscope shortcut](https://doc.periscopedata.com/article/sql-formatters-dollars-percent#article-title), but this isn't required for the calculation.