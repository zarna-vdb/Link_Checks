import requests
import pandas as pd
import io
import streamlit as st
from openpyxl import Workbook, load_workbook


def check_links(df, link_column, stock_column):
    invalid_links = []

    for index, row in df.iterrows():
        link = row[link_column]
        try:
            response = requests.get(link)
            st.write(f"Done : {index} ; Response Status : {response.status_code}")
            if response.status_code != 200:
                invalid_links.append({'Stock Number': row[stock_column], 'Link': link, 'code': response.status_code})
        except Exception as e:
            st.write(f"Error occurred while checking {link_column}-{index}-{link}: {e}")
            invalid_links.append({'Stock Number': row[stock_column], 'Link': link})

        # print("Done:", index)

    return pd.DataFrame(invalid_links)


def export_to_excel(df, excel_file_path, sheet_name):
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


def check (stock, link, data):
    m = data[[stock, link]]
    st.write(link)
    with st.container(height=300, border=True):
        checked = check_links(df = m, link_column = link, stock_column=stock)
    if not checked.empty:
        final = checked.dropna(subset=["Link"])
    # excel_file_path = file_name
    # sheet_name ="Invalid"
    # export_to_excel(final, excel_file_path, sheet_name)
    else:
        final = checked

    return final


def create_excel_file(dataframes, sheet_names):
    # Create a BytesIO buffer to save the Excel file in memory
    output = io.BytesIO()

    # Create a Pandas Excel writer using the buffer as the file
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for df, sheet in zip(dataframes, sheet_names):
            df.to_excel(writer, sheet_name=sheet, index=False)

    # Seek to the beginning of the stream
    output.seek(0)

    return output
