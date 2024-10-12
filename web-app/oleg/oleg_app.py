import joblib
import pandas as pd
import streamlit as st

# @st.cache_data
# def load_model():
#     file_path = "Support_Vector_Regressor_model.pkl"
#     try:
#         loaded_model = joblib.load(file_path)
#         return(loaded_model)
#     except FileNotFoundError:
#         print(f"Error: The file '{file_path}' was not found.")
#         return None   
#     except IOError:
#         print(f"Error: An error occurred while trying to read the file '{file_path}'.")
#         return None 
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None
    

def load_data(file_path: str):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def predict( company_value, location_value, job_value) -> float:
# --
    file_path = "Support_Vector_Regressor_model.pkl"
    try:
        model = joblib.load(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")  
    except IOError:
        print(f"Error: An error occurred while trying to read the file '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# --
    # model = load_model()
    input_df=pd.DataFrame([[company_value, location_value, job_value]], columns=['Company_Code', 'Location_Code', 'Job_Code'])
    avg_salary_predicted = model.predict(input_df)
    return avg_salary_predicted


# App execution
def app():
    #initialise page
    st.set_page_config(
            page_title='Salary Prediction',
            page_icon='💸', 
            layout='wide'
            )
    #load data
     
    # web-app/oleg/companies.csv
    # /workspaces/SDS-009-ds-salary-pred/web-app/oleg/companies.csv

    location_df = load_data('web-app/oleg/locations.csv')
    job_df = load_data('web-app/oleg/jobs.csv')
    company_df = load_data('web-app/oleg/companies.csv')
   
    avg_salary_predicted=0
    
    with st.sidebar:
       #Location
        location_name = st.selectbox('Location :', location_df['Location'].unique())
        # Retrieve the corresponding value
        location_value = location_df[location_df['Location'] == location_name]['Location_Code'].values[0]
        
       #Job
        job_name = st.selectbox('Job :', job_df['Job Category'].unique())
        # Retrieve the corresponding value
        job_value = job_df[job_df['Job Category'] == job_name]['Job_Code'].values[0]
    
       #Company
        company_name = st.selectbox('Company :', company_df['Company'].unique())
        # Retrieve the corresponding value
        company_value = company_df[company_df['Company'] == company_name]['Company_Code'].values[0]
    
        if st.button("Predict"): 
            avg_salary_predicted = predict(company_value, location_value, job_value)
    
    st.write(avg_salary_predicted)

#run application 
if __name__ == "__main__":
    app()
