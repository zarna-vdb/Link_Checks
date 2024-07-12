from Link_check_functions import *

st.set_page_config(layout="wide")

st.title("Links Validation")
st.divider()

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:
    with st.sidebar:
        excel_data = pd.ExcelFile(uploaded_file)
        sheet_names = excel_data.sheet_names
        selected_sheet = st.selectbox("Select a sheet", sheet_names, index=None)
    if selected_sheet:
        data = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        columns = list(data.columns)
        stock = st.selectbox("Select the stock column", options=columns, key="selectbox")

        available_options = [col for col in columns if col != stock]

        select_all_option = "Select All"
        available_options_with_select_all = [select_all_option] + available_options

        options = st.multiselect("Select Columns to Validate", options=available_options_with_select_all, key="multiselect")
        if select_all_option in options:
            options = available_options

        st.write(f"Columns Selected : {options}")
        val = st.button("Validate")
        if val:
            sheet_names = []
            checked_sheets = []
            for i in options:
                checked_data = check(stock, i, data)
                checked_sheets.append(checked_data)
                sheet_names.append(i)
                st.write(f"Number of invalid links in {i} : {len(checked_data)}")
                st.success(f"Validation for {i} is Done!")

            excel_file = create_excel_file(checked_sheets, sheet_names)
            st.download_button(
                label="Download Excel file",
                data=excel_file,
                file_name=f"{selected_sheet}_Invalid_Links.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
