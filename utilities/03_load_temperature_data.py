import pandas as pd
import os


start_folder = "C:\\Users\\hppc\\Desktop\\GitHub\\wildfire_prediction\\data\greek_fire_data"
columns_to_read = ["STATION", "DATE", "SOURCE", "LATITUDE", "LONGITUDE", "ELEVATION", "NAME", "REPORT_TYPE", "QUALITY_CONTROL", "WND", "CIG", "VIS", "TMP", "DEW"]

os.chdir(start_folder)

data = pd.DataFrame()

for i in range(2000, 2020):
    working_folder = str(i)
    os.chdir(f"{working_folder}")

    list_of_files = os.listdir(os.getcwd())
    for current_file in list_of_files:
        temp_df = pd.read_csv(current_file, index_col=False, usecols=columns_to_read)
        temp_df['YEAR'] = i
        data = data.append(temp_df)

    os.chdir("C:\\Users\\hppc\\Desktop\\GitHub\\wildfire_prediction\\data\greek_fire_data")

print(f"Total Rows: {data.shape[0]}")
print(data.head())
print(data.NAME.unique())
