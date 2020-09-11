# compile_data.py - assemble the dataset 
import pandas as pd
import datetime

# Create the dataframe
#df = pd.read_csv("US_Accidents_June20.csv")
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
popDfIn = pd.read_csv("population_by_zip_small")
demographics = list(sorted(set(popDfIn['gender'] + ' ' + popDfIn['minimum_age'].astype('str') + '-' + popDfIn['maximum_age'].astype('str'))))
zips = list(sorted(set(popDfIn['zipcode'])))
popDfOut = pd.DataFrame(columns=['zip'] + demographics)
for iter, row in df.iterrows():
  pass
print(popDfOut)