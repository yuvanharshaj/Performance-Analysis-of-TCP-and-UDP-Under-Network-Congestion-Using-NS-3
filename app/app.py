import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import glob
import subprocess
import shutil
import time

# Add python directory to path to reuse analyze_results module
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_DIR = os.path.join(BASE_DIR, "python")
if PYTHON_DIR not in sys.path:
    sys.path.append(PYTHON_DIR)

from analyze_results import parse_flowmon_xml

# Page configuration
st.set_page_config(
    page_title="NS-3 TCP/UDP Congestion Analyzer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)


def check_ns3_availability():
    """Check if NS-3 binary is executable on this environment."""
    if sys.platform.startswith("linux"):
        return os.path.exists("/home/yuvan/ns-allinone-3.42/ns-3.42/build/scratch/ns3.42-congestion-analysis-default")
    elif sys.platform == "win32":
        return shutil.which("wsl") is not None
    return False


def get_available_runs():
    """Get list of completed simulation prefixes from results/raw."""
    raw_dir = os.path.join(BASE_DIR, "results", "raw")
    flowmon_files = glob.glob(os.path.join(raw_dir, "*-flowmon.xml"))
    prefixes = []
    for f in flowmon_files:
        p = f.replace("-flowmon.xml", "")
        prefixes.append(os.path.basename(p))
    return sorted(list(set(prefixes)))


def run_live_simulation(params, output_prefix):
    """
    Safely execute NS-3 simulation binary using argument list (never shell=True).
    """
    linux_binary = "/home/yuvan/ns-allinone-3.42/ns-3.42/build/scratch/ns3.42-congestion-analysis-default"
    lib_path = "/home/yuvan/ns-allinone-3.42/ns-3.42/build/lib"

    if sys.platform == "win32":
        # Using WSL
        target_prefix = f"/home/yuvan/project/results/raw/{os.path.basename(output_prefix)}"
        cmd = [
            "wsl", "-d", "Ubuntu-24.04", "--", "bash", "-c",
            f"LD_LIBRARY_PATH={lib_path} {linux_binary} "
            f"--bottleneckBandwidth={params['bottleneckBandwidth']} "
            f"--bottleneckDelay={params['bottleneckDelay']} "
            f"--queueSize={params['queueSize']} "
            f"--udpDataRate={params['udpDataRate']} "
            f"--packetSize={params['packetSize']} "
            f"--simulationTime={params['simulationTime']} "
            f"--trafficMode={params['trafficMode']} "
            f"--outputPrefix={target_prefix} "
            f"--enableCwndTracing={str(params['enableCwndTracing']).lower()}"
        ]
    else:
        cmd = [
            linux_binary,
            f"--bottleneckBandwidth={params['bottleneckBandwidth']}",
            f"--bottleneckDelay={params['bottleneckDelay']}",
            f"--queueSize={params['queueSize']}",
            f"--udpDataRate={params['udpDataRate']}",
            f"--packetSize={params['packetSize']}",
            f"--simulationTime={params['simulationTime']}",
            f"--trafficMode={params['trafficMode']}",
            f"--outputPrefix={output_prefix}",
            f"--enableCwndTracing={str(params['enableCwndTracing']).lower()}"
        ]

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = lib_path
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)
    return res


# App Header
st.markdown("<div class='main-header'>🌐 Performance Analysis of TCP and UDP Under Congestion</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Course: Computer Networks (24CS53) | Academic IPCC Project | Discrete-Event Network Simulator (NS-3)</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Ns-3-logo.png/320px-Ns-3-logo.png", width=120)
st.sidebar.title("Simulation Control")

ns3_available = check_ns3_availability()
app_mode = st.sidebar.radio(
    "Application Mode:",
    ["Saved Results Browser (Cloud Compatible)", "Live NS-3 Execution (Local Only)"],
    index=0
)

