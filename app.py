import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Rai Properties Prototype",
    layout="wide"
)

st.title("🏢 Rai Properties – Prototype")

@st.cache_data
def load_data():
    return pd.read_csv("D:\Sagarpur Project\Rai_Properties_Dataset.csv")

df = load_data()

st.success("Data loaded successfully ✅")
st.write("Preview of data:")
st.dataframe(df.head(), use_container_width=True)