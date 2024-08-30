import streamlit as st

def update_keys():
    for k in st.session_state.key_list_product:
        st.session_state.key_list_product[k] = st.session_state[k]

if "key_list_product" not in st.session_state:
    st.session_state.key_list_product = {"name":"","vorname":"","email":""}

for k in st.session_state.key_list_product:
    #st.write(k, st.session_state.key_list_product[k])
    st.session_state[k] = st.session_state.key_list_product[k]
    #st.write( st.session_state[k])

with st.form("test_form"):
    nachname = st.text_input("Nachname", key="name")
    vorname = st.text_input("Vorname", key="vorname")
    mail = st.text_input("E-Mail Adresse", key="email")

    # Form submit button
    submit_button = st.form_submit_button(label='Weiter', on_click=update_keys)