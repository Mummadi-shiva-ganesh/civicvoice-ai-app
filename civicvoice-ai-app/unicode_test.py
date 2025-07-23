import streamlit as st

st.title("Unicode Input Test")
text = st.text_area("Paste Telugu or any Indian language text here:")
st.write("You entered:", text) 