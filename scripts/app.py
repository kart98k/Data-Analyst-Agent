import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Sidebar API Key Input
with st.sidebar:
    
    api_key = st.text_input(
        "OPENAI_API_KEY",
        value="",
        type="password"
    )
    st.caption("😊 Built by Srikonda Karthik")
    st.caption("OpenAI • Pandas • Plotly • Streamlit")

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("📊 AI Data Analyst Dashboard")
st.caption("Upload any CSV file to generate charts + AI insights")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    st.subheader("📈 Auto Charts")

    # Numeric Charts
    for col in numeric_cols[:3]:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)

    # Categorical Charts
    for col in categorical_cols[:3]:
        top_data = df[col].value_counts().nlargest(10).reset_index()
        top_data.columns = [col, "Count"]

        fig = px.bar(
            top_data,
            x=col,
            y="Count",
            title=f"Top Categories in {col}"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Mixed Charts
    if numeric_cols and categorical_cols:
        cat = categorical_cols[0]
        num = numeric_cols[0]

        grouped = df.groupby(cat)[num].mean().reset_index().nlargest(10, num)

        fig = px.bar(
            grouped,
            x=cat,
            y=num,
            title=f"Average {num} by {cat}"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().round(2)

        fig = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.index),
            annotation_text=corr.values.astype(str),
            showscale=True
        )
        st.plotly_chart(fig, use_container_width=True)

    # AI Insights
    st.subheader("🤖 AI Insights")

    sample = df.head(30).to_csv(index=False)

    prompt = f"""
    Analyze this dataset sample and provide:
    1. Key trends
    2. Risks
    3. Opportunities
    4. Business recommendations

    Dataset:
    {sample}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    st.markdown(response.choices[0].message.content)