#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("10_25_data/full_data_10_25.csv")

''' Begin k-fold validation techniques '''
# Shuffle dataset randomly
df = df.sample(frac=1).reset_index(drop=True)


# Create a copy of the data frame
copy = df.copy()
# Sample 80% of dataframe for training
# The random_state paramter means there is a different random split each run
train = copy.sample(frac=0.8, random_state=0) 
test_and_valid = copy.drop(train.index) 
# Sample half of the remaining 20% for testing and half for validation (10% of original df each)
test = test_and_valid.sample(frac=0.5, random_state=0)
valid = test_and_valid.drop(test.index)

# Write groups to their respective files
train.to_csv('./10_25_data/training_data_10_25.csv')
test.to_csv('./10_25_data/testing_data_10_25.csv')
valid.to_csv('./10_25_data/validation_data_10_25.csv')


# TODO: try 70% training and 30% testing 

'''end = group_size * 8
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



# Display number of each type of accident severity
print(f"Severity 1: {len(df[df['Severity'] == 1])}")
print(f"Severity 2: {len(df[df['Severity'] == 2])}")
print(f"Severity 3: {len(df[df['Severity'] == 3])}")
print(f"Severity 4: {len(df[df['Severity'] == 4])}")'''
