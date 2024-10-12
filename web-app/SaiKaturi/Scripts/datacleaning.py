import pandas as pd 
import os

def check_null_values(dataset):
    return dataset.isna().sum()
def clean_data(dataset):
    i = dataset[dataset['Salary'].isna()].index
    dataset = dataset.drop(i) ## dropping the records with missing values in salary column 
    dataset['Location'] = dataset['Location'].apply(lambda x: "United States" if pd.isnull(x) else x)
    directory = os.path.expanduser('Data/Cleaned')
    dataset.to_csv(os.path.join(directory,'Cleaned.csv'))
    return dataset

def datacleaningnofile():
    directory = os.path.expanduser('Data/Cleaned')
    dataset = pd.read_csv(os.path.join(directory,'Cleaned.csv'))
    return dataset