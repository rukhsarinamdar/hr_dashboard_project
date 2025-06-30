import pandas as pd
import psycopg2
import streamlit as st

# Streamlit page config
st.set_page_config(page_title="HR Dashboard", layout="wide")

# Database connection
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='199211',  # ✅ Corrected password format
    host='localhost',
    port='5432'
)

# Query the view
df = pd.read_sql("SELECT * FROM vw_active_employees", conn)

# Preprocess date
df['hire_date'] = pd.to_datetime(df['hire_date'])

# Title
st.title("👥 HR Dashboard - Active Employees")

# KPI Summary
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", len(df))
col2.metric("Departments", df['department_name'].nunique())
col3.metric("Job Titles", df['job_title'].nunique())

st.markdown("---")

# Filters
st.subheader("🔍 Filters")
departments = df['department_name'].unique()
selected_dept = st.selectbox("Select Department", options=["All"] + sorted(departments.tolist()))

if selected_dept != "All":
    filtered_df = df[df['department_name'] == selected_dept]
else:
    filtered_df = df

# Show filtered data
st.dataframe(filtered_df)

# Department-wise Chart
st.subheader("📊 Department-wise Active Employee Count")
dept_count = df['department_name'].value_counts().reset_index()
dept_count.columns = ['Department', 'Number of Employees']
st.bar_chart(dept_count.set_index('Department'))

# Hires Over Time
st.subheader("📈 Hiring Trend Over Time")
hires_by_month = df.groupby(df['hire_date'].dt.to_period('M')).size()
hires_by_month.index = hires_by_month.index.astype(str)  # Fix PeriodIndex
st.line_chart(hires_by_month)

# Download Button
st.subheader("⬇️ Download Data")
st.download_button("Download CSV", filtered_df.to_csv(index=False), "active_employees.csv", "text/csv")

# Close DB connection
conn.close()