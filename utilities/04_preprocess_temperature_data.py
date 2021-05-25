import pandas as pd
import os


start_folder = "C:\\Users\\hppc\\Desktop\\GitHub\\wildfire_prediction\\data\\greek_fire_data"
os.chdir(start_folder)

columns = ['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'LATITUDE', 'LONGITUDE', 'NAME', 'TEMPERATURE', 'TEMPERATURE_VALID', 'DIRECTION', 'WIND_VALID', 'CODE', 'SPEED', 'WIND_SPEED_VALID', 'DEW', 'DEW_VALID']
processed_data = pd.DataFrame(columns=columns)

columns_to_read = ["DATE", "LATITUDE", "LONGITUDE", "NAME", "WND", "TMP", "DEW"]

for i in range(2000, 2020):
    working_folder = str(i)
    os.chdir(f"{working_folder}")

    list_of_files = os.listdir(os.getcwd())
    for current_file in list_of_files:
        data = pd.read_csv(current_file, index_col=False, usecols=columns_to_read)

        temperature_data = pd.DataFrame()
        wind_data = pd.DataFrame()
        dew_data = pd.DataFrame()
        datetime_data = pd.DataFrame()

        temperature_data[['TEMPERATURE', 'TEMPERATURE_VALID']] = data['TMP'].str.split(',', 1, expand=True)
        wind_data[['DIRECTION', 'WIND_VALID', 'CODE', 'SPEED', 'WIND_SPEED_VALID']] = data['WND'].str.split(',', expand=True)
        dew_data[['DEW', 'DEW_VALID']] = data['DEW'].str.split(',', 1, expand=True)
        datetime_data[['YEAR', 'MONTH', 'DAYTIME']] = data['DATE'].str.split('-', expand=True)
        datetime_data[['DAY']] = datetime_data['DAYTIME'].str[:2]
        datetime_data[['HOUR']] = datetime_data['DAYTIME'].str[3:5]
        datetime_data[['MINUTE']] = datetime_data['DAYTIME'].str[6:8]

        datetime_data = datetime_data.drop('DAYTIME', 1)

        temperature_data['TEMPERATURE'] = pd.to_numeric(temperature_data['TEMPERATURE'])/10
        wind_data['SPEED'] = pd.to_numeric(wind_data['SPEED'])/10
        dew_data['DEW'] = pd.to_numeric(dew_data['DEW'])/10

        columns = ['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'LATITUDE', 'LONGITUDE', 'NAME', 'TEMPERATURE', 'TEMPERATURE_VALID', 'DIRECTION', 'WIND_VALID', 'CODE', 'SPEED', 'WIND_SPEED_VALID', 'DEW', 'DEW_VALID']

        merged_data = pd.DataFrame(columns=columns)

        merged_data[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']] = datetime_data[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']]
        merged_data[['LATITUDE', 'LONGITUDE', 'NAME']] = data[['LATITUDE', 'LONGITUDE', 'NAME']]
        merged_data[['TEMPERATURE', 'TEMPERATURE_VALID']] = temperature_data[['TEMPERATURE', 'TEMPERATURE_VALID']]
        merged_data[['DIRECTION', 'WIND_VALID', 'CODE', 'SPEED', 'WIND_SPEED_VALID']] = wind_data[['DIRECTION', 'WIND_VALID', 'CODE', 'SPEED', 'WIND_SPEED_VALID']]
        merged_data[['DEW', 'DEW_VALID']] = dew_data[['DEW', 'DEW_VALID']]

        processed_data = processed_data.append(merged_data)

    os.chdir(start_folder)

print(processed_data.head())

processed_data.to_pickle('C:\\Users\\hppc\\Desktop\\GitHub\\wildfire_prediction\\data\\processed_data.pkl')

#print(processed_data.to_string())

'''
print(merged_data.head())

# Count dataloss
print(f"Invalid Temperature: {merged_data[merged_data['TEMPERATURE_VALID'] != '1'].count()[0]}")
print(f"Invalid Wind Direction: {merged_data[merged_data['WIND_VALID'] != '1'].count()[0]}")
print(f"Invalid Wind Speed: {merged_data[merged_data['WIND_SPEED_VALID'] != '1'].count()[0]}")
print(f"Invalid Dew: {merged_data[merged_data['DEW_VALID'] != '1'].count()[0]}")
'''
