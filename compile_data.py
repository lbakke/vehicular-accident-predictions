# compile_data.py - assemble the dataset 
import pandas as pd
import datetime

# Create the dataframe

df = pd.read_csv("US_Accidents_June20.csv")

def fix_zip(zip): 
    if isinstance(zip, str): 
        if '-' in zip: 
            fixed = int(zip.split('-')[0])
        else: 
            fixed = int(zip)
        return fixed
    else: 
        return None 


df['Zipcode'].map(fix_zip)

df.Start_Time = df['Start_Time'].astype('string')
df = df[df['Start_Time'].str.contains("2018|2019|2020")]

print(df)
df.Zipcode = df['Zipcode'].astype('string')
print(df['Zipcode'])

# income_df = pd.read_csv("income_data_small.csv")

#####
def pop_row_to_demo(row):
    gender = row['gender'] if not pd.isnull(row['gender']) else 'total'
    minAge = int(row['minimum_age']) if not pd.isnull(row['minimum_age']) else '~'
    maxAge = int(row['maximum_age']) if not pd.isnull(row['maximum_age']) else '~'
    return '{} {}-{}'.format(gender, minAge, maxAge)

def fix_gender(row): 
    if not pd.isnull(row):
        return row
    else: 
        return 'total'

def fix_age(row): 
    if not pd.isnull(row): 
        return row
    else:
        return '~'

def get_pop_by_zip(filename):
    popDfIn = pd.read_csv(filename)

    popDfIn['gender'].map(fix_gender)

    popDfIn['minimum_age'].map(fix_age)

    popDfIn['maximum_age'].map(fix_age)


    popDfIn.pop('geo_id')
    popDfIn.pop('population')
    popDfIn = popDfIn.rename(columns={'zipcode': 'Zipcode'})
    popDfIn.Zipcode = popDfIn['Zipcode'].astype('string')
    print("here??")
    print(popDfIn)
    print(popDfIn['Zipcode'])
    #popDfIn = popDfIn[~popDfIn.index.duplicated(keep='first')]
    popDfIn = popDfIn.drop_duplicates(subset="Zipcode", keep="first")
    print("222\n\n\n\n\n")
    print(popDfIn)
    return popDfIn

def aggregate_income_data(columns, filename="14zpallagi.csv"): 
    income_df = pd.read_csv(filename, usecols=columns)

    income_df = income_df[income_df.zipcode != 0]
    income_df = income_df.rename(columns={'zipcode': 'Zipcode'})
    income_df.Zipcode = income_df['Zipcode'].astype('string')

    print("**** \n\n\n")
    print(income_df.groupby("Zipcode").mean())

    return income_df.groupby("Zipcode").mean()

popByZip = get_pop_by_zip("population_by_zip_2010.csv")

columns = ["zipcode", "A00100", "A00700"]
income_df = aggregate_income_data(columns)

income_df.index.rename("Zipcode", inplace=True)
print(popByZip['Zipcode'])

df = df.set_index('Zipcode')
print(df)

df = df.join(income_df, on="Zipcode")

popByZip = popByZip.set_index('Zipcode')
print(popByZip)
print(income_df)
# print(df)
df = df.join(popByZip, on="Zipcode")
# df = df[~df.index.duplicated(keep='first')]
# df = df.merge(popByZip)
# df = df.join(popByZip)
print(df)

df.to_csv('full_data_final.csv')













''' OLD CODE ''' 

# for row in df.itertuples():
#     # print(df['Zipcode'])
#     # print(iter)
#     if '-' in row[19]:      # zipcode
#         # df[row['Zipcode']] = row['Zipcode'].split('-')[0]
#         #df[df.Zipcode] = row['Zipcode'].split('-')[0]
#         #df[df.Zipcode == row['Zipcode']]['Zipcode'] = int(row['Zipcode'].split('-')[0])
#         #    income_df = income_df[income_df.zipcode != 0]
#         #df.iloc[iter, 17] = int(row['Zipcode'].split('-')[0])
#         df.replace(row[19], int(row[19].split('-')[0]), inplace=True)
#         # df = df.map(lambda x: )
#     else: 
#         df.replace(row[19], int(row[19]), inplace=True)
#     print(row[5])
#     time = row[5]

''' from pop function ''' 

    # demographics = list(sorted(demographics))
    # zips = list(sorted(set(popDfIn['zipcode'])))

    # popDfOut = pd.DataFrame(columns=['zip'] + demographics, index=zips)
    # print("created df")
    # for iter, row in popDfIn.iterrows():
    #     demo = pop_row_to_demo(row)
    #     zipcode = row['zipcode']
    #     popDfOut.at[zipcode, demo] = row['population'] 
    #     popDfOut.at[zipcode, 'zip'] = zipcode 
    # return popDfOut