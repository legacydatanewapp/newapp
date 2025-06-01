import streamlit as st
import pandas as pd

# --- Custom Styling ---
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.imgur.com/E8nl2xS.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }

        .centered-header {
            text-align: center;
            color: white;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .section-spacing {
            margin-top: 30px;
        }

        .stFileUploader {
            width: 360px !important;
            margin: auto;
            display: block;
        }

        input[type="number"] {
            text-align: left !important;
            width: 300px !important;
        }

        .stButton button {
            display: block;
            margin: 10px auto;
        }

        .stDownloadButton {
            text-align: center;
        }

        .block-space {
            margin-bottom: 20px;
        }

        .custom-success {
            background-color: #0f4f36;
            color: white;
            padding: 1rem;
            text-align: center;
            font-weight: bold;
            border-radius: 8px;
            width: 300px;
            margin: 15px auto;
        }

        .centered-subheader {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: white;
            margin-top: 10px;
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<h2 class="centered-header">Prediction App</h2>', unsafe_allow_html=True)

# --- Spacer before Single Input Section ---
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('<h4 class="centered-header">Single Input Prediction</h4>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_value = st.number_input("", step=0.1, label_visibility="collapsed")

if st.button("Predict from single input"):
    result = round(user_value * 0.75, 2)
    st.markdown(f'<div class="custom-success">Prediction: {result}</div>', unsafe_allow_html=True)

# --- Spacer before Batch Upload Section ---
st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
st.markdown('<h4 class="centered-header">Batch Prediction from File</h4>', unsafe_allow_html=True)

col4, col5, col6 = st.columns([1, 2, 1])
with col5:
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"], label_visibility="collapsed")

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.markdown('<div class="block-space"></div>', unsafe_allow_html=True)
        st.markdown('<div class="centered-subheader">Preview of uploaded data:</div>', unsafe_allow_html=True)

        col7, col8, col9 = st.columns([1, 1.5, 1])
        with col8:
            st.data_editor(df.head(), use_container_width=True, disabled=True, hide_index=True)

        if 'value' in df.columns:
            df['prediction'] = df['value'] * 0.75
            st.markdown('<div class="centered-subheader">Predictions:</div>', unsafe_allow_html=True)

            col10, col11, col12 = st.columns([1, 1.5, 1])
            with col11:
                st.data_editor(df, use_container_width=True, disabled=True, hide_index=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Predictions", csv, "predictions.csv", "text/csv")
        else:
            st.error("Your file must have a column named 'value'.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
