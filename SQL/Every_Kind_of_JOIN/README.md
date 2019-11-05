# Every Kind of JOIN

More often than not, you'll need data from multiple different tables to create the perfect chart! There are many ways to do this but the most common way in SQL would be to use Joins! 

There are four basic types of Joins: inner, left, right and full. Periscope also supports Cross Joins, Cross Database Joins, and our custom Automatic Join. Joins are placed after the FROM clause and is usually followed by an ON or USING clause where you specify the condition for joining. The syntax resembles the example below:

    select *
    from TableA
    left join TableB
      on TableA.id = TableB.user_id

## Basic Joins

When describing the 4 basic Joins, it's very common to use venn diagrams to show what information is included in the resulting table. The colored sections show what would be included in the end. The following diagrams are from [sql-joins.com](http://www.sql-join.com/sql-join-types/).

### 0. ON vs. USING

The ON clause is used to tell the query which columns to join two tables on. For example, if there is a 'users' table with an 'id' column, and a 'purchases' table which has a 'user_id' column, we would need to specify that 'id' and 'user_id' is where the tables should be joined using a '='. 

    from users
    join purchases
      on user.id = purchases.user_id
      
      
The USING clause is used when TableA and TableB share column names and we want to specify which shared column names to use for the match. If there is only one column in both tables that share the same name, neither the ON nor the USING clause is necessary.

The USING clause is usually used when the tables share more than one column name and we need to specify which column names to match to. For example, let's say, 'users' and 'purchases' both have columns named 'user_id',  'first_name', and 'last_name' but we only want to match columns 'user_id', then we'd use the syntax below:      
      
     from users
    join purchases
      using (user_id)    
      
### 1. INNER JOIN

Inner Join returns all records from two tables only if they both meet the join condition. Inner Join is the default Join if the type is not specified.      
      

![inner](/SQL/Every_Kind_of_JOIN/Images/inner.png)

### 2. LEFT JOIN

Left Join returns all records from Table A and the matched records from Table B. 

![left](/SQL/Every_Kind_of_JOIN/Images/left.png)

### 3. RIGHT JOIN

Right Join returns all records from Table B and the matched records from Table A. 

![right](/SQL/Every_Kind_of_JOIN/Images/right.png)

### 4. FULL JOIN

Full Join will return all of the records if there is a match in either Table A or Table B. 

![full](/SQL/Every_Kind_of_JOIN/Images/full.png)

### 5. OUTER JOIN

Left, Right and Full Joins are all Outer Joins so you may see them written as "Left Outer Join." An outer join returns the rows that include what an Inner Join would return but also includes the rows that don't have a match in both tables. That's why you may see some blank cells when using an Outer Join. 

## Additional Joins

### 1. CROSS JOIN

Cross Join returns a result that matches each item in Table A to every item in Table B. The size of the result set will be the number of rows in Table A multiplied by the number of rows in Table B. A Cross Join can actually be written without a JOIN clause and just separated by commas in the FROM clause.

    select *
    from TableA, TableB
    
It can also be written by joining on 1=1.

    select *
    from TableA
    join TableB
      on 1=1
      
### 2. Cross-Database JOIN

[Cross-Database Joins](https://doc.periscopedata.com/article/cross-database-joins) allow users to join tables from different databases by having the tables exist on the Periscope Cache or Warehouse. The syntax is similar to a single database join with the addition of the database name preceding the table name. 

    select *
    from database1.user as TableA
    right join database2.purchases as TableB
      on TableA.id = TableB.user_id
      
Cross-Database Joins must align with Redshift syntax rules and all the tables used in the join must be cached. 

### 3. Automatic JOIN

Periscope Data has created a shortcut to automatically Inner Join or Left Join tables together with a special syntax. These shortcuts will join the tables based on their primary keys, foreign keys, and common naming conventions. There cannot be whitespace within the brackets. 

For Inner Joins:

    select * from [TableA+TableB]
    
For Left Joins:

    select * from [TableA<TableB]
    
### 4. JOIN Views & CSVs

With the Cache and Warehouse infrastructure, users can Join to a [CSV upload](https://doc.periscopedata.com/article/csv-upload#JoinToCSV) or a [Periscope View](https://doc.periscopedata.com/article/joining-views). When joining CSVs and Views, all of the tables in the query must exist on the cache. The syntax is the same as joining two tables with the addition of brackets necessary for CSVs and Views. The alias of the CSV or View must be assigned within the brackets. 

    select *
    from TableA
    inner join [csv_or_view_name as TableB]
      on TableA.id = TableB.email
      
      
## Extra Documentation
Here are the official Periscope Data documents for [Cross-Database Joins](https://doc.periscopedata.com/article/cross-database-joins), [Automatic Joins](https://doc.periscopedata.com/article/automatic-joins), [Joining CSVs](https://doc.periscopedata.com/article/csv-upload#JoinToCSV), and [Joining Views](https://doc.periscopedata.com/article/joining-views). 