# Saved Results Browser Mode
if app_mode.startswith("Saved Results"):
    st.sidebar.info("💡 **Saved Results Mode Active**\nVisualizes verified simulation runs shipped with the repository. Recommended for cloud hosting (Streamlit Cloud).")
    available_runs = get_available_runs()

    if not available_runs:
        st.warning("No saved experiment results found in `results/raw/`. Run `python python/run_experiments.py` first.")
        st.stop()

    selected_run = st.sidebar.selectbox("Select Experiment Run:", available_runs, index=0)

    # Load summary CSV if available
    summary_path = os.path.join(BASE_DIR, "results", "processed", "experiments_summary.csv")
    if os.path.exists(summary_path):
        summary_df = pd.read_csv(summary_path)
    else:
        summary_df = None

    xml_path = os.path.join(BASE_DIR, "results", "raw", f"{selected_run}-flowmon.xml")
    cwnd_path = os.path.join(BASE_DIR, "results", "raw", f"{selected_run}-cwnd.csv")

    st.subheader(f"Run Details: `{selected_run}`")

    # Parse and display metrics
    flow_stats = parse_flowmon_xml(xml_path)
    if not flow_stats:
        st.error(f"Could not parse FlowMonitor XML at: {xml_path}")
        st.stop()

    metrics_df = pd.DataFrame(flow_stats)

    # Forward flows only for top metric cards
    tcp_flow = next((f for f in flow_stats if "TCP Forward" in f.get("FlowType", "")), None)
    udp_flow = next((f for f in flow_stats if "UDP Forward" in f.get("FlowType", "")), None)

    # Metric Cards Display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tcp_thpt = f"{tcp_flow['Throughput_Mbps']} Mbps" if tcp_flow else "N/A"
        udp_thpt = f"{udp_flow['Throughput_Mbps']} Mbps" if udp_flow else "N/A"
        st.metric("Throughput (TCP / UDP)", f"{tcp_thpt}", f"UDP: {udp_thpt}")
    with col2:
        tcp_pdr = f"{tcp_flow['PDR_percent']}%" if tcp_flow else "N/A"
        udp_pdr = f"{udp_flow['PDR_percent']}%" if udp_flow else "N/A"
        st.metric("PDR (TCP / UDP)", f"{tcp_pdr}", f"UDP: {udp_pdr}")
    with col3:
        tcp_loss = f"{tcp_flow['PacketLoss_percent']}%" if tcp_flow else "N/A"
        udp_loss = f"{udp_flow['PacketLoss_percent']}%" if udp_flow else "N/A"
        st.metric("Packet Loss (TCP / UDP)", f"{tcp_loss}", f"UDP: {udp_loss}")
    with col4:
        tcp_delay = f"{tcp_flow['AvgDelay_ms']} ms" if tcp_flow else "N/A"
        udp_delay = f"{udp_flow['AvgDelay_ms']} ms" if udp_flow else "N/A"
        st.metric("Avg Delay (TCP / UDP)", f"{tcp_delay}", f"UDP: {udp_delay}")

    # Tabs for detailed inspection
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Flow Metrics Table", "📈 Congestion Window (Cwnd)", "📑 Experiment Comparison", "📥 Downloads"])

    with tab1:
        st.dataframe(metrics_df, use_container_width=True)

    with tab2:
        if os.path.exists(cwnd_path):
            cwnd_df = pd.read_csv(cwnd_path)
            if not cwnd_df.empty:
                st.line_chart(cwnd_df.set_index("Time")["Cwnd"] / 1024, height=350, use_container_width=True)
                st.caption("Figure: TCP Congestion Window (KB) vs Simulation Time (s)")
            else:
                st.info("Cwnd trace file exists but contains no records.")
        else:
            st.info("No TCP Cwnd trace generated for this run (e.g., UDP-only mode).")

    with tab3:
        if summary_df is not None:
            st.write("#### All Experiment Runs Summary")
            st.dataframe(summary_df, use_container_width=True)

            # Show pre-generated plots
            st.write("#### Pre-Generated Publication Figures")
            graph_files = [
                ("Queue vs Loss", "queue_vs_loss.png"),
                ("Queue vs Delay", "queue_vs_delay.png"),
                ("Bandwidth vs Throughput", "bandwidth_vs_throughput.png"),
                ("TCP vs UDP PDR", "tcp_vs_udp_pdr.png"),
                ("Cwnd vs Time", "cwnd_vs_time.png")
            ]
            g_col1, g_col2 = st.columns(2)
            for idx, (title, g_file) in enumerate(graph_files):
                g_path = os.path.join(BASE_DIR, "graphs", g_file)
                target_col = g_col1 if idx % 2 == 0 else g_col2
                if os.path.exists(g_path):
                    target_col.image(g_path, caption=title, use_container_width=True)

    with tab4:
        st.write("#### Download Run Artifacts")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            with open(xml_path, "rb") as f:
                st.download_button("Download FlowMonitor XML", f.read(), file_name=f"{selected_run}-flowmon.xml", mime="application/xml")
        with d_col2:
            metrics_csv = metrics_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Metrics CSV", metrics_csv, file_name=f"{selected_run}-metrics.csv", mime="text/csv")
        with d_col3:
            if os.path.exists(cwnd_path):
                with open(cwnd_path, "rb") as f:
                    st.download_button("Download Cwnd CSV", f.read(), file_name=f"{selected_run}-cwnd.csv", mime="text/csv")

