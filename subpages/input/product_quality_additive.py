import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import datetime

## Basic variables
# Save data to excel file
file_path = "content/plastiq_input_information.xlsx"
df_header = "Zusätze"

## Functions
# Function to update dict with session state keys after every submission of form
def update_keys():
    for k in st.session_state.key_dict_additive_quality:
        st.session_state.key_dict_additive_quality[k] = st.session_state[k]

# Function to collect product quality data
def collect_additive_quality(additiv_typ, fuellstoff_typ):
    with st.form(key="waste_additive_form"):
    
        values_additiv_typ = []
        values_additiv_anteil = []
        values_fuellstoff_typ = []
        values_fuellstoff_anteil = []

        # Additional variables for the DataFrame
        id_product = 1 #to be specified
        timestamp = datetime.datetime.now().timestamp()
        utc_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # Form submit button
        submit_button_additive_quality = st.form_submit_button(label='Speichern', on_click=update_keys)

        # Store the data in a DataFrame if the form is submitted
        if submit_button_additive_quality:

            additive_quality = {
                "ID_Wertstoff": [id_product],
                "Zeit_UTC": [utc_time],
                "Additive": [values_additiv_typ],
                #"Additivanteil": [values_additiv_anteil],
                "Füllstoffe": [values_fuellstoff_typ],
                #"Füllstoffanteil": [values_fuellstoff_anteil]
            }

            product_df = pd.DataFrame(additive_quality)
            return product_df
    return None

# Function to show dataframe
def show_dataframe(header, df):
    st.write(header)
    st.dataframe(df)

# Function to append data to an existing Excel file
def append_df_to_excel(file_path, df, sheet_name='additive_quality', startrow=None, **to_excel_kwargs):
    try:
        # Try to open an existing workbook
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Get the last row in the existing Excel sheet if startrow is not defined
            if startrow is None:
                writer.workbook = load_workbook(file_path)
                if sheet_name in writer.workbook.sheetnames:
                    startrow = writer.workbook[sheet_name].max_row
                else:
                    startrow = 0

            # Write out the new data below the existing data
            df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False, header=False, **to_excel_kwargs)

    except FileNotFoundError:
        # If the file does not exist, create it with the DataFrame
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, **to_excel_kwargs)

# Initialize keys for product input form if not available 
if "key_dict_product_quality_additive" not in st.session_state:
    st.session_state.key_dict_product_quality_additive = {"input_additiv_typ":None,
                                                "input_additiv_anteil":0,
                                                "input_fuellstoff_typ":None,
                                                "input_fuellstoff_anteil":0,
                                                }
    
# For loop: Create session state key for every key in key_dict_product
for k in st.session_state.key_dict_additive_quality:
    st.session_state[k] = st.session_state.key_dict_additive_quality[k]

# Streamlit app
st.title("Wertstoffdaten")
st.header("Additive und Füllstoffe", divider="red", help="Bitte gebe die Informationen zum Anteil der Additive und Füllstoffe in den Materialien an.")

# Collect product quality data using the function
value_fraction = st.session_state.key_dict_product["input_waste_fraction_number"]
values_additiv_typ = []
values_fuellstoff_typ = []

# Collect all additive and filler information in separate lists
for i in range(value_fraction):
    values_additiv_typ.append(st.session_state.key_dict_product[f"input_additiv_typ_{i}"])
    values_fuellstoff_typ.append(st.session_state.key_dict_product[f"input_fuellstoff_typ_{i}"])

product_df = collect_additive_quality(values_additiv_typ, values_fuellstoff_typ)

# Display the dataframe if not None
if product_df is not None:

    # Append the DataFrame to the existing Excel file
    append_df_to_excel(file_path, product_df)
    show_dataframe (df_header, product_df)

# Display buttons to switch between input pages
left_column_bottom, right_column_bottom = st.columns([.13,1])
button_back = left_column_bottom.button("Zurück")
if button_back:
    st.switch_page("subpages/input/product_quality.py")
button_next = right_column_bottom.button("Weiter")
if button_next:
    st.switch_page("subpages/input/product_further.py")