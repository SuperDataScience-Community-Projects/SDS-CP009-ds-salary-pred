import pickle
import streamlit as st

@st.cache_data
def load_model():
    file_path = 'Support Vector Regressor_model.pkl'
    try:
        with open(file_path, 'rb') as file:
           loaded_model = pickle.load(file)
        return(loaded_model)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError:
        print(f"Error: An error occurred while trying to read the file '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# @st.cache_resource
# def load_companies():

# @st.cache_resource
# def load_jobs():

# @st.cache_resource
# def load_locations();    

@st.cache_resource
def init_page():
    st.set_page_config(
        page_title='Salary Prediction',
        page_icon='💸', 
        layout='wide'
        )
        


# execution

#initialise page
init_page()

model = load_model()

with st.sidebar:
    st.selectbox('Location', [1,2,3])
    st.selectbox('Job', [1,2,3])
    st.selectbox('Company', [1,2,3])




