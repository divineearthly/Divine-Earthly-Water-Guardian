import os
import sys
from vedic_binding import QuantumInspiredBridge

def simulate_sensor_call(bridge):
    """Simulates a hardware sensor data retrieval and processing."""
    # Sample sensor data
    ph_val = 7.0
    turb_val = 5.0
    tds_val = 200.0
    
    print(f"--- Simulated Sensor Input ---")
    print(f"pH: {ph_val}, Turbidity: {turb_val}, TDS: {tds_val}")
    
    # Process via C++ Vedic Kernel
    try:
        results = bridge.run_prediction(ph_val, turb_val, tds_val)
        print("\n--- Vedic C++ Normalized Results ---")
        print(results['normalized'])
    except Exception as e:
        print(f"Error during kernel execution: {e}")

def main():
    """Entry point for the Divine-Earthly Water Guardian interface."""
    print("Initializing Divine-Earthly Water Guardian System...")
    
    try:
        # Instantiate the bridge (path is handled automatically by the class logic)
        bridge = QuantumInspiredBridge()
        print("Vedic-Python Bridge: ACTIVE")
        
        # Execute sample simulation
        simulate_sensor_call(bridge)
        
    except Exception as e:
        print(f"System Initialization Failed: {e}")

if __name__ == '__main__':
    # This structure is compatible with future Tkinter GUI threading/mainloop
    main()
