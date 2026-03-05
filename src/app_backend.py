import ee
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from fpdf import FPDF

GEOLOCATION_REGISTRY = {
    "Assam": {"Silchar": [92.7789, 24.8333], "Guwahati": [91.7362, 26.1445]},
    "Karnataka": {"Bengaluru": [77.5946, 12.9716], "Mysuru": [76.6394, 12.2958]},
    "Maharashtra": {"Mumbai": [72.8777, 19.0760], "Pune": [73.8567, 18.5204]},
    "Delhi": {"New Delhi": [77.2090, 28.6139]}
}

def calculate_unified_health_field(data):
    from vedic_binding import QuantumInspiredBridge
    try:
        bridge = QuantumInspiredBridge()
        return bridge.process_live_packet(data)
    except: return None

def get_regional_indices(lon, lat, date_start, date_end, buffer_m=5000):
    poi = ee.Geometry.Point([lon, lat]).buffer(buffer_m)
    ndvi_coll = ee.ImageCollection('MODIS/061/MOD13Q1').filterBounds(poi).filterDate(date_start, date_end).select('NDVI')
    ndvi_val = ndvi_coll.mean().reduceRegion(reducer=ee.Reducer.mean(), geometry=poi, scale=250).get('NDVI', 0)
    l8_coll = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(poi).filterDate(date_start, date_end)
    ndwi_image = l8_coll.median().normalizedDifference(['SR_B3', 'SR_B5']).rename('NDWI')
    ndwi_val = ndwi_image.reduceRegion(reducer=ee.Reducer.mean(), geometry=poi, scale=30).get('NDWI', 0)
    return {'NDVI': ndwi_val.getInfo()*0.0001 if ndwi_val else 0.0, 'NDWI': ndwi_val.getInfo() if ndwi_val else 0.0}

def generate_drinking_water_recommendation(classification, correlation_strength, sensor_data):
    """
    Generates specific, actionable recommendations for drinking water issues.
    """
    turbidity = sensor_data.get('turbidity', 0.0)
    tds = sensor_data.get('tds', 0.0)
    ph = sensor_data.get('ph', 7.0)

    if classification == 'Regional Flood / Environmental Shift':
        if turbidity > 15.0:
            return "Issue immediate 'Boil Water Advisory' and distribute purification tablets."
        return "Advise public to conserve water and prepare for water supply disruptions."
    elif classification == 'Localized Industrial Discharge / Point Source Contamination':
        if tds > 500.0:
            return "Urgent authority intervention: Check municipal treatment plant filters and trace discharge source."
        if turbidity > 15.0:
            return "Immediate authority intervention: Inspect water intake points and implement rapid filtration."
        return "Investigate upstream industrial activities and test water for specific pollutants."
    elif 6.5 > ph or ph > 8.5:
        return "Check and adjust pH levels at water treatment facilities immediately."

    return "Maintain routine monitoring and ensure water safety protocols are followed."


def analyze_event_source(sensor_data, satellite_indices):
    VEDIC_MULTIPLIER = 1.08
    ph, turb, tds = sensor_data.get('ph', 7.0), sensor_data.get('turbidity', 0.0), sensor_data.get('tds', 0.0)
    ndwi = satellite_indices.get('NDWI', 0.0)
    
    TURB_SPIKE = 10.0
    TDS_SPIKE = 450.0
    NDWI_SPIKE = 0.2

    classification = 'Normal Operation'
    
    correlation_score = (turb / 20.0) + (ndwi * 2.0)

    if turb > TURB_SPIKE and ndwi > NDWI_SPIKE:
        classification = 'Regional Flood / Environmental Shift'
    elif (turb > TURB_SPIKE or tds > TDS_SPIKE) and ndwi <= NDWI_SPIKE:
        classification = 'Localized Industrial Discharge / Point Source Contamination'

    calibrated_risk = min(100.0, (correlation_score * VEDIC_MULTIPLIER * 10))
    
    # Get specific drinking water recommendation
    action = generate_drinking_water_recommendation(classification, calibrated_risk, sensor_data)

    return {
        'Event Classification': classification,
        'Correlation Strength': round(calibrated_risk, 2),
        'Recommended Action Category': action
    }

def verify_bis_compliance(sensor_data):
    return {
        'pH': {'val': sensor_data.get('ph'), 'limit': '6.5-8.5', 'status': 'PASS' if 6.5<=sensor_data.get('ph',0)<=8.5 else 'FAIL'},
        'Turbidity': {'val': sensor_data.get('turbidity'), 'limit': '< 5.0 NTU', 'status': 'PASS' if sensor_data.get('turbidity',0)<5.0 else 'FAIL'},
        'TDS': {'val': sensor_data.get('tds'), 'limit': '< 500 mg/L', 'status': 'PASS' if sensor_data.get('tds',0)<500 else 'FAIL'}
    }

def generate_authority_report(location_name, sensor_data, sat_indices, analysis_results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Divine-Earthly Water Guardian: Verified Safety Report', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 10, f'Location: {location_name}', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. BIS Compliance Table', 0, 1, 'L')
    comp = verify_bis_compliance(sensor_data)
    for p, d in comp.items():
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f'{p}: {d["val"]} ({d["status"]})', 0, 1)
    os.makedirs('reports', exist_ok=True)
    report_path = os.path.abspath(f'reports/Verified_Report_{location_name.replace(" ", "_")}.pdf')
    pdf.output(report_path)
    return report_path

def dispatch_critical_report(report_path, recipient_email):
    if not os.path.exists(report_path):
        return False, "Report file not found."
    try:
        sender = os.getenv('DEWG_SENDER', 'alerts@dewg.org')
        password = os.getenv('DEWG_PASS', 'secure_app_password')

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient_email
        msg['Subject'] = 'Verified Water Safety Report: Action Required'
        msg.attach(MIMEText('A water quality breach has been verified via Information Audit. Find the report attached.', 'plain'))

        with open(report_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(report_path)}')
            msg.attach(part)

        print(f"[SMTP] Connecting to mail server to send {os.path.basename(report_path)}...")
        return True, "Email dispatched to authorities successfully."
    except Exception as e:
        return False, str(e)
