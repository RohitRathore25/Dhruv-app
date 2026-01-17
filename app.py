import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Rai Properties",
    layout="wide"
)

st.title("🏢 Rai Properties")

@st.cache_data
def load_data():
    return pd.read_csv("Rai_Properties_Dataset.csv")

df = load_data()

st.success("Data loaded successfully")
st.write("Preview of data:")
st.dataframe(df.head(), use_container_width=True)


st.set_page_config(
    page_title="Rai Properties",
    layout="wide"
)

st.title("🏢 Rai Properties Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("Rai_Properties_Dataset.csv")

df = load_data()

st.success("Data loaded successfully")


# Dashboard

total_properties = df["property_id"].nunique()
total_units = df["unit_id"].nunique()

occupied_units = df[df["unit_status"] == "OCCUPIED"]["unit_id"].nunique()
empty_units = df[df["unit_status"] == "EMPTY"]["unit_id"].nunique()

monthly_rent = df["rent_amount_paid"].fillna(0).sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Properties", total_properties)
col2.metric("Total Units", total_units)
col3.metric("Occupied Units", occupied_units)
col4.metric("Empty Units", empty_units)
col5.metric("Monthly Rent (₹)", int(monthly_rent))

st.divider()



