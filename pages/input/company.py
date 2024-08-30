import streamlit as st
import datetime

#current_datetime = datetime.datetime.now()
timestamp = datetime.datetime.now(datetime.UTC).timestamp()
formatted_string = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
st.write("Timestamp:", timestamp)
st.write("Datetime:", formatted_string)