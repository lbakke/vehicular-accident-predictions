# compile_data.py - assemble the dataset 
import pandas as pd
import datetime

feature_names = ["ID", "Source", "TMC", "Start_Time", "End_Time", "Start_Lat", "Start_Lng", "Distance(mi)", "Description", "Street", "Side", "City", "County", "State", "Country", "Timezone", "Airport_Code", "Weather_Timestamp", "Temperature(F)", "Wind_Chill(F)", "Humidity(%)", "Pressure(in)", "Visibility(mi)", "Wind_Direction", "Wind_Speed(mph)", "Precipitation(in)", "Weather_Condition", "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout", "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop", "Sunrise_Sunset", "Civil_Twilight", "Nautical_Twilight", "Astronomical_Twilight", "A00100", "A00700", "minimum_age", "maximum_age", "gender"]

# Create the dataframe

df = pd.read_csv("US_Accidents_June20.csv")

def fix_zip(zip): 
    if isinstance(zip, str): 
        if '-' in zip: 
            fixed = int(zip.split('-')[0])
        else: 
            fixed = int(zip)
        return str(fixed)
    else: 
        return None 

def fix_others(feature): 
    if None: 
        return feature
    else:
        return str(feature)


df['Zipcode'] = df['Zipcode'].map(fix_zip)

df.Start_Time = df['Start_Time'].astype('string')
df = df[df['Start_Time'].str.contains("2018|2019|2020")]

df.Zipcode = df['Zipcode'].astype('string')
df = df.drop(columns=['Number'])
df = df.drop(columns=['End_Lat'])
df = df.drop(columns=['End_Lng'])

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
    popDfIn = popDfIn.drop_duplicates(subset="Zipcode", keep="first")
    return popDfIn

def aggregate_income_data(columns, filename="14zpallagi.csv"): 
    income_df = pd.read_csv(filename, usecols=columns)

    income_df = income_df[income_df.zipcode != 0]
    income_df = income_df.rename(columns={'zipcode': 'Zipcode'})
    income_df.Zipcode = income_df['Zipcode'].astype('string')

    return income_df.groupby("Zipcode").mean()

popByZip = get_pop_by_zip("population_by_zip_2010.csv")

columns = ["zipcode", "A00100", "A00700"]
income_df = aggregate_income_data(columns)

income_df.index.rename("Zipcode", inplace=True)
df = df.set_index('Zipcode')
df = df.join(income_df, on="Zipcode")

popByZip = popByZip.set_index('Zipcode')
df = df.join(popByZip, on="Zipcode")

# eliminate nan's 
for feature in feature_names: 
    df = df[pd.notnull(df[feature])]

''' begin k-fold validation technique '''
#1 shuffle dataset randomly

df = df.sample(frac=1)

#2 split into 10 groups of equal size
length = len(df.index)
group_size = int(length/10)
prev = 0

#3 use 8 of these groups for training, 1 for testing, and 1 for validation
# write directly to their respective files 

end = group_size * 8
newdf = df.iloc[prev:end]
prev = end + 1
newdf.to_csv('training_data_10_25.csv')

end = 9 * group_size
newdf = df.iloc[prev:end]
prev = end + 1
newdf.to_csv('testing_data_10_25.csv')

end = 10 * group_size
newdf = df.iloc[prev:end]
prev = end + 1
newdf.to_csv('validation_data_10_25.csv')