# Live Simulation Mode
else:
    st.sidebar.subheader("Live Parameters")
    traffic_mode = st.sidebar.selectbox("Traffic Mode", ["tcp-udp", "tcp", "udp"], index=0)
    bw = st.sidebar.selectbox("Bottleneck Bandwidth", ["1Mbps", "2Mbps", "5Mbps", "10Mbps"], index=1)
    delay = st.sidebar.selectbox("Bottleneck Delay", ["2ms", "5ms", "10ms", "20ms"], index=2)
    queue = st.sidebar.number_input("Bottleneck Queue (packets)", min_value=1, max_value=500, value=50, step=5)
    udp_rate = st.sidebar.selectbox("UDP Data Rate", ["1Mbps", "2Mbps", "5Mbps"], index=1)
    pkt_size = st.sidebar.number_input("Packet Size (bytes)", min_value=64, max_value=2048, value=1024, step=64)
    sim_time = st.sidebar.slider("Simulation Time (seconds)", min_value=2.0, max_value=30.0, value=10.0, step=1.0)
    trace_cwnd = st.sidebar.checkbox("Enable Cwnd Tracing", value=True)

    run_btn = st.sidebar.button("🚀 Run Simulation", type="primary")

    if run_btn:
        timestamp = int(time.time())
        run_name = f"live_{traffic_mode}_bw{bw}_q{queue}_{timestamp}"
        out_prefix = os.path.join(BASE_DIR, "results", "raw", run_name)

        params = {
            "trafficMode": traffic_mode,
            "bottleneckBandwidth": bw,
            "bottleneckDelay": delay,
            "queueSize": queue,
            "udpDataRate": udp_rate,
            "packetSize": pkt_size,
            "simulationTime": sim_time,
            "enableCwndTracing": trace_cwnd
        }

        with st.spinner("Running NS-3 discrete-event simulation..."):
            res = run_live_simulation(params, out_prefix)

        if res.returncode == 0:
            st.success(f"Simulation completed successfully! Output prefix: `{run_name}`")
            xml_out = f"{out_prefix}-flowmon.xml"
            flows = parse_flowmon_xml(xml_out)
            df_live = pd.DataFrame(flows)
            st.dataframe(df_live, use_container_width=True)

            cwnd_out = f"{out_prefix}-cwnd.csv"
            if os.path.exists(cwnd_out):
                cwnd_data = pd.read_csv(cwnd_out)
                st.line_chart(cwnd_data.set_index("Time")["Cwnd"] / 1024)
        else:
            st.error(f"Simulation failed with exit code {res.returncode}:\n{res.stderr}\n{res.stdout}")
