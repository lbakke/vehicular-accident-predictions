# compile_data.py - assemble the dataset 
import pandas as pd
import datetime

# Create the dataframe
#df = pd.read_csv("US_Accidents_June20.csv")
###
df = pd.read_csv("US_Accidents_small.csv")
for iter, row in df.iterrows():
    if '-' in row['Zipcode']:
        row['Zipcode'] = row['Zipcode'].split('-')[0]

    time = row['Start_Time']
    year = time.split("-")[0]
    if int(year) > 2017: 
        # keep and add columns from other tables
        print("keep")
    else: 
        # remove these rows 
        df.drop(iter, inplace=True)
    print()

print(df)

income_df = pd.read_csv("income_data_small")

#####
def pop_row_to_demo(row):
    gender = row['gender'] if not pd.isnull(row['gender']) else 'total'
    minAge = int(row['minimum_age']) if not pd.isnull(row['minimum_age']) else '~'
    maxAge = int(row['maximum_age']) if not pd.isnull(row['maximum_age']) else '~'
    return '{} {}-{}'.format(gender, minAge, maxAge)

def get_pop_by_zip(filename="population_by_zip_2010.csv"):
    popDfIn = pd.read_csv(filename)
    demographics = set(pop_row_to_demo(row) for iter, row in popDfIn.iterrows())
    demographics = list(sorted(demographics))
    zips = list(sorted(set(popDfIn['zipcode'])))
    popDfOut = pd.DataFrame(columns=['zip'] + demographics, index=zips)
    for iter, row in popDfIn.iterrows():
        demo = pop_row_to_demo(row)
        zipcode = row['zipcode']
        popDfOut.at[zipcode, demo] = row['population'] 
        popDfOut.at[zipcode, 'zip'] = zipcode 
    return popDfOut