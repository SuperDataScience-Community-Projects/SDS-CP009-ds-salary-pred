import pandas as pd 

def check_null_values(dataset):
    return dataset.isna().sum()
def clean_data(dataset):
    i = dataset[dataset['Salary'].isna()].index
    dataset = dataset.drop(i) ## dropping the records with missing values in salary column 
    dataset['Location'] = dataset['Location'].apply(lambda x: "United States" if pd.isnull(x) else x)
    return dataset