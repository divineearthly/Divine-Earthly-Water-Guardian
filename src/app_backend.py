
import ee
import geemap
import networkx as nx
import pandas as pd
import datetime
import math
import os
from fpdf import FPDF
from ipyleaflet import FullScreenControl, WidgetControl
from ipywidgets import HTML

# --- 1. SATELLITE ENGINE ---
def get_water_health_index(coords):
    poi = ee.Geometry.Point(coords).buffer(5000)
    dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')                     .filterBounds(poi)                     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))                     .sort('system:time_start', False)                     .first()
    ndwi = dataset.normalizedDifference(['B3', 'B8']).rename('NDWI')
    stats = ndwi.reduceRegion(reducer=ee.Reducer.mean(), geometry=poi, scale=10).getInfo()
    return stats['NDWI']

# --- 2. VEDIC-QUANTUM UNIFIED FIELD ---
def calculate_unified_health_field(satellite_score, sensor_df, multiplier=1.08):
    avg_turbidity = sensor_df['Turbidity_NTU'].mean()
    avg_chlorine = sensor_df['Chlorine_mgL'].mean()
    chlorine_stress = max(0, 0.2 - avg_chlorine) / 0.2
    turbidity_stress = min(1, avg_turbidity / 10.0)
    combined_sensor_stress = (chlorine_stress + turbidity_stress) / 2
    satellite_stress = min(1, abs(satellite_score) / 100.0)
    field_correlation = (satellite_stress * combined_sensor_stress) * multiplier
    return round(field_correlation * 100, 2)

# --- 3. DYNAMIC NETWORK SIMULATION ---
def create_dynamic_distribution_network(center_coords):
    lon, lat = center_coords
    G_dyn = nx.DiGraph()
    G_dyn.add_node('Source_WTP', type='Treatment Plant')
    G_dyn.add_node('Tank_1', type='Storage Tank')
    G_dyn.add_node('Cluster_A', type='Residential Cluster')
    G_dyn.add_edge('Source_WTP', 'Tank_1', distance=2.0)
    G_dyn.add_edge('Tank_1', 'Cluster_A', distance=1.5)
    dynamic_pos = {'Source_WTP': (lon, lat), 'Tank_1': (lon + 0.01, lat + 0.01), 'Cluster_A': (lon + 0.02, lat + 0.02)}
    return G_dyn, dynamic_pos

# --- 4. AUTHORITY ROUTING ---
def get_authority_contact(location_query):
    directory = {'Silchar': 'smb1882@gmail.com', 'Guwahati': 'commissionergmc@gmail.com'}
    for loc, email in directory.items():
        if loc.lower() in location_query.lower(): return {'office': loc, 'email': email}
    return {'office': 'National Authority', 'email': 'support@gov.in'}

# --- 5. GRIEVANCE PDF ENGINE ---
def generate_grievance_report(location, ndwi, risk, map_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'DIVINE EARTHLY WATER GRIEVANCE', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f'Location: {location}\nNDWI: {ndwi:.4f}\nRisk Index: {risk}')
    if os.path.exists(map_path): pdf.image(map_path, x=10, w=180)
    output = 'grievance_report.pdf'
    pdf.output(output)
    return output

# --- PLACEHOLDER FOR WEB UI (e.g., Streamlit) ---
# st.title('Divine Earthly Water Guardian')
# lat = st.number_input('Latitude', value=24.83)
# lon = st.number_input('Longitude', value=92.77)
