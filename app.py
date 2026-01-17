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


st.divider()
st.subheader("🤖 AI Assistant (Ask About Your Properties)")

question = st.text_input(
    "Ask a question (e.g. 'How many flats are empty in Gurgaon?')"
)

if question:
    q = question.lower()

    # 1️⃣ Empty units
    if "empty" in q and "flat" in q:
        result = df[df["unit_status"] == "EMPTY"]
        st.success(f"There are {len(result)} empty units.")
        st.dataframe(
            result[["property_name", "city", "unit_number", "expected_rent"]],
            use_container_width=True
        )

    # 2️⃣ Total rent
    elif "total rent" in q or "monthly rent" in q:
        total_rent = df["rent_amount_paid"].fillna(0).sum()
        st.success(f"Your total monthly rent is ₹{int(total_rent)}")

    # 3️⃣ City-based query
    elif "gurgaon" in q:
        city_df = df[df["city"].str.lower() == "gurgaon"]
        st.success(f"You have {city_df['unit_id'].nunique()} units in Gurgaon.")
        st.dataframe(
            city_df[["property_name", "unit_number", "unit_status", "expected_rent"]],
            use_container_width=True
        )

    # 4️⃣ Investment properties
    elif "investment" in q:
        invest_df = df[df["saved_for_investment"] == "YES"]
        st.success("These properties are marked for investment:")
        st.dataframe(
            invest_df[
                ["property_name", "city", "investment_expected_roi", "investment_priority"]
            ].drop_duplicates(),
            use_container_width=True
        )

    else:
        st.warning(
            "I can answer questions about empty units, rent, city-wise data, and investments."
        )
        
             
import openai
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.divider()
st.subheader("🤖 AI Assistant (LLM Powered)")

user_question = st.text_area(
    "Ask anything about your properties:",
    placeholder="e.g. How much rent am I getting from Noida?"
)

if st.button("Ask AI") and user_question:

    with st.spinner("AI is thinking..."):
        # Prepare a safe data summary
        data_context = df.head(50).to_string(index=False)

        system_prompt = f"""
You are a helpful property management AI assistant.
Answer questions ONLY using the data provided.
If the answer is not in the data, say you don't know.

DATA:
{data_context}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
                ],
            temperature=0
            )
        
        answer = response.choices[0].message.content
        st.success(answer)


