import csv, ast, psycopg2

f = open('/path/to/survey/data/survey_data.csv', 'r')
reader = csv.reader(f)

longest, headers, type_list = [], [], []

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

statement = 'create table stack_overflow_survey ('

for i in range(len(headers)):
    if type_list[i] == 'varchar':
        statement = (statement + '\n{} varchar({}),').format(headers[i].lower(), str(longest[i]))
    else:
        statement = (statement + '\n' + '{} {}' + ',').format(headers[i].lower(), type_list[i])

statement = statement[:-1] + ');'

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