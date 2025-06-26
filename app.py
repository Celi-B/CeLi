import streamlit as st
import pandas as pd

st.title("Payment Check App")

#Upload the excel file
uploaded_file = st.file_uploader ("Choose an excel file", type=["xlsx","xls"])

#if a file is uploaded
if uploaded_file is not None:
  try:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)

    # show the data
    st.subheader("Preview of your data")
    st.dataframe(df)

  except Esception as e:
    st.error(f"❌File Reading Error: {e}")

else:
  st.info("Please upload an excel file to get started.")


# st.write("Hello, the World only for me merely working on my own logic!")
# slider_value = st.slider("Pick your favorite number",0,100)
# st.write("Your favorite number is", slider_value)
