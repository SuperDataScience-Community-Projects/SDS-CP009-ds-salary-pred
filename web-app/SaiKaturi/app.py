# app.py
import streamlit as st
import pandas as pd
import os
from Scripts.utils import load_data
from Scripts.datacleaning import clean_data,check_null_values,datacleaningnofile
from Scripts.datapreprocessing import datapreprocessing,dataprocessingnofile
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
    
    st.dataframe(cleaned_data.head())

    # Check null values
    st.write("Checking Null values after cleaning the data")
    null_values = check_null_values(cleaned_data)
    st.dataframe(null_values)
    
    #Preprocessing the data
    processed_data = datapreprocessing(cleaned_data)
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
    
else :
    #Data Cleaning
    st.write("Processed data")
    cleaned_data = datacleaningnofile()
    st.dataframe(cleaned_data.head())

    #Data preprocessing
    st.write("Processed data")
    processed_data = dataprocessingnofile()
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