import streamlit as st 
import streamlit.components.v1 as stc 
from eda_app import run_eda_app
from ml_app import run_ml_app

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">IT professional  Data App </h1>
		<h4 style="color:white;text-align:center;">Salary </h4>
		</div>
		"""

def main():
	# st.title("IT Salary Prediction")
	stc.html(html_temp)

	menu = ["Home","EDA","ML","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		st.write("""
			### IT salary Prediction
			
			#### App Content
				- EDA Section: Exploratory Data Analysis of Data
				- ML Section: ML Predictor App

			""")
	elif choice == "EDA":
		run_eda_app()
	elif choice == "ML":
		run_ml_app()
	else:
		st.subheader("About")
		st.text("SuperDataScience")
		st.text("Salary Prediction")
		st.text("By Paul Alemoh")

if __name__ == '__main__':
	main()