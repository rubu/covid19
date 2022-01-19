from datetime import date
import urllib.request
import urllib.parse
import json

def execute_sql_query(query):
    request = urllib.request.urlopen(f'https://data.gov.lv/dati/lv/api/3/action/datastore_search_sql?sql={urllib.parse.quote(query)}')    
    return request.read().decode('utf-8')

data_interval_query = 'SELECT MIN("Vakcinācijas datums"), MAX("Vakcinācijas datums") from "9320d913-a4a2-4172-b521-73e58c2cfe83"'
data_interval_result = json.loads(execute_sql_query(data_interval_query))
if ('success' not in data_interval_result or data_interval_result['success'] != True or 'result' not in data_interval_result):
    print(f'failed to obtain start and end timestamps of the data collection, response: {data_interval_result}')
    quit()

result = data_interval_result['result']
if ('records' not in result):
    print('invalid result format')
    quit()

records = result['records']
if (len(records) == 0):
    print('result does not contain any records')
    quit()

date_interval = records[0]
print(f'results range from {date_interval["min"]} to {date_interval["max"]}')

group_size_query = 'SELECT COUNT("Vakcinēto personu skaits") from "9320d913-a4a2-4172-b521-73e58c2cfe83" GROYP BY("Vakcinācijas posms")'
group_size_result = json.loads(execute_sql_query(group_size_query))
print(group_size_result)