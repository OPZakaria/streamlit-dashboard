import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def process_test_status(data):
    filtered_data = data[data['isHeading'] != 'true']
    status_counts = filtered_data['TEST_Status'].value_counts()
    total_count = status_counts.sum()
    status_df = pd.DataFrame({
        'Status': status_counts.index,
        'Count': status_counts.values,
        'Percentage': (status_counts.values / total_count) * 100
    })
    return status_df

def process_verifies_link(data):
    filtered_data = data[(data['Artifact Type'] == 'Test Plan') & (data['isHeading'] != 'True')]
    total_test_plans = len(filtered_data)
    verified_count = filtered_data['Link:Verifies (<)'].notna().sum()
    verified_percent = (verified_count / total_test_plans) * 100
    not_verified_percent = 100 - verified_percent
    verifies_df = pd.DataFrame({
        'Status': ['Verified', 'Not Verified'],
        'Percentage': [verified_percent, not_verified_percent],
        'Count': [verified_count, total_test_plans - verified_count]
    })
    return verifies_df

def process_satisfied_link(data):
    total_req = len(data)
    functional_req = data[data['Req_type'] == 'Functional Req']
    total_functional_req = len(functional_req)
    functional_req_with_link = functional_req['Link:Satisfied by (>)'].notna().sum()
    functional_req_percentage = (total_functional_req / total_req) * 100
    functional_req_with_link_percentage = (functional_req_with_link / total_functional_req) * 100 if total_functional_req > 0 else 0
    satisfied_df = pd.DataFrame({
        'Description': ['Functional Req %', 'Other Req %', '% Functional Req with Link', '% Functional Req without Link'],
        'Percentage': [functional_req_percentage, 100 - functional_req_percentage, functional_req_with_link_percentage, 100 - functional_req_with_link_percentage]
    })
    return satisfied_df

def load_and_analyze(file):
    data = pd.read_excel(file, engine='openpyxl')
    
    if 'TEST_Status' in data.columns:
        st.write("Processing TEST_Status data...")
        status_df = process_test_status(data)
        st.dataframe(status_df)
        fig, ax = plt.subplots()
        ax.pie(status_df['Percentage'], labels=status_df['Status'], autopct='%1.1f%%', startangle=90)
        ax.set_title("TEST_Status Distribution")
        st.pyplot(fig)
    
    elif 'Link:Verifies (<)' in data.columns:
        st.write("Processing Link:Verifies data...")
        verifies_df = process_verifies_link(data)
        st.dataframe(verifies_df)
        fig, ax = plt.subplots()
        ax.pie(verifies_df['Percentage'], labels=verifies_df['Status'], autopct='%1.1f%%', startangle=90)
        ax.set_title("Percentage of Test Plans Verified")
        st.pyplot(fig)
    
    elif 'Link:Satisfied by (>)' in data.columns:
        st.write("Processing Link:Satisfied data...")
        satisfied_df = process_satisfied_link(data)
        st.dataframe(satisfied_df)
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        ax[0].pie([satisfied_df['Percentage'][0], satisfied_df['Percentage'][1]], labels=['Functional Req', 'Other Req'], autopct='%1.1f%%', startangle=90)
        ax[0].set_title("Functional Req vs Other Req")
        ax[1].pie([satisfied_df['Percentage'][2], satisfied_df['Percentage'][3]], labels=['With Link', 'Without Link'], autopct='%1.1f%%', startangle=90)
        ax[1].set_title("Functional Req with Link")
        st.pyplot(fig)
    else:
        st.error("No relevant data found in the selected file.")

st.title('Analyse de la Traçabilité des Produits des Batteries')
st.image("C:\\Users\\Bruger\\OneDrive\\Bureau\\Capture.PNG", width=800)

uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")

if uploaded_file is not None:
    st.success('Fichier chargé avec succès')
    load_and_analyze(uploaded_file)
