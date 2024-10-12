# app.py
import streamlit as st
import pandas as pd
import os
from Scripts.utils import load_data
from Scripts.datacleaning import clean_data,check_null_values
from Scripts.datapreprocessing import datapreprocessing
from Scripts.datavisualization import plot_data
from Scripts.model import load_model, predict

# Title
st.title('IT Salary Prediction')

# Sidebar for user inputs
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = load_data(uploaded_file)
    
    # Display raw data
    st.write("Raw Data")
    st.dataframe(df.head())
    # Check null values
    st.write("Checking Null values before cleaning data")
    null_values = check_null_values(df)
    st.dataframe(null_values)
    
    # Clean data
    cleaned_data = clean_data(df)
    st.write("Cleaned Data")
    cleaned_data.to_csv("Data/Cleaned/cleaned_data.csv")
    st.dataframe(cleaned_data.head())

    # Check null values
    st.write("Checking Null values after cleaning the data")
    null_values = check_null_values(cleaned_data)
    st.dataframe(null_values)
    
    #Preprocessing the data
    processed_data = datapreprocessing(cleaned_data)
    st.write("Preprocessed data")
    processed_data.to_csv("Data/Processed/Processed_data.csv")
    st.dataframe(processed_data.head())

    #Data Visualization
    st.write("Data Visualization")
    plot_data(processed_data)
    image_folder = 'Images/'
    # Get a list of all files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    # Display each image in the folder
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        st.image(image_path, caption=image_file)
    ''' 
    # Model Prediction
    model = load_model()
    if st.button('Predict'):
        predictions = predict(model, cleaned_data)
        st.write("Predictions")
        st.write(predictions)
'''
else:
    cleaned_data = pd.read_csv('Data/Cleaned/Cleaned_data.csv')
    st.write("Cleaned data")
    st.dataframe(cleaned_data.head())


    processed_data = pd.read_csv('Data/Processed/Processed_data.csv')

    st.write("Preprocessed data")
    st.dataframe(processed_data.head())

    #Data Visualization
    st.write("Data Visualization")
    plot_data(processed_data)
    image_folder = 'Images/'
    # Get a list of all files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    # Display each image in the folder
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        st.image(image_path, caption=image_file)
