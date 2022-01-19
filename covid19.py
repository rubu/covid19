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

vaccine_type_query = 'SELECT DISTINCT "Preparāts" from "9320d913-a4a2-4172-b521-73e58c2cfe83"'
vaccine_type_result = execute_sql_query(vaccine_type_query)
if (len(vaccine_type_result) == 0):
    print('failed to obtain vaccination stages')
    quit()


vaccine_stage_query = 'SELECT DISTINCT "Vakcinācijas posms" from "9320d913-a4a2-4172-b521-73e58c2cfe83"'
vaccine_stage_result = execute_sql_query(vaccine_stage_query)
if (len(data_interval_result) == 0):
    print('failed to obtain vaccination stages')
    quit()

for vaccine_stage in vaccine_stage_result:
    vaccine_stage_name = vaccine_stage['Vakcinācijas posms']
    total = 0
    vaccine_type_totals = []
    for vaccine_type in vaccine_type_result:
        vaccine_type_name = vaccine_type['Preparāts']
        vaccine_type_group_size_query = f'SELECT SUM("Vakcinēto personu skaits") from "9320d913-a4a2-4172-b521-73e58c2cfe83" WHERE "Vakcinācijas posms" = \'{vaccine_stage_name}\' and "Preparāts" = \'{vaccine_type_name}\''
        vaccine_type_group_size_result = execute_sql_query(vaccine_type_group_size_query)
        if vaccine_type_group_size_result[0]["sum"] != None:
            total += int(vaccine_type_group_size_result[0]["sum"])
            vaccine_type_totals.append({'type': vaccine_type_name, 'sum': vaccine_type_group_size_result[0]['sum']})
    vaccine_group_size_query = f'SELECT SUM("Vakcinēto personu skaits") from "9320d913-a4a2-4172-b521-73e58c2cfe83" WHERE "Vakcinācijas posms" = \'{vaccine_stage_name}\''
    total_from_database = int(execute_sql_query(vaccine_group_size_query)[0]['sum'])
    if total_from_database != total:
        print(f'!!! math does not add up for "{vaccine_stage_name}", calculated total: {total}, total from api: {total_from_database} !!!')
    print(f'{vaccine_stage_name}: {total}')
    for vaccine_type_total in vaccine_type_totals:
        print(f'\t{vaccine_type_total["type"]}: {vaccine_type_total["sum"]} ({round(int(vaccine_type_total["sum"]) * 100 / total, 2)}%)')