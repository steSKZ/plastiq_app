import streamlit as st

page_input_contact = st.Page("pages/input/contact.py", title="Kontakt", icon=":material/contacts:")
page_input_company = st.Page("pages/input/company.py", title="Unternehmen", icon=":material/apartment:")
page_input_product = st.Page("pages/input/product.py", title="Abfalldaten", icon=":material/add_circle:")
page_output_score = st.Page("pages/output/score.py", title="Passende Verwertung", icon=":material/all_match:")
page_output_recyler = st.Page("pages/output/recycler.py", title="Passende Abnehmer", icon=":material/pin_drop:")

pg = st.navigation(
    {
        "Datenaufnahme": [page_input_contact, page_input_company, page_input_product],
        "Ergebnisse": [page_output_score, page_output_recyler],
    }
)

pg.run()