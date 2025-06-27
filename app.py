import streamlit as st
import pandas as pd

st.title("Payment Check App")

#Upload the excel file
uploaded_file = st.file_uploader ("Choose an excel file", type=["xlsx","xls"])

#if a file is uploaded
if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # set the columns I want to display
        important_columns = [
            'Project', 
            'Supplier', 
            "Supplier's Invoice Number",
            'Invoice Date', 
            'Invoice Status', 
            'Spend Category', 
            'Total Invoice Amount (reporting currency)', 
            'Line Tax Amount', 
            'Line Extended Amount', 
            'Currency', 
            'Document Payment Status', 
            'Payment Date'
        ]

        # check that the selected columns exist in the file
        available_columns = [col for col in important_columns if col in df.columns]

    
        if available_columns:
            st.subheader("selected important columns")
            st.dataframe(df[available_columns])
        else:
            st.warning("None of the selected columns were found in the uploaded file.")


    except Exception as e:
        st.error(f"❌File Reading Error: {e}")


