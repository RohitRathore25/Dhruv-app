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

st.success("Data loaded successfully ✅")
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

st.subheader("🔍 Search & Filter Properties")

col1, col2, col3 = st.columns(3)

city_filter = col1.selectbox(
    "Select City",
    ["All"] + sorted(df["city"].dropna().unique().tolist())
)

status_filter = col2.selectbox(
    "Unit Status",
    ["All", "OCCUPIED", "EMPTY"]
)

tenant_type_filter = col3.selectbox(
    "Tenant Type",
    ["All"] + sorted(df["tenant_type"].dropna().unique().tolist())
)

filtered_df = df.copy()

if city_filter != "All":
    filtered_df = filtered_df[filtered_df["city"] == city_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["unit_status"] == status_filter]

if tenant_type_filter != "All":
    filtered_df = filtered_df[filtered_df["tenant_type"] == tenant_type_filter]

st.dataframe(
    filtered_df[
        [
            "property_name",
            "city",
            "unit_number",
            "rooms",
            "unit_status",
            "expected_rent",
            "tenant_name"
        ]
    ],
    use_container_width=True
)


st.divider()
st.subheader("🏠 Property Detail View")

selected_property = st.selectbox(
    "Select a Property",
    sorted(df["property_name"].unique())
)

property_df = df[df["property_name"] == selected_property]

# Property summary
st.write("### Property Summary")

summary_cols = [
    "property_name",
    "location",
    "city",
    "area_sqft",
    "usage_type",
    "property_status",
    "year_acquired"
]

st.dataframe(
    property_df[summary_cols].drop_duplicates(),
    use_container_width=True
)

# Units under property
st.write("### Units in this Property")

units_cols = [
    "unit_number",
    "floor",
    "rooms",
    "unit_status",
    "expected_rent",
    "tenant_name",
    "tenant_occupation"
]

st.dataframe(
    property_df[units_cols],
    use_container_width=True
)


