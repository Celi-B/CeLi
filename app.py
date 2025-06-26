import streamlit as st

st.title("My Second Streamlit App")
st.write("Hello, the World only for me merely working on my own logic!")
slider_value = st.slider("Pick your favorite number",0,100)
st.write("Your favorite number is", slider_value)
