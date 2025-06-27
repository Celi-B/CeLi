import streamlit as st
import pandas as pd

st.title("Payment Check App")

#Upload the excel file
uploaded_file = st.file_uploader ("Choose an excel file", type=["xlsx","xls"])

#if a file is uploaded
if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file, engine='openpyxl', header=1)

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
            st.subheader("Filter Options")

            # Get all unique values for filters (unfiltered)
            all_suppliers = df['Supplier'].dropna().unique()
            all_categories = df['Spend Category'].dropna().unique()

            selected_suppliers = st.multiselect("Filter by Supplier (optional)", options=all_suppliers)
            selected_categories = st.multiselect("Filter by Spend Category (optional)", options=all_categories)

            # Start with full dataframe
            filtered_df = df

            # Apply filters independently
            if selected_suppliers:
                filtered_df = filtered_df[filtered_df['Supplier'].isin(selected_suppliers)]

            if selected_categories:
                filtered_df = filtered_df[filtered_df['Spend Category'].isin(selected_categories)]

            st.subheader("Filtered Data")
            st.dataframe(filtered_df[available_columns])
        else:
            st.warning("None of the selected columns were found in the uploaded file.")


    except Exception as e:
        st.error(f"❌File Reading Error: {e}")


