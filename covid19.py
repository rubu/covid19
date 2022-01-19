from datetime import date
import urllib.request
import urllib.parse
import json

def execute_sql_query(query):
    try:
        request = urllib.request.urlopen(f'https://data.gov.lv/dati/lv/api/3/action/datastore_search_sql?sql={urllib.parse.quote(query)}')
        result = json.loads(request.read().decode('utf-8'))
        if ('success' not in result or result['success'] != True or 'result' not in result):
            print(f'failed to execute query "${query}", result: result')
            quit()
        result = result['result'] 
        if ('records' in result):
            return result['records']
        return []
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        quit()

data_interval_query = 'SELECT MIN("Vakcinācijas datums"), MAX("Vakcinācijas datums") from "9320d913-a4a2-4172-b521-73e58c2cfe83"'
data_interval_result = execute_sql_query(data_interval_query)
if (len(data_interval_result) == 0):
    print('failed to obtain vaccination time range')
    quit()
print(f'results range from {data_interval_result[0]["min"]} to {data_interval_result[0]["max"]}')

vaccine_stage_query = 'SELECT DISTINCT "Vakcinācijas posms" from "9320d913-a4a2-4172-b521-73e58c2cfe83"'
vaccine_stage_result = execute_sql_query(vaccine_stage_query)
if (len(data_interval_result) == 0):
    print('failed to obtain vaccination stages')
    quit()

for vaccination_stage in vaccine_stage_result:
    group_size_query = f'SELECT SUM("Vakcinēto personu skaits") from "9320d913-a4a2-4172-b521-73e58c2cfe83" WHERE "Vakcinācijas posms" = "{vaccination_stage["Vakcinācijas posms"]}"'
    group_size_result = execute_sql_query(group_size_query)
    print(group_size_result)