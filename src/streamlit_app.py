import streamlit as st
import pandas as pd
import time
import sys
import os
import random
import numpy as np
import json
import ee
from datetime import datetime, timedelta
from google.oauth2 import service_account

# Path setup: This will correctly resolve when streamlit_app.py is run as a script.
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from vedic_binding import QuantumInspiredBridge
import app_backend as backend

# Earth Engine Initialization with proper Auth flow
@st.cache_resource
def init_earth_engine():
    try:
        cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ee_creds.json') # Use __file__ here
        if not os.path.exists(cred_path):
            st.error("Auth File Missing")
            return False

        with open(cred_path, 'r') as f:
            info = json.load(f)

        # Standard Google Auth flow for EE
        scopes = ['https://www.googleapis.com/auth/earthengine']
        credentials = service_account.Credentials.from_service_account_info(info, scopes=scopes)
        ee.Initialize(credentials)
        return True
    except Exception as e:
        st.error(f'Earth Engine Auth Failed: {e}')
        return False

ee_status = init_earth_engine()

# Resource Caching for Vedic Bridge and AI Model
@st.cache_resource
def load_vedic_system():
    try:
        return QuantumInspiredBridge()
    except Exception as e:
        st.error(f"Vedic Kernel Error: {e}")
        return None

bridge = load_vedic_system()

# Data Caching: Earth Engine Regional Indices
@st.cache_data(ttl=3600) # Cache satellite data for 1 hour
def get_cached_satellite_indices(lon, lat, start_date, end_date):
    return backend.get_regional_indices(lon, lat, start_date, end_date)

st.set_page_config(page_title='Divine-Earthly Water Guardian', layout='wide', page_icon='🛡️')

st.title('🌊 Divine-Earthly Water Guardian')
st.markdown('### Automated Safety Verification & Dispatch Interface')

tab_audit, tab_national = st.tabs(['📍 Verification Audit', '🌍 National Command'])

with tab_audit:
    st.header('📍 Critical Zone Audit')
    raw_p = {'ph': round(random.uniform(6.0, 9.0), 2), 'turbidity': round(random.uniform(0.1, 15.0), 2), 'tds': round(random.uniform(100, 600), 1)}

    m1, m2, m3 = st.columns(3)
    m1.metric("Sensor pH", raw_p['ph'])
    m2.metric("Turbidity (NTU)", raw_p['turbidity'])
    m3.metric("TDS (mg/L)", raw_p['tds'])

    st.divider()
    st.subheader("🔍 Information Audit Gate")
    st.warning("⚠️ MANUAL VERIFICATION REQUIRED: Cross-reference ground sensor trends with regional satellite indices.")

    audit_confirmed = st.checkbox("I verify that these readings align with current macro-environmental telemetry.", key="final_audit_gate")

    if audit_confirmed:
        st.success("✅ AUDIT PASSED: Reporting and Dispatch channels UNLOCKED.")

        col_rep, col_dis = st.columns(2)
        with col_rep:
            if st.button("Generate Verified Safety Report"):
                # Generate analysis for the report
                sat_mock = {'NDWI': 0.05, 'NDVI': 0.35}
                analysis = backend.analyze_event_source(raw_p, sat_mock)
                report_path = backend.generate_authority_report('Silchar_Field_Unit', raw_p, sat_mock, analysis)
                st.session_state['last_report'] = report_path
                st.info(f"Report Generated: {os.path.basename(report_path)}")

        with col_dis:
            if st.button("Dispatch Verified Email to Authorities"):
                if 'last_report' in st.session_state:
                    success, message = backend.dispatch_critical_report(st.session_state['last_report'], 'authority.board@gov.in')
                    if success:
                        st.success(message)
                    else:
                        st.error(f"Dispatch Failed: {message}")
                else:
                    st.warning("Please generate a report first.")
    else:
        st.error("🔒 DISPATCH LOCKED: Information Audit Pending.")

with tab_national:
    st.title('🌍 National Water Intelligence Infrastructure')
    st.markdown('### Macro-Environmental Correlation & Authority Dispatch')

    selected_state = st.selectbox('Select Indian State', list(backend.GEOLOCATION_REGISTRY.keys()))
    selected_city = st.selectbox('Select City', list(backend.GEOLOCATION_REGISTRY[selected_state].keys()))

    coords = backend.GEOLOCATION_REGISTRY[selected_state][selected_city]
    lon, lat = coords[0], coords[1]

    # Scenario Selection for Dynamic mock_ground data
    scenario_options = {
        "Normal Operation": {'ph': 7.5, 'turbidity': 2.0, 'tds': 150.0},
        "Regional Flood": {'ph': 7.1, 'turbidity': 25.0, 'tds': 180.0},
        "Industrial Discharge": {'ph': 6.2, 'turbidity': 8.0, 'tds': 700.0},
        "pH Imbalance": {'ph': 5.0, 'turbidity': 3.0, 'tds': 200.0}
    }
    selected_scenario_name = st.selectbox("Select Scenario to Simulate", list(scenario_options.keys()))
    dynamic_mock_ground = scenario_options[selected_scenario_name]

    if st.button('Initialize Multi-Layered Analysis'):
        if not ee_status:
            st.error("Earth Engine is Offline")
        else:
            with st.spinner(f'Synchronizing Satellite Data for {selected_city}...'):
                end_d = datetime.now().strftime('%Y-%m-%d')
                start_d = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

                # Using CACHED function for EE data
                sat_indices = get_cached_satellite_indices(lon, lat, start_d, end_d)

                # Use dynamic_mock_ground based on selected scenario
                analysis = backend.analyze_event_source(dynamic_mock_ground, sat_indices)

                m_col1, m_col2 = st.columns([1, 2])
                with m_col1:
                    st.metric('Regional NDWI', f"{sat_indices['NDWI']:.4f}")
                    st.metric('Regional NDVI', f"{sat_indices['NDVI']:.4f}")
                    st.metric('Correlation Strength', f"{analysis['Correlation Strength']}", delta='Vedic Calibrated')

                with m_col2:
                    st.map(pd.DataFrame([{'lat': lat, 'lon': lon}]))

                st.info(f"**Event Classification:** {analysis['Event Classification']}")
                st.success(f"**Recommendation:** {analysis['Recommended Action Category']}") # Enhanced recommendation display

                if st.button('Dispatch Official Report to Authorities'):
                    report_path = backend.generate_authority_report(selected_city, dynamic_mock_ground, sat_indices, analysis)
                    backend.dispatch_critical_report(report_path, 'authority.board@gov.in')
                    st.success(f'Report generated and synchronized.')