import joblib
import pandas as pd
import streamlit as st
from sklearn.svm import SVR

from geopy.geocoders import Nominatim
import pydeck as pdk

import matplotlib.pyplot as plt

@st.cache_data
def load_model() -> SVR:
    file_path = 'web-app/oleg/Support_Vector_Regressor_model.pkl'
    
    try:
        loaded_model = SVR()
        loaded_model = joblib.load(file_path)
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
    model = SVR()
    model = load_model()
    input_df=pd.DataFrame([[company_value, location_value, job_value]], columns=['Company_Code', 'Location_Code', 'Job_Code'])
    avg_salary_predicted = model.predict(input_df)[0]
    return avg_salary_predicted

def predict_all_jobs(company_value, location_value, jobs_df) -> pd.DataFrame:
    model = SVR()
    model = load_model()
    input_df = pd.DataFrame(columns=['Company_Code', 'Location_Code', 'Job_Code'])
    input_df['Job_Code']=jobs_df['Job_Code']
    input_df['Company_Code'] = company_value
    input_df['Location_Code'] = location_value
 
    output_df = pd.DataFrame(columns=['Company_Code', 'Location_Code', 'Job_Code','Job','Avg'])
    output_df = input_df
    output_df['Avg'] = model.predict(input_df)
    output_df.loc[output_df['Job_Code'].isin(jobs_df['Job_Code']),'Job']=jobs_df.set_index('Job_Code')['Job Category']
    
    output_df.drop(columns=['Job_Code', 'Company_Code','Location_Code'], inplace=True)

    return output_df


# App execution
def app():
    #initialise page
    st.set_page_config(
            page_title='Salary Prediction',
            page_icon='💸', 
            layout='wide'
            )

    location_df = load_data('web-app/oleg/locations.csv')
    job_df = load_data('web-app/oleg/jobs.csv')
    company_df = load_data('web-app/oleg/companies.csv')
   
    avg_salary_predicted=0
    update = False

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
            avg_salaries_predicted = predict_all_jobs(company_value, location_value, job_df)
            update = True
    
    if update:
        # Initialize the Nominatim geocoder
        geolocator = Nominatim(user_agent="city_locator")
        location = geolocator.geocode(location_name)
        # Create a map centered on the city's location
        city_location = pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=location.latitude,
                longitude=location.longitude,
                zoom=10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=[{"lat": location.latitude, "lon": location.longitude}],
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=1000,
                ),
            ],
        )
        
        # Show the map
        st.pydeck_chart(city_location)
        st.dataframe(avg_salaries_predicted)

# /////<BEGIN>
# Create the plot
        x = avg_salaries_predicted['Job']
        # y = avg_salaries_predicted['Avg'] 

        fig, ax = plt.subplots()
        ax.hist(x, bins=len(x), color='g', edgecolor='black')
        # ax.plot(x, y, marker='o', linestyle='-', color='b')
        ax.set_title('Salaries by job')
        ax.set_xlabel('Job')
        ax.set_ylabel('Salary ,K $ ')
        ax.tick_params(axis='x', labelrotation=90)
        # ax.set_xticks(x) 
        # ax.set_yticks(range(1, len(avg_salaries_predicted['Job']) + 1))  # Set y-ticks to be the values in Job
        # ax.set_yticklabels(avg_salaries_predicted['Avg'])  # Set y-tick labels to actual Job values
        # ax.grid()

        # Display the plot in Streamlit
        st.pyplot(fig)
# /////<END>
        st.write(f'Average Salary for the position of {job_name} at {company_name} company in the {location_name} area is {avg_salary_predicted:.2f}K anually')
    else:
        st.write('')

#run application 
if __name__ == "__main__":
    app()
