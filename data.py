import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📊 Universal Data Visualizer")

st.subheader("Choose how to load your data")
method = st.radio("Data Source:", ["Upload File", "Enter File Path"])

df = None

def read_file(file):
    if file.name.endswith('.csv') or file.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xlsx', '.xls')) or file.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)
    elif file.name.endswith('.json') or file.endswith('.json'):
        return pd.read_json(file)
    else:
        return None

if method == "Upload File":
    uploaded_file = st.file_uploader("Upload any structured file (CSV, Excel, JSON)", type=["csv", "xlsx", "xls", "json"])
    if uploaded_file is not None:
        try:
            df = read_file(uploaded_file)
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

elif method == "Enter File Path":
    file_path = st.text_input("Enter the full file path", value="C:/Users/marad/Downloads/datasets2/poll.csv")
    if os.path.exists(file_path):
        try:
            df = read_file(file_path)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.warning("❗ File not found. Please check the path.")

if df is not None:
    st.success("✅ File loaded successfully!")
    st.subheader("📋 Data Preview")
    st.dataframe(df)

    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if numeric_columns and categorical_columns:
        chart_type = st.selectbox("📈 Choose a chart type:", ["Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot"])

        x_axis = st.selectbox("X-axis (Categorical):", categorical_columns)
        y_axis = st.selectbox("Y-axis (Numeric):", numeric_columns)

        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, title="Bar Chart")
        elif chart_type == "Pie Chart":
            fig = px.pie(df, names=x_axis, values=y_axis, title="Pie Chart")
        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, title="Scatter Plot")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Need at least one categorical and one numeric column to visualize.")
else:
    st.info("📁 Please upload or enter a valid file path to begin.")
