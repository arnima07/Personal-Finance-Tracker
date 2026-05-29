import streamlit as st
import pandas as pd
import os
import plotly.express as px


st.set_page_config(page_title="Personal Finance Tracker",page_icon="💸",layout="wide")

# FILE SETUP 

FILE_NAME = "expenses_backup.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Type", "Amount", "Category", "Description","Date"])
    df.to_csv(FILE_NAME, index=False)

df = pd.read_csv(FILE_NAME)
if "Date" not in df.columns:
    df["Date"] = pd.Timestamp.today().strftime("%Y-%m-%d")
    df.to_csv(FILE_NAME, index=False)

# TITLE 
st.title(" Personal Finance Tracker")
st.markdown("Track your income, expenses, and spending habits")


st.header("Add Transaction")

transaction_type = st.radio("Transaction Type", ["Expense", "Income"], horizontal=True)

amount = st.number_input("Enter Amount",min_value=0.0,step=1.0)

# Different cat for Income and Expense

if transaction_type == "Income":
    category = st.selectbox(
        "Select Category",
        [
            "Salary",
            "Freelance",
            "Scholarship",
            "Investment",
            "Gift",
            "Miscellenous",
            "Pocket money",
            "Refund",
            "Borrowed",
            "Cashback",
            "self Transfer",
            "Interest"
        ]
    )
else:
    category = st.selectbox(
        "Select Category",
        [
            "Eating Out",
            "Travel",
            "Food and Drinks",
            "Shopping",
            "Bills",
            "Fuel",
            "Groceries",
            "Medical Expense",
            "Grooming",
            "Lent",
            "Housing Rent",
            "Subscriptions",
            "Education",
            "Taxes",
            "Child Care",
            "Miscellaneous",
            "Gifting",
            "Food Delivery",
            "Pet Care"
        ]
    )

date = st.date_input("Date")

description = st.text_input("Description")

# SAVE BUTTON 

if st.button("Add Transaction"):

    new_transaction = {
        "Type": transaction_type,
        "Amount": amount,
        "Category": category,
        "Description": description,
          "Date": str(date)
          }

    df = pd.concat([df, pd.DataFrame([new_transaction])],ignore_index=True)

    df.to_csv(FILE_NAME, index=False)

    st.success("Transaction Added Successfully!")

    # Refresh dataframe
    df = pd.read_csv(FILE_NAME)

    if "Date" not in df.columns:
        df["Date"] = pd.Timestamp.today().strftime("%Y-%m-%d")
        df.to_csv(FILE_NAME, index=False)

# KPI CARDS 

total_transactions = len(df)

total_income = (df[df["Type"] == "Income"]["Amount"].sum())

total_expense = (df[df["Type"] == "Expense"]["Amount"].sum())

balance = total_income - total_expense

average_expense = df[df["Type"] == "Expense"]["Amount"].mean()

average_income = df[df["Type"] == "Income"]["Amount"].mean()

col1, col2, col3=st.columns(3)
col4 , col5 , col6= st.columns(3)

col1.metric(
    "Transactions",total_transactions)

col2.metric(
    "Income", f"₹ {total_income:,.2f}")

col3.metric(
    "Expense",f"₹ {total_expense:,.2f}")

col4.metric(
    "Balance",f"₹ {balance:,.2f}")

col5.metric(
    "Average Spend",f"₹ {average_expense:,.2f}") 

col6.metric(
    "Average Income", f"₹ {average_income:,.2f}")


expense_df = df[df["Type"] == "Expense"]

if not expense_df.empty:

    category_totals = (expense_df.groupby("Category")["Amount"].sum())

    highest_category = category_totals.idxmax()
    highest_amount = category_totals.max()

    st.metric(" Highest Spending Category",highest_category,f"₹ {highest_amount:,.2f}")


# SIDEBAR FILTER 

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox("Filter by Transaction Type",["All"] + list(df["Type"].unique()))

if selected_category != "All":
    filtered_df = df[df["Type"] == selected_category]
else:
    filtered_df = df

# data

st.subheader("Transaction History")

st.dataframe(filtered_df,use_container_width=True)

# pie chart

st.subheader("Category Money Distribution")

category_data = (filtered_df.groupby("Category")["Amount"].sum().reset_index())

pie_fig = px.pie(category_data,names="Category",values="Amount",hole=0.4)

st.plotly_chart(pie_fig,use_container_width=True) 

# bar chart 

st.subheader("Category-wise Spending ")
st.write("All transactions with the same category and add their amounts together.")

bar_fig = px.bar(category_data,x="Category",y="Amount",color="Category")

st.plotly_chart(bar_fig,use_container_width=True)

# line chart

st.subheader(" Spending Trends Over Time")

df["Date"] = pd.to_datetime(df["Date"])

expense_df = df[df["Type"] == "Expense"].copy()

daily_expense = (expense_df.groupby("Date", as_index=False)["Amount"].sum())

line_fig = px.line(daily_expense,x="Date",y="Amount",title="Daily Expense Trend",markers=True)

st.plotly_chart(line_fig, use_container_width=True)

st.success("All data visualizations are based on the current transactions in the system. Add more transactions to see updated trends and distributions!")
