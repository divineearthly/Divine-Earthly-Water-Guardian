import os
import sys
from vedic_binding import QuantumInspiredBridge

def simulate_sensor_call(bridge):
    """Simulates a hardware sensor data retrieval and Silchar safety check."""
    ph_val = 7.2
    turb_val = 3.1
    tds_val = 250.0

    print(f"--- Silchar Regional Sensor Input ---")
    print(f"pH: {ph_val}, Turbidity: {turb_val} NTU, TDS: {tds_val} mg/L")

    try:
        safety_score = bridge.run_silchar_check(ph_val, turb_val, tds_val)
        print(f"\nVedic Safety Score: {safety_score:.2f}/100")

        if safety_score > 70.0:
            print("STATUS: SAFE (GREEN) - Within BIS 10500:2012 Standards")
        else:
            print("STATUS: UNSAFE/CONTAMINATED (RED) - Immediate Intervention Required")
    except Exception as e:
        print(f"Error during Silchar safety check: {e}")

def main():
    """Entry point for the Divine-Earthly Water Guardian interface."""
    print("Initializing Divine-Earthly Water Guardian: Silchar Module...")
    try:
        bridge = QuantumInspiredBridge()
        print("Vedic-Python Bridge: ACTIVE")
        simulate_sensor_call(bridge)
    except Exception as e:
        print(f"System Initialization Failed: {e}")

if __name__ == "__main__":
    main()
