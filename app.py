import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Bank Customer Churn Analysis",
    page_icon="🏦",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank.csv")
    return df

df = load_data()

# Title
st.title("🏦 Bank Customer Churn Analysis Dashboard")
st.markdown("**Analyst: Ankita Das | Unified Mentor Internship Project**")
st.markdown("---")

# SECTION 1 - Overview
st.header("📊 Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", "10,000")
with col2:
    st.metric("Churned Customers", "2,037")
with col3:
    st.metric("Churn Rate", "20.37%")

st.markdown("---")

# SECTION 2 - Churn by Geography
st.header("🌍 Churn by Country")
geo = df.groupby("Geography")["Exited"].agg(["sum", "count"]).reset_index()
geo.columns = ["Country", "Churned", "Total"]
geo["Churn Rate %"] = round(geo["Churned"] * 100 / geo["Total"], 2)
st.bar_chart(geo.set_index("Country")["Churn Rate %"])
st.dataframe(geo)

st.markdown("---")

# SECTION 3 - Churn by Gender
st.header("👫 Churn by Gender")
gen = df.groupby("Gender")["Exited"].agg(["sum", "count"]).reset_index()
gen.columns = ["Gender", "Churned", "Total"]
gen["Churn Rate %"] = round(gen["Churned"] * 100 / gen["Total"], 2)
st.bar_chart(gen.set_index("Gender")["Churn Rate %"])
st.dataframe(gen)

st.markdown("---")

# SECTION 4 - Churn by Age Group
st.header("👴 Churn by Age Group")
df["Age_Group"] = pd.cut(df["Age"],
                          bins=[0, 30, 45, 100],
                          labels=["Young", "Middle", "Senior"])
age = df.groupby("Age_Group", observed=True)["Exited"].agg(["sum", "count"]).reset_index()
age.columns = ["Age Group", "Churned", "Total"]
age["Churn Rate %"] = round(age["Churned"] * 100 / age["Total"], 2)
st.bar_chart(age.set_index("Age Group")["Churn Rate %"])
st.dataframe(age)

st.markdown("---")

# SECTION 5 - Churn by Number of Products
st.header("📦 Churn by Number of Products")
prod = df.groupby("NumOfProducts")["Exited"].agg(["sum", "count"]).reset_index()
prod.columns = ["Products", "Churned", "Total"]
prod["Churn Rate %"] = round(prod["Churned"] * 100 / prod["Total"], 2)
st.bar_chart(prod.set_index("Products")["Churn Rate %"])
st.dataframe(prod)

st.markdown("---")

# SECTION 6 - Active vs Inactive
st.header("😴 Active vs Inactive Members")
active = df.groupby("IsActiveMember")["Exited"].agg(["sum", "count"]).reset_index()
active["Status"] = active["IsActiveMember"].map({1: "Active", 0: "Inactive"})
active.columns = ["IsActiveMember", "Churned", "Total", "Status"]
active["Churn Rate %"] = round(active["Churned"] * 100 / active["Total"], 2)
st.bar_chart(active.set_index("Status")["Churn Rate %"])
st.dataframe(active[["Status", "Churned", "Total", "Churn Rate %"]])

st.markdown("---")

# SECTION 7 - Risk Score Distribution
st.header("🎯 Churn Risk Score Distribution")

def calculate_risk(row):
    score = 0
    if row["Age"] > 45: score += 30
    if row["IsActiveMember"] == 0: score += 25
    if row["NumOfProducts"] >= 3: score += 20
    if row["Geography"] == "Germany": score += 15
    if row["Balance"] == 0: score += 10
    if row["Gender"] == "Female": score += 10
    if row["CreditScore"] < 500: score += 10
    return score

df["Risk_Score"] = df.apply(calculate_risk, axis=1)
df["Risk_Category"] = df["Risk_Score"].apply(
    lambda x: "High Risk" if x > 60 else ("Medium Risk" if x > 30 else "Low Risk")
)

risk = df["Risk_Category"].value_counts().reset_index()
risk.columns = ["Risk Category", "Count"]
st.bar_chart(risk.set_index("Risk Category")["Count"])
st.dataframe(risk)

st.markdown("---")

# SECTION 8 - Risk Calculator
st.header("🧮 Customer Churn Risk Calculator")
st.markdown("Enter customer details to calculate churn risk:")

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Age", 18, 92, 40)
    geography = st.selectbox("Country", ["France", "Spain", "Germany"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    credit_score = st.slider("Credit Score", 350, 850, 650)

with col2:
    is_active = st.selectbox("Is Active Member?", ["Yes", "No"])
    num_products = st.slider("Number of Products", 1, 4, 1)
    balance = st.number_input("Account Balance", 0, 300000, 50000)

score = 0
if age > 45: score += 30
if is_active == "No": score += 25
if num_products >= 3: score += 20
if geography == "Germany": score += 15
if balance == 0: score += 10
if gender == "Female": score += 10
if credit_score < 500: score += 10

st.markdown(f"### Current Risk Score: {score}")

if score <= 30:
    st.success(f"✅ Risk Score: {score} — LOW RISK")
elif score <= 60:
    st.warning(f"⚠️ Risk Score: {score} — MEDIUM RISK")
else:
    st.error(f"🔴 Risk Score: {score} — HIGH RISK")

st.markdown("---")
st.markdown("*Dashboard built by Ankita Das | Unified Mentor Internship | Bank Customer Churn Analysis Project*")