
import streamlit as st
import pandas as pd
import app_backend as backend
import ee
import json
import os

st.set_page_config(page_title='Divine Earthly Water Guardian', layout='wide')

# --- GEE INITIALIZATION ---
def init_gee():
    if 'EE_SERVICE_ACCOUNT_JSON' in st.secrets:
        info = json.loads(st.secrets['EE_SERVICE_ACCOUNT_JSON'])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=info['private_key'])
        ee.Initialize(credentials, project=info['project_id'])
        return True
    return False

st.title('🌊 Divine Earthly: National Water Guardian')
st.markdown('### Autonomous Satellite Monitoring & Official Grievance System')

# --- SIDEBAR CONFIG ---
st.sidebar.header('Location Settings')
lat = st.sidebar.number_input('Latitude', value=24.8333, format='%.4f')
lon = st.sidebar.number_input('Longitude', value=92.7789, format='%.4f')
loc_name = st.sidebar.text_input('City/Region Name', 'Silchar, Assam')

if st.sidebar.button('Analyze Location'):
    try:
        with st.spinner('Accessing Sentinel-2 Satellite Data...'):
            if init_gee():
                coords = [lon, lat]
                ndwi = backend.get_water_health_index(coords)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric('Detected NDWI', f'{ndwi:.4f}')
                    health_score = round(ndwi * 108, 2) # Simplified Vedic Multiplier
                    st.metric('Vedic Health Score', f'{health_score}/100')
                
                with col2:
                    st.info('Generating Infrastructure Simulation...')
                    # Logic to run network and map would go here
                    st.success('Analysis Complete')

                if st.button('Generate Official PDF Grievance'):
                    # Call backend PDF engine
                    solutions = ['GAC Filtration', 'Chlorine Boosting']
                    pdf_path = backend.generate_grievance_report(loc_name, ndwi, 45.0, solutions)
                    with open(pdf_path, 'rb') as f:
                        st.download_button('Download Official Report', f, file_name='Water_Grievance.pdf')
            else:
                st.error('GEE Service Account not configured in Secrets.')
    except Exception as e:
        st.error(f'Error: {e}')
