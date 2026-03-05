
# 🌊 Divine Earthly Water Guardian (DEWG)
**"Harmonizing Earth's Vitals through Vedic-Quantum Intelligence"**

## 🔱 Vision
The Divine Earthly Water Guardian is a monitoring and optimization system designed to protect and revitalize water bodies. By integrating **Quantum Physics** and **Vedic Formulas**, DEWG creates a "Vitality Index" for water resources, moving beyond simple data collection toward true environmental harmony.

## 🧬 The Core Logic: Vedic-Quantum Optimization
This project utilizes a specific **Vedic Constant ($1.08$)** to calibrate environmental data.
* **Input:** Real-time satellite data (NASA SMAP for Soil Moisture & Sentinel-2 for NDWI).
* **Processing:** A Quantum-Vedic engine that calculates the "Prana" (Life Force) of the water body.
* **Output:** Precise health scores that trigger alerts when the ecological balance is disrupted.



## 🛠️ Tech Stack
* **Language:** Python 3
* **Tools:** Google Colab, Pydroid 3, Termux
* **Libraries:** `pandas`, `numpy`, `matplotlib`
* **Future Hardware:** IoT-enabled sensors (ESP32/Arduino) for localized physical monitoring.

## 🚀 How to Run (Google Colab)
1. Open the `Water_Guardian_Colab.ipynb` file.
2. Run the environment setup cell to install dependencies.
3. Execute the `DivineWaterGuardian` engine to begin the simulation.

---
**Founder:** Joydeep Das
**Project:** Divine Earthly
**UPI for Support:** `divinesouljoy@pnb`


## ⚙ Hybrid C++/Python Architecture
The system utilizes a hybrid architecture for high-performance edge computing. A Python-based `QuantumInspiredBridge` serves as the primary interface, communicating with a high-speed C++ shared library (`libvedic.so`) via the `ctypes` foreign function interface. This allows the system to perform Vedic-accelerated normalization of sensor data at near-native speeds before feeding results into the predictive AI kernel.

### ⚙ Compilation Instructions
To recompile the Vedic optimization library, use the following command from the project root:
```bash
g++ -O3 -shared -fPIC -o cpp/libvedic.so cpp/vedic_multiplier.cpp
```
*   `-O3`: Enables maximum compiler optimizations.
*   `-shared`: Creates a shared object library.
*   `-fPIC`: Generates Position Independent Code, required for shared libraries.

### ⚙ Model Input Schema (Pruned Model)
The pruned Random Forest model is optimized for 5 specific features. All inputs must be normalized through the Vedic C++ kernel before interaction features are engineered. The required input order is:
1.  `Turb_TDS_Interaction` (Normalized Turbidity %% Normalized TDS)
2.  `pH_Turb_Interaction` (Normalized pH %% Normalized Turbidity)
3.  `Normalized pH` (Raw pH calibrated by 1.08 constant)
4.  `pH_Squared` (Normalized pH%%2)
5.  `pH_TDS_Interaction` (Normalized pH %% Normalized TDS)


## ⚙ Hybrid C++/Python Architecture
The Divine-Earthly Water Guardian utilizes a high-performance hybrid architecture. A Python-based `QuantumInspiredBridge` serves as the primary interface, communicating with a high-speed C++ shared library (`libvedic.so`) via the `ctypes` foreign function interface. This allows the system to perform Vedic-accelerated normalization of sensor data at near-native speeds before feeding results into the predictive AI kernel.

### 🛠 Compilation Instructions
To recompile the Vedic optimization library, use the following `g++` command from the project root:
```bash
g++ -O3 -shared -fPIC -o cpp/libvedic.so cpp/vedic_multiplier.cpp
```
*   `-O3`: Enables maximum compiler optimizations for speed.
*   `-shared`: Instructs the compiler to produce a shared object library (.so).
*   `-fPIC`: Generates Position Independent Code, which is required for shared libraries.

### 📊 Model Input Schema (Pruned Model)
The pruned Random Forest model is optimized to process 5 specific features. All inputs must be normalized through the Vedic C++ kernel before feature engineering. The required input order for the model is:
1.  `Turb_TDS_Interaction` (Normalized Turbidity &times; Normalized TDS)
2.  `pH_Turb_Interaction` (Normalized pH &times; Normalized Turbidity)
3.  `Normalized pH` (Raw pH calibrated by the 1.08 Vedic constant)
4.  `pH_Squared` (Normalized pH")
5.  `pH_TDS_Interaction` (Normalized pH &times; Normalized TDS)
