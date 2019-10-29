# Using Python to Write a Create Table Statement and Load a CSV into Redshift

![Header](/Python/Using_Python_to_Write_a_create_table_statement_and_load_a_CSV_into_Redshift/Images/header.png)

Usually when I need to upload a CSV I will use Periscope Data's CSV functionality. It's fast, easy, allows me to join the data with all my databases, and automatically casts types. Sometimes, however, I like to interact directly with a Redshift cluster—usually for complex data transformations and modeling in Python. When interacting directly with a database, it can be a pain to write a create table statement and load your data. When the table is wide, you have two choices while writing your create table—spend the time to figure out the correct data types, or lazily import everything as text and deal with the type casting in SQL. The first is slow, and the second will get you in trouble down the road.

I recently ran into a great example of this when I found out that Stack Overflow released their awesome-as-always survey results for 2017. They are available in a CSV format, but a daunting 158 columns wide. I wanted to load the data into Redshift—and rather than be generous in my data types, I wanted to use the proper columns. I decided to speed up the load process by writing a Python script, which turned into a fun exercise in data type detection. 

## Importing Libraries and Reading Data in Python

The first step is to load our data, import our libraries, and load the data into a CSV reader object. The csv library will be used to iterate over the data, and the ast library will be used to determine data type.

We will also use a few lists. "Longest" will be a list of the longest values in character length to specify varchar column capacity, "headers" will be a list of the column names, and "type_list" will be the updating list of column types as we iterate over our data.

    import csv, ast, psycopg2

    f = open('/path/to/survey/data/survey_data.csv', 'r')
    reader = csv.reader(f)
    
    longest, headers, type_list = [], [], []

## Finding the Data Type

Once we have our data, we need to find the data type for each row. This means we need to evaluate every value and cast to the most restrictive option, from decimalized numbers to integers, and from integers to strings.

The function dataType does this. First, it evaluates to see if the value is text or a number, and then for the appropriate type of number if needed. This function consumes both the new data, and the current best type to evaluate against.

    def dataType(val, current_type):
        try:
        # Evaluates numbers to an appropriate type, and strings an error
            t = ast.literal_eval(val)
        except ValueError:
            return 'varchar'
        except SyntaxError:
           return 'varchar'
       if type(t) in [int, long, float]:
           if (type(t) in [int, long]) and current_type not in ['float', 'varchar']:
           # Use smallest possible int type
               if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
                   return 'smallint'
               elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
                   return 'int'
               else:
                   return 'bigint'
           if type(t) is float and current_type not in ['varchar']:
               return 'decimal'
        else:
           return 'varchar'

We can iterate over the rows in our CSV, call our function above, and populate our lists.

    for row in reader:
        if len(headers) == 0:
            headers = row
            for col in row:
                longest.append(0)
                type_list.append('')
        else:
            for i in range(len(row)):
                # NA is the csv null value
                if type_list[i] == 'varchar' or row[i] == 'NA':
                    pass
                else:
                    var_type = dataType(row[i], type_list[i])
                    type_list[i] = var_type
            if len(row[i]) > longest[i]:
                longest[i] = len(row[i])
    f.close()

And use our lists to write the SQL statement.

    statement = 'create table stack_overflow_survey ('

    for i in range(len(headers)):
        if type_list[i] == 'varchar':
            statement = (statement + '\n{} varchar({}),').format(headers[i].lower(), str(longest[i]))
        else:
            statement = (statement + '\n' + '{} {}' + ',').format(headers[i].lower(), type_list[i])

    statement = statement[:-1] + ');'

Finally, our output!

    create table stack_overflow_survey_data (
        respondent int,
        , professional varchar(56)
        , programhobby varchar(45)
        , country varchar(34)
        ....
        , expectedsalary decimal);

## Finishing the Job

Of course, the job isn't done—the data needs to get into Redshift! This can be done using the psycopg2 library, and the astute reader will notice we imported it above. To use the **copy** command, I first loaded the data to S3. The access key ID and secret access key can be found under users in your AWS console.

You can find additional details about the **copy** command used below on our blog, [How to ETL Data into and out of Amazon Redshift](https://www.periscopedata.com/blog/etl-data-into-and-out-of-amazon-redshift).

    conn = psycopg2.connect(
        host='mydb.mydatabase.us-west-2.redshift.amazonaws.com',
        user='user',
        port=5439,
        password='password',
        dbname='example_db')

    cur = conn.cursor()

    cur.execute(statement)
    conn.commit()

    sql = """copy stack_overflow_survey_data from 's3://an-example-bucket/survey_data.csv'
        access_key_id '<access_key_id>'
        secret_access_key '<secret_access_key>'
        region 'us-west-1'
        ignoreheader 1
        null as 'NA'
        removequotes
        delimiter ',';"""
    cur.execute(sql)
    conn.commit()

And you're ready to begin examining some awesome Stack Overflow data! 

Let's make a few quick charts to celebrate. Stack Overflow asked a great series of questions asking people what attributes are the most important when making technical hires—including knowledge of algorithms, communications skills, titles and education. 

We can compare a couple of those questions with the average salary of the respondents:

    select
     importantHiringAlgorithms
      , avg(salary) as salary
      , count(*) as respondents
    from
      stack_overflow_survey_data
    group by
      1
    order by
      1
 
And we quickly see that average respondent's salary actually decreases with a focus on data structures and algorithms when hiring! In contrast, a heavier emphasis on communications skills is associated with higher salaries.

![Knowledge of Algoithms](/Python/Using_Python_to_Write_a_create_table_statement_and_load_a_CSV_into_Redshift/Images/Knowledge_of_Algoithms.png)

How important should each of the following be in the hiring process? 

When we look a level deeper, we can see why—students aren't worried about communications skills yet.

![Knowledge of Algoithms Area](/Python/Using_Python_to_Write_a_create_table_statement_and_load_a_CSV_into_Redshift/Images/Knowledge_of_Algoithms_Area.png)


While Stack Overflow didn't ask for respondent's titles, I suspect an emphasis on communication skills continues to grow as people advance their careers. It turns out communications skills are highly valued. Luckily, we've written a [post about communications in analytics](https://www.periscopedata.com/blog/communication-is-critical-in-analytics)!