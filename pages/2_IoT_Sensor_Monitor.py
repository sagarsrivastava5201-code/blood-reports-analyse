
import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="IoT Health Monitoring",
    page_icon="📡",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background: #f2f8f7;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #cfe3df;
}
.status {
    background: #d8eeea;
    padding: 15px;
    border-radius: 12px;
    color: #12302f;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("📡 IoT Health Monitoring")
st.caption("Monitor health parameters using connected sensors or simulation.")

# ---------- MODE ----------
mode = st.radio(
    "Select Monitoring Mode",
    ["Simulation Mode", "Real Sensor Mode"],
    horizontal=True
)

if mode == "Simulation Mode":
    st.info("Simulation Mode: Generated sample data is being used. These are NOT actual patient readings.")

    if "sensor_history" not in st.session_state:
        st.session_state.sensor_history = []

    # Generate readings
    heart_rate = random.randint(70, 95)
    spo2 = random.randint(95, 100)
    temperature = round(random.uniform(36.2, 37.5), 1)

    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.sensor_history.append({
        "Time": timestamp,
        "Heart Rate": heart_rate,
        "SpO2": spo2,
        "Temperature": temperature
    })

    st.session_state.sensor_history = st.session_state.sensor_history[-30:]

    # ---------- METRICS ----------
    st.subheader("Live Sensor Readings")

    col1, col2, col3 = st.columns(3)

    col1.metric("❤️ Heart Rate", f"{heart_rate} BPM")
    col2.metric("🫁 SpO₂", f"{spo2}%")
    col3.metric("🌡️ Temperature", f"{temperature} °C")

    # ---------- STATUS ----------
    st.subheader("Health Monitoring Status")

    if heart_rate > 100 or spo2 < 95 or temperature >= 38:
        st.warning("Some readings need attention. Check the readings and consult a healthcare professional if concerned.")
    else:
        st.success("Sample readings are within the selected demo thresholds.")

    # ---------- GRAPHS ----------
    df = pd.DataFrame(st.session_state.sensor_history)

    st.subheader("📊 Sensor Data Graphs")

    st.line_chart(
        df.set_index("Time")[["Heart Rate"]],
        y_label="BPM"
    )

    st.line_chart(
        df.set_index("Time")[["SpO2"]],
        y_label="Percentage"
    )

    st.line_chart(
        df.set_index("Time")[["Temperature"]],
        y_label="°C"
    )

    # ---------- INSIGHTS ----------
    st.subheader("💡 Basic Health Insights")

    if heart_rate > 100:
        st.write("• Heart rate is above the demo threshold.")
    else:
        st.write("• Heart rate is within the demo threshold.")

    if spo2 < 95:
        st.write("• Oxygen saturation is below the demo threshold.")
    else:
        st.write("• Oxygen saturation is within the demo threshold.")

    if temperature >= 38:
        st.write("• Temperature is elevated in this sample.")
    else:
        st.write("• Temperature is within the demo threshold.")

    # ---------- HISTORY ----------
    st.subheader("📋 Sensor Data History")
    st.dataframe(df, use_container_width=True)

    if st.button("🔄 Refresh Sensor Data"):
        st.rerun()

else:
    st.subheader("🔌 Real Sensor Connection")

    st.warning(
        "Real Sensor Mode requires an ESP32 or compatible device "
        "that sends actual sensor readings."
    )

    st.write("Expected sensor data:")
    st.code("""
{
    "heart_rate": 78,
    "spo2": 98,
    "temperature": 36.8
}
    """, language="json")

    st.info(
        "Connect your ESP32 through Wi-Fi/API to receive actual readings here. "
        "No real sensor data is connected yet."
    )

# ---------- FOOTER ----------
st.divider()
st.caption("HealthLens IoT Monitoring | Simulation and sensor-based monitoring demo")
st.caption("Developed by Sagar Srivastava")
