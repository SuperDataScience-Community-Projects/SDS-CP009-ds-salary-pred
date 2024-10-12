import pickle
import pandas as pd
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
        return None   
    except IOError:
        print(f"Error: An error occurred while trying to read the file '{file_path}'.")
        return None 
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

def load_data(file_path):
    try:
        df = pd.read_csv(file_path,'rb')
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


# App execution
def app():
    #initialise page
    st.set_page_config(
            page_title='Salary Prediction',
            page_icon='💸', 
            layout='wide'
            )
    #load data
    model = load_model()
    location_df = load_data('locations.csv')
    job_df = load_data('jobs.csv')
    company_df = load_data('companies.csv')

   
    
    # with st.sidebar:
        #Location
        # location_name = st.selectbox('Location :', location_df['Location'])
        # Retrieve the corresponding value
        # location_value = location_df[location_df['Location'] == location_name]['Location_Code'].values[0]
            


        #job

        #company

        # st.selectbox('Location', ["A1",2,3])
        # st.selectbox('Job', [1,2,3])
        # st.selectbox('Company', [1,2,3])

    # st.write = location_value

#run application 
if __name__ == "__main__":
    app()
