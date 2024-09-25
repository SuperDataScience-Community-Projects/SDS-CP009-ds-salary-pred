#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
import re


# In[10]:


# Load the dataset
df = pd.read_csv('salaries.csv')


# In[11]:


df.shape


# In[28]:


# Function to clean the salary column and extract min and max salary values
def extract_salary_range(salary_str):
    # Use regex to find salary range in the format (e.g., "$68K - $94K")
    salary_range = re.findall(r'(\d+K)', salary_str)
    
    # If two values are found, assign min and max salary
    if len(salary_range) == 2:
        min_salary = int(salary_range[0].replace('K', '')) * 1000
        max_salary = int(salary_range[1].replace('K', '')) * 1000
        return (min_salary + max_salary) / 2  # Return the average salary
    return None

# Apply the function to the 'Salary' column and create a new column for average salary
df['Average Salary'] = df['Salary'].apply(extract_salary_range)


# In[30]:


# Now let's check for missing values in the new 'Average Salary' column

missing_salaries = df['Average Salary'].isnull().sum()

# Display the number of missing salaries

missing_salaries


# In[46]:


# Create an instance of SimpleImputer for numerical data
imputer_numeric = SimpleImputer(strategy='mean')

# Apply it to the 'Company Score' (numerical column) to fill missing values with the mean
df[['Company Score']] = imputer_numeric.fit_transform(df[['Company Score']])

# For categorical columns (like 'Company', 'Location'), use the most frequent value to fill missing data
imputer_categorical = SimpleImputer(strategy='most_frequent')

# Apply it to the 'Company' and 'Location' columns
df[['Company', 'Location']] = imputer_categorical.fit_transform(df[['Company', 'Location']])


# Create an instance of SimpleImputer for numerical data (strategy = median)
imputer = SimpleImputer(strategy='median')

# Apply it to the 'Average Salary' column to fill missing values with the median
df[['Average Salary']] = imputer.fit_transform(df[['Average Salary']])

# Check for any remaining missing values in the dataset
df.isnull().sum()




# In[47]:


df.head()


# In[59]:


# the 'Salary' column has been drop now that min and max salaries are extracted
df2 = df.drop(columns=['Salary'])

# show the new data without the Salary column
df2.head(20)


# In[60]:


mv=df2.isnull().sum()
mv


# In[61]:


df2 = df2.drop_duplicates()


# In[62]:


df2.to_csv('IT salaries_cleaned new.csv', index=False)


# In[67]:


df3=pd.read_csv('IT salaries_cleaned new.csv')


# In[70]:


# X: All columns except the last one (Average Salary)
X = df3.iloc[:, :-1].values  

# y: The last column (Average Salary)
y = df3.iloc[:, -1].values

print("Independent Variables (X):")
print(X)


# In[71]:


print (y)


# In[ ]:




