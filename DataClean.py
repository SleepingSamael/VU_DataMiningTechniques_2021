import numpy as np
import pandas as pd
import re
# Plots
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


def import_data(dir):
    df = pd.read_excel(dir)
    df.columns = ['Tijdstempel', 'Programme', 'ML', 'IR', 'Statistics', 'Databases', 'Gender', 'Chocolate',
                  'Birthday', 'Neighbors', 'Stand-up', 'Stress-level', '100euro', 'Random-number',
                  'Time2bed', 'Good-day1', 'Good-day2']
    return df


def clean_data(df):
    for index, row in df.iterrows():
        # Programme
        prog = row['Programme']
        if 'artificial' in prog.lower() or 'ai' in prog.lower():
            df.at[index, 'Programme'] = 'AI'
        elif 'computer' in prog.lower() or 'cs' in prog.lower():
            df.at[index, 'Programme'] = 'CS'
        elif 'computational' in prog.lower() or 'cls' in prog.lower():
            df.at[index, 'Programme'] = 'CLS'
        elif 'bioinformatics ' in prog.lower():
            df.at[index, 'Programme'] = 'Bioinfo'
        elif 'business analysis' in prog.lower() or 'ba' in prog.lower():
            df.at[index, 'Programme'] = 'BA'
        elif 'quantitative risk management' in prog.lower() or 'qrm' in prog.lower():
            df.at[index, 'Programme'] = 'QRM'
        else:
            df.at[index, 'Programme'] = 'Others'
        # ML
        if row['ML'] not in ['yes', 'no', 'unknown']:
            df.at[index, 'ML'] = 'unknown'
        # IR
        if row['IR'] not in [0, 1, 'unknown']:
            df.at[index, 'IR'] = 'unknown'
        # Statistics
        if row['Statistics'] not in ['mu', 'sigma', 'unknown']:
            df.at[index, 'Statistics'] = 'unknown'
        # DB
        if row['Databases'] not in ['nee', 'ja', 'unknown']:
            df.at[index, 'Databases'] = 'unknown'
        # Gender
        if row['Gender'].lower() not in ['male', 'female']:
            df.at[index, 'Gender'] = 'others'
        # Chocolate
        if row['Chocolate'] not in ['slim', 'fat', 'neither']:
            df.at[index, 'Chocolate'] = 'unknown'
        # Birthday
        age = 'unknown'
        birthday = row['Birthday']
        bir_list = re.findall(r'\d+', str(birthday))
        for item in bir_list:
            if item.isdigit():
                if len(item) == 4:
                    if 1922 < int(item) < 2022:
                        age = 2022 - int(item)
                elif len(item) == 2:
                    if 90 <= int(item) <= 99:
                        age = 122 - int(item)
                elif len(item) == 8:
                    if 1922 < int(item[0:4]) < 2022:
                        age = 2022 - int(item[0:4])
                    elif 1922 < int(item[-4:]) < 2022:
                        age = 2022 - int(item[-4:])

        df.at[index, 'Age'] = age
        # TODO:Extract birthday from dates in different formats

        # Neighbors
        neighbors = row['Neighbors']
        if not (str(neighbors).isdigit() and 0 <= int(neighbors) <= 8):
            df.at[index, 'Neighbors'] = 'unknown'
        # Stand-up
        if row['Stand-up'] not in ['yes', 'no', 'unknown']:
            df.at[index, 'Databases'] = 'unknown'
        # Stress - level
        stress_level = row['Stress-level']
        if not str(stress_level).lstrip('-').isdigit():
            print(type(stress_level))
            if type(stress_level) == float:
                pass
            else:
                stress_list = re.findall(r'\d+', stress_level)
            if stress_list:
                stress_level = stress_list[0]
        if str(stress_level).isdigit():
            if int(stress_level) > 100:
                df.at[index, 'Stress-level'] = 100
            elif int(stress_level) < 0:
                df.at[index, 'Stress-level'] = 0
        else:
            df.at[index, 'Stress-level'] = 'unknown'
        # Random-number
        if not str(row['Random-number']).isdigit():
            df.at[index, 'Random-number'] = 'unknown'
        # Time2bed
        time2b = str(row['Time2bed'])
        if ':' not in time2b and '.' not in time2b:
            if 'am' in time2b.lower() or 'pm' in time2b.lower():
                time_list = re.findall(r'\d+', time2b)
                if not time_list:
                    continue
                if 12 > int(time_list[0]) > 6:
                    time = f'{int(time_list[0]) + 12}:00:00'
                elif int(time_list[0]) < 6:
                    time = f'{time_list[0]}:00:00'
                else:
                    df.at[index, 'Time2bed'] = pd.Timestamp(pd.NaT)
                    continue
                df.at[index, 'Time2bed'] = pd.to_datetime(time, format='%H:%M:%S').time()
            else:
                df.at[index, 'Time2bed'] = pd.Timestamp(pd.NaT)
        else:
            time_list = re.findall(r'\d+', time2b)
            if not time_list:
                continue
            if 12 > int(time_list[0]) > 6:
                time = f'{int(time_list[0]) + 12}:00:00'
            elif int(time_list[0]) < 6:
                if 0 < int(time_list[1]) < 60:
                    time = f'{time_list[0]}:{time_list[1]}:00'
                else:time = f'{time_list[0]}:00:00'
            else:
                df.at[index, 'Time2bed'] = pd.Timestamp(pd.NaT)
                continue
            df.at[index, 'Time2bed'] = pd.to_datetime(time, format='%H:%M:%S').time()

    return df


def save_data(df):
    saved_df = df
    saved_fetures = ['Programme', 'ML', 'IR', 'Statistics', 'Databases', 'Gender', 'Chocolate',
                     'Neighbors', 'Stand-up', 'Stress-level', 'Random-number', 'Time2bed', 'Age']
    saved_df[saved_fetures].to_csv('ODI/ODI-2022-cleaned.csv', index=False)
    print('Data saved')


if __name__ == '__main__':
    df = import_data('ODI/ODI-2022.xlsx')
    df = clean_data(df)
    save_data(df)

