import pandas as pd
import os


start_folder = "C:\\Users\\hppc\\Desktop\\GitHub\\wildfire_prediction\\data\\dasikes_pirkagies"
fire_data = pd.DataFrame()
columns_to_read = ["AREA", "PREFECTURE", "START_DAY", "START_TIME", "END_DATE", "END_TIME", "FOREST_AREA"]
os.chdir(start_folder)

list_of_files = os.listdir(os.getcwd())
for current_file in list_of_files:
    if not current_file.endswith("2012.xlsx"):
        print(current_file)
        temp_df = pd.read_excel(current_file, index_col=False, usecols=columns_to_read)
        fire_data = fire_data.append(temp_df)
    else:
        temp_df = pd.DataFrame()
        xls = pd.ExcelFile(current_file)
        df_1 = pd.read_excel(xls, sheet_name='2000', usecols=columns_to_read)
        df_2 = pd.read_excel(xls, sheet_name='2001', usecols=columns_to_read)
        df_3 = pd.read_excel(xls, sheet_name='2002', usecols=columns_to_read)
        df_4 = pd.read_excel(xls, sheet_name='2003', usecols=columns_to_read)
        df_5 = pd.read_excel(xls, sheet_name='2004', usecols=columns_to_read)
        df_6 = pd.read_excel(xls, sheet_name='2005', usecols=columns_to_read)
        df_7 = pd.read_excel(xls, sheet_name='2006', usecols=columns_to_read)
        df_8 = pd.read_excel(xls, sheet_name='2007', usecols=columns_to_read)
        df_9 = pd.read_excel(xls, sheet_name='2008', usecols=columns_to_read)
        df_10 = pd.read_excel(xls, sheet_name='2009', usecols=columns_to_read)
        df_11 = pd.read_excel(xls, sheet_name='2010', usecols=columns_to_read)
        df_12 = pd.read_excel(xls, sheet_name='2011', usecols=columns_to_read)
        df_13 = pd.read_excel(xls, sheet_name='2012', usecols=columns_to_read)

        fire_data = fire_data.append(df_1)
        fire_data = fire_data.append(df_2)
        fire_data = fire_data.append(df_3)
        fire_data = fire_data.append(df_4)
        fire_data = fire_data.append(df_5)
        fire_data = fire_data.append(df_6)
        fire_data = fire_data.append(df_7)
        fire_data = fire_data.append(df_8)
        fire_data = fire_data.append(df_9)
        fire_data = fire_data.append(df_10)
        fire_data = fire_data.append(df_11)
        fire_data = fire_data.append(df_12)
        fire_data = fire_data.append(df_13)


fire_data[['START_YEAR', 'START_MONTH', 'START_DAY']] = fire_data['START_DAY'].astype(str).str.split('-', expand=True)
fire_data[['START_HOUR']] = fire_data['START_TIME'].astype(str).str[:2]
fire_data[['START_MINUTE']] = fire_data['START_TIME'].astype(str).str[3:5]

fire_data[['END_YEAR', 'END_MONTH', 'END_DAY']] = fire_data['END_DATE'].astype(str).str.split('-', expand=True)
fire_data[['END_DAY']] = fire_data['END_DAY'].astype(str).str[:2]
fire_data[['END_HOUR']] = fire_data['END_TIME'].astype(str).str[:2]
fire_data[['END_MINUTE']] = fire_data['END_TIME'].astype(str).str[3:5]

print(fire_data['END_DATE'].unique())
print(fire_data['END_YEAR'].unique())
print(fire_data['END_MONTH'].unique())
print(fire_data['END_DAY'].unique())
print(fire_data['END_HOUR'].unique())
print(fire_data['END_MINUTE'].unique())

#print(fire_data['START_YEAR'].unique())

#fire_data.to_pickle('C:\\Users\\hppc\\Desktop\\GitHub\\wildfire_prediction\\data\\fire_data.pkl')
