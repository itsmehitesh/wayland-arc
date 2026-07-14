import streamlit as st
import plotly.graph_objects as go
import time
from data import TelemetryDatabase
from analytics import StatisticalProcessControl
from alerts import SafetyAlertSystem

st.set_page_config(page_title="Wayland Cell Dashboard", layout="wide")
st.title("Wayland Industrial Production Dashboard")

# Engineering Limits
USL = 11.5
LSL = 8.5

db = TelemetryDatabase(db_path='data/wayland.db')
spc = StatisticalProcessControl()
safety = SafetyAlertSystem(cpk_target=1.33)

metrics_block = st.container()
alarms_block = st.container()
plots_block = st.container()

def refresh_mes_view():
    df = db.fetch_recent(limit=100)
    
    if df.empty:
        st.warning("Data Storage Pipeline Empty. Awaiting initial records from main.py...")
        return

    widths = df['bead_width'].values
    mean, ucl, lcl = spc.get_control_limits(widths)
    _, cpk = spc.calculate_cpk(widths, USL, LSL)
    current_val = widths[-1]
    
    # Process Alarms
    active_alarms = safety.check_tolerances(current_val, USL, LSL, cpk)

    with metrics_block:
        st.markdown("### Manufacturing Execution Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Optical Width", f"{current_val:.2f} mm")
        col2.metric("Calculated Process Cpk", f"{cpk:.2f}", delta="Out of Control" if cpk < 1.33 else "Stable Range", delta_color="inverse" if cpk < 1.33 else "normal")
        col3.metric("Arc Potential (Voltage)", f"{df['voltage'].values[-1]:.1f} V")
        col4.metric("Line Load (Amps)", f"{df['current'].values[-1]:.0f} A")

    with alarms_block:
        if active_alarms:
            for error in active_alarms:
                st.error(f"⚠️ {error}")
        else:
            st.success("✅ System Status: Manufacturing tolerances normal.")

    with plots_block:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['bead_width'], mode='lines+markers', name='Bead Measurements', line=dict(color='#00ffcc')))
        fig.add_hline(y=USL, line_dash="dash", line_color="red", annotation_text="USL (Upper Specification Limit)")
        fig.add_hline(y=LSL, line_dash="dash", line_color="red", annotation_text="LSL (Lower Specification Limit)")
        fig.add_hline(y=ucl, line_dash="dot", line_color="yellow", annotation_text="UCL (Upper Control Limit)")
        fig.add_hline(y=lcl, line_dash="dot", line_color="yellow", annotation_text="LCL (Lower Control Limit)")
        fig.add_hline(y=mean, line_color="green", annotation_text="Process Mean")
        
        fig.update_layout(title="X-Bar Quality Control Chart", xaxis_title="Timestamp", yaxis_title="Dimension (mm)", template="plotly_dark", height=420)
        st.plotly_chart(fig, use_container_width=True)

while True:
    refresh_mes_view()
    time.sleep(1)
    st.rerun()