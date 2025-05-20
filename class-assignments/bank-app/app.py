import streamlit as st
from bank import BankAccount, PersonalAccount

st.title("💰 Bank Account Management System")

# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = None

# Account selection
account_type = st.selectbox("Select Account Type", ["Normal Account", "Premium Account"])
name = st.text_input("Enter Account Holder's Name")

# Account creation
if st.button("Create Account"):
    if name:
        if account_type == "Normal Account":
            st.session_state.account = BankAccount(name)
        else:
            st.session_state.account = PersonalAccount(name)
        st.success(f"{account_type} created for {name}")
    else:
        st.error("Please enter a name")

# If account is created, show options
if st.session_state.account:
    st.subheader(f"Welcome {st.session_state.account.get_name()}!")

    action = st.selectbox("Select Action", ["Deposit", "Withdraw", "Check Balance"])

    if action == "Check Balance":
        st.info(st.session_state.account.get_balance())

    elif action == "Deposit":
        amount = st.number_input("Enter Amount to Deposit", min_value=0)
        if st.button("Deposit"):
            result = st.session_state.account.deposit(amount)
            st.success(result)

    elif action == "Withdraw":
        amount = st.number_input("Enter Amount to Withdraw", min_value=0)
        if st.button("Withdraw"):
            result = st.session_state.account.withdraw(amount)
            st.success(result)
