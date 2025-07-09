import streamlit as st
import pandas as pd
import os

st.title("Payment Check App")

# 저장할 파일 이름
DATA_FILE = "stored_data.csv"

#Upload the excel file
uploaded_file = st.file_uploader ("Choose an excel file", type=["xlsx","xls"])

#if a file is uploaded
if uploaded_file is not None:
    try:
        # Read the Excel file
        new_df = pd.read_excel(uploaded_file, engine='openpyxl', header=1) #업로드된 엑셀 파일에서 실제로 가져온 컬럼 이름들입니다

        # set the columns I want to display
        key_columns = [
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

        # 실제 존재하는 키 컬럼만 추출
        existing_keys = [col for col in key_columns if col in new_df.columns]
        missing_keys = list(set(key_columns) - set(existing_keys))

        if missing_keys:
            st.warning(f"⚠️ 병합을 위한 컬럼 중 누락된 항목: {', '.join(missing_keys)}")

        if not existing_keys:
            st.error("❌ 병합 할 수 있는 컬럼이 없습니다.")
            st.stop()

        # 병합 키 생성
        new_df['__merge_key__'] = new_df[existing_keys].astype(str).agg('|'.join, axis=1)

        # 기존 데이터 처리
        if os.path.exists(DATA_FILE):
            old_df = pd.read_csv(DATA_FILE)
            existing_keys_old = [col for col in existing_keys if col in old_df.columns]
            if existing_keys_old:
                old_df['__merge_key__'] = old_df[existing_keys_old].astype(str).agg('|'.join, axis=1)
            else:
                old_df['__merge_key__'] = ''
        else:
            old_df = pd.DataFrame(columns=new_df.columns)
            old_df['__merge_key__'] = ''


        #새로운 행만 필터링
        filtered_new_df = new_df[~new_df['__merge_key__'].isin(old_df['__merge_key__'])].copy()

        # 병합 후 저장
        updated_df = pd.concat(
            [old_df.drop(columns='__merge_key__'), filtered_new_df.drop(columns='__merge_key__')], 
            ignore_index=True
        )
        updated_df.to_csv(DATA_FILE, index=False)

        st.success(f"✅ {len(filtered_new_df)}개의 새로운 행이 저장되었습니다.")
        st.subheader("Newly Added Data")
        st.dataframe(filtered_new_df)

        
        # check that the selected columns exist in the file
        available_columns = [col for col in key_columns if col in new_df.columns]

    
        if available_columns:
            st.subheader("Filter Options")

            # Get all unique values for filters (unfiltered)
            all_suppliers = sorted(new_df['Supplier'].dropna().unique())
            all_categories = sorted(new_df['Document Payment Status'].dropna().unique())

            selected_suppliers = st.multiselect("Filter by Supplier (optional)", options=all_suppliers)
            selected_categories = st.multiselect("Filter by Document Payment Status (optional)", options=all_Document Payment Status)

            # Start with full dataframe
            filtered_df = new_df.copy()

            # Apply filters independently
            if selected_suppliers:
                filtered_df = filtered_df[filtered_df['Supplier'].isin(selected_suppliers)]

            if selected_categories:
               filtered_df = filtered_df[filtered_df['Document Payment Status'].isin(selected_Document Payment Status)]

            st.subheader("Filtered Data")
            st.dataframe(filtered_df[available_columns])
        else:
            st.warning("None of the selected columns were found in the uploaded file.")


    except Exception as e:
        st.error(f"❌File Reading Error: {e}")


