import streamlit as st
import pandas as pd
import OS

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

               #key_columns의 모든 항목이 new_df.columns 안에 다 들어 있느냐?
        if not set(key_columns).issubset(new_df.columns): #key_columns에 있는 모든 컬럼들이 new_df.columns에 포함되지 않았다면
            st.error("❌ there is no enough columns for duplication check 중복체크를 위한 필수 컬럼이 부족합니다.")


        
        else:
            #기존 데이터 불러오기 (없으면 빈 DF)
            if os.path.exists(DATA_FILE):
                old_df = pd.read_csv(DATA_FILE)
            else:
                old_df = pd.DataFrame(columns=new_df.columns)


            # 비교 대상 키 만들기
            new_df['__merge_key__'] = new_df[key_columns].astype(str).agg('|'.join, axis=1)
            old_df['__merge_key__'] = old_df[key_columns].astype(str).agg('|'.join, axis=1)

            #새로운 행만 필터링
            filtered_new_df = new_df[~new_df['__merge_key__'].isin(old_df['__merge_key__'])].copy()

            # 병합 후 저장
            updated_df = pd.concat([old_df.drop(columns='__merge_key__'), filtered_new_df.drop(columns='__merge_key__')], ignore_index=True)
            updated_df.to_csv(DATA_FILE, index=False)

            st.success(f"✅ {len(filtered_new_df)}개의 새로운 행이 저장되었습니다.")
            st.subheader("Newly Added Data")
            st.dataframe(filtered_new_df)

        
        # check that the selected columns exist in the file
        available_columns = [col for col in important_columns if col in df.columns]

    
        if available_columns:
            st.subheader("Filter Options")

            # Get all unique values for filters (unfiltered)
            all_suppliers = sorted(df['Supplier'].dropna().unique())
            all_categories = sorted(df['Spend Category'].dropna().unique())

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


