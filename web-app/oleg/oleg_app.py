import streamlit as st

st.title('Streamlit Application')

user_input = st.text_input("Enter some text")
st.write('You entered: ', user_input)
