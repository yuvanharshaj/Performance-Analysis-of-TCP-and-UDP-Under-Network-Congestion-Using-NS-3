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
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.0rem;
    }
    .mode-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    .mode-badge-saved {
        background-color: #E0F2FE;
        color: #0369A1;
        border: 1px solid #BAE6FD;
    }
    .mode-badge-local {
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #BBF7D0;
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


def get_system_deploy_mode():
    """
    Detect deployment mode:
    1. Explicit environment variable DEPLOY_MODE ('saved' or 'local').
    2. Auto-detect: if NS-3 binary/WSL environment is missing, lock to 'saved'.
    """
    env_mode = os.environ.get("DEPLOY_MODE", "").lower().strip()
    if env_mode in ["saved", "local"]:
        return env_mode
    if check_ns3_availability():
        return "local"
    return "saved"


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


# Determine operational mode
system_mode = get_system_deploy_mode()

# App Header
st.markdown("<div class='main-header'>🌐 Performance Analysis of TCP and UDP Under Congestion</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Course: Computer Networks (24CS53) | Academic IPCC Project | Discrete-Event Network Simulator (NS-3)</div>", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Ns-3-logo.png/320px-Ns-3-logo.png", width=120)
st.sidebar.title("Simulation Control")

if system_mode == "saved":
    st.sidebar.markdown("""
    <div class='mode-badge mode-badge-saved'>🟢 MODE: SAVED-RESULTS (Cloud Deployment)</div>
    """, unsafe_allow_html=True)
    st.sidebar.info("💡 **Saved-Results Mode Active**\nVisualizes verified empirical NS-3 simulation data shipped with the repository. NS-3 binary execution is disabled on cloud hosts.")
    active_mode = "saved"
else:
    mode_selection = st.sidebar.radio(
        "Application Mode:",
        ["Saved-Results Mode (Cloud / Verified Data)", "Live NS-3 Execution (Local Subprocess)"],
        index=0
    )
    if mode_selection.startswith("Saved-Results"):
        active_mode = "saved"
        st.sidebar.markdown("""
        <div class='mode-badge mode-badge-saved'>🟢 MODE: SAVED-RESULTS</div>
        """, unsafe_allow_html=True)
    else:
        active_mode = "local"
        st.sidebar.markdown("""
        <div class='mode-badge mode-badge-local'>⚡ MODE: LOCAL LIVE NS-3</div>
        """, unsafe_allow_html=True)

# Display active mode banner in main area
if active_mode == "saved":
    st.info("📌 **Deployment Mode: Saved Results** | Visualizing 11 verified empirical NS-3 experiment runs from `results/raw/`. No subprocess or simulation binary is invoked on this host.")
else:
    st.success("⚡ **Deployment Mode: Local Live Simulation** | Connected to local NS-3 environment. Live discrete-event simulation via subprocess is enabled.")

# Available runs in repository
available_runs = get_available_runs()
if not available_runs:
    st.error("No saved experiment results found in `results/raw/`. Please ensure dataset is committed.")
    st.stop()

# Load summary CSV if present
summary_path = os.path.join(BASE_DIR, "results", "processed", "experiments_summary.csv")
summary_df = pd.read_csv(summary_path) if os.path.exists(summary_path) else None

# Execution / Inspection Section
if active_mode == "saved":
    st.sidebar.subheader("Select Saved Experiment")
    
    # Run descriptions for user clarity
    run_labels = {
        "exp1_queue_10p": "Exp 1: Queue Size = 10 packets (Severe drops)",
        "exp1_queue_25p": "Exp 1: Queue Size = 25 packets (Moderate buffer)",
        "exp1_queue_50p": "Exp 1: Queue Size = 50 packets (Baseline buffer)",
        "exp1_queue_100p": "Exp 1: Queue Size = 100 packets (Large buffer / bufferbloat)",
        "exp2_bw_1Mbps": "Exp 2: Bottleneck Bandwidth = 1 Mbps (Severe bottleneck)",
        "exp2_bw_2Mbps": "Exp 2: Bottleneck Bandwidth = 2 Mbps (Baseline contention)",
        "exp2_bw_5Mbps": "Exp 2: Bottleneck Bandwidth = 5 Mbps (Capacity surplus)",
        "exp2_bw_10Mbps": "Exp 2: Bottleneck Bandwidth = 10 Mbps (Full absorption)",
        "exp3_mode_tcp": "Exp 3: TCP-Only Mode (99.25% link utilization)",
        "exp3_mode_udp": "Exp 3: UDP-Only Mode (Unresponsive saturation)",
        "exp3_mode_tcp-udp": "Exp 3: TCP + UDP Contention (TCP starvation)",
        "test_tcp_udp": "Baseline: Verification Run (TCP + UDP)",
        "test_symlink": "Verification: Symlink Build Test"
    }
    
    def format_run_label(r):
        return run_labels.get(r, f"Run: {r}")

    selected_run = st.sidebar.selectbox(
        "Available Experiment Runs:",
        available_runs,
        format_func=format_run_label,
        index=0
    )

    # Saved Mode "Run Simulation" button that loads and displays the actual pre-computed run
    run_sim_btn = st.sidebar.button("🚀 Run Simulation (Load Saved Data)", type="primary")

    if run_sim_btn:
        st.toast(f"Loaded verified results for `{selected_run}`", icon="✅")

    # Main view for the selected run
    st.markdown(f"### Experiment Run: `{selected_run}` ({format_run_label(selected_run)})")
    st.caption("ℹ️ **Saved-Results Mode Active:** Metrics, packet statistics, and congestion window traces are retrieved directly from pre-computed dataset files in `results/raw/`.")

    xml_path = os.path.join(BASE_DIR, "results", "raw", f"{selected_run}-flowmon.xml")
    cwnd_path = os.path.join(BASE_DIR, "results", "raw", f"{selected_run}-cwnd.csv")

    # Parse FlowMonitor XML
    flow_stats = parse_flowmon_xml(xml_path)
    if not flow_stats:
        st.error(f"Could not parse FlowMonitor XML at: `{xml_path}`")
        st.stop()

    metrics_df = pd.DataFrame(flow_stats)

    # Extract forward flows for top-level metric cards
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
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Flow Metrics Table",
        "📈 Congestion Window (Cwnd)",
        "📑 All Experiments Summary & Figures",
        "📥 Downloads"
    ])

    with tab1:
        st.write("#### Detailed Flow Statistics (FlowMonitor)")
        st.dataframe(metrics_df, use_container_width=True)

    with tab2:
        st.write("#### TCP Congestion Window (Cwnd) Dynamics")
        if os.path.exists(cwnd_path):
            cwnd_df = pd.read_csv(cwnd_path)
            if not cwnd_df.empty:
                cwnd_df["Cwnd_KB"] = cwnd_df["Cwnd"] / 1024.0
                st.line_chart(cwnd_df, x="Time", y="Cwnd_KB", height=380, use_container_width=True)
                st.caption("Figure: TCP Congestion Window (KB) vs Simulation Time (seconds). Shows additive increase and multiplicative decrease (AIMD) phases.")
            else:
                st.info("Cwnd trace file exists but contains no records.")
        else:
            st.info("ℹ️ No TCP Cwnd trace generated for this run (e.g., UDP-only traffic mode).")

    with tab3:
        if summary_df is not None:
            st.write("#### All 11 Verified Experiment Runs")
            st.dataframe(summary_df, use_container_width=True)

            st.write("#### Pre-Generated High-DPI Publication Figures")
            graph_files = [
                ("Queue Size vs Packet Loss", "queue_vs_loss.png"),
                ("Queue Size vs Latency & Delay", "queue_vs_delay.png"),
                ("Bottleneck Bandwidth vs Throughput", "bandwidth_vs_throughput.png"),
                ("TCP vs UDP Contention (PDR Comparison)", "tcp_vs_udp_pdr.png"),
                ("TCP Congestion Window Tracing (Cwnd vs Time)", "cwnd_vs_time.png")
            ]
            g_col1, g_col2 = st.columns(2)
            for idx, (title, g_file) in enumerate(graph_files):
                g_path = os.path.join(BASE_DIR, "graphs", g_file)
                target_col = g_col1 if idx % 2 == 0 else g_col2
                if os.path.exists(g_path):
                    target_col.image(g_path, caption=f"Figure: {title}", use_container_width=True)

    with tab4:
        st.write("#### Download Experiment Artifacts")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            with open(xml_path, "rb") as f:
                st.download_button(
                    "📥 FlowMonitor XML",
                    f.read(),
                    file_name=f"{selected_run}-flowmon.xml",
                    mime="application/xml",
                    key=f"dl_xml_{selected_run}"
                )
        with d_col2:
            metrics_csv = metrics_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Metrics CSV",
                metrics_csv,
                file_name=f"{selected_run}-metrics.csv",
                mime="text/csv",
                key=f"dl_metrics_{selected_run}"
            )
        with d_col3:
            if os.path.exists(cwnd_path):
                with open(cwnd_path, "rb") as f:
                    st.download_button(
                        "📥 Cwnd Trace CSV",
                        f.read(),
                        file_name=f"{selected_run}-cwnd.csv",
                        mime="text/csv",
                        key=f"dl_cwnd_{selected_run}"
                    )
            else:
                st.button("📥 Cwnd Trace CSV (N/A for UDP)", disabled=True)

        st.markdown("---")
        st.write("#### Download Complete Dataset & Publication Figures")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if summary_df is not None:
                summary_csv_bytes = summary_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Complete Experiments Summary CSV (All 11 Runs)",
                    summary_csv_bytes,
                    file_name="experiments_summary.csv",
                    mime="text/csv",
                    key="dl_summary_all"
                )
        with p_col2:
            st.write("Download High-DPI Publication PNGs:")
            for g_name, g_fn in [("Queue vs Loss", "queue_vs_loss.png"),
                                 ("Queue vs Delay", "queue_vs_delay.png"),
                                 ("Bandwidth vs Throughput", "bandwidth_vs_throughput.png"),
                                 ("TCP vs UDP PDR", "tcp_vs_udp_pdr.png"),
                                 ("Cwnd vs Time", "cwnd_vs_time.png")]:
                g_p = os.path.join(BASE_DIR, "graphs", g_fn)
                if os.path.exists(g_p):
                    with open(g_p, "rb") as gf:
                        st.download_button(
                            f"🖼️ {g_name} (PNG)",
                            gf.read(),
                            file_name=g_fn,
                            mime="image/png",
                            key=f"dl_graph_{g_fn}"
                        )

# Local Simulation Mode (Subprocess to NS-3 Binary)
else:
    st.sidebar.subheader("Live Simulation Parameters")
    traffic_mode = st.sidebar.selectbox("Traffic Mode", ["tcp-udp", "tcp", "udp"], index=0)
    bw = st.sidebar.selectbox("Bottleneck Bandwidth", ["1Mbps", "2Mbps", "5Mbps", "10Mbps"], index=1)
    delay = st.sidebar.selectbox("Bottleneck Delay", ["2ms", "5ms", "10ms", "20ms"], index=2)
    queue = st.sidebar.number_input("Bottleneck Queue (packets)", min_value=1, max_value=500, value=50, step=5)
    udp_rate = st.sidebar.selectbox("UDP Data Rate", ["1Mbps", "2Mbps", "5Mbps"], index=1)
    pkt_size = st.sidebar.number_input("Packet Size (bytes)", min_value=64, max_value=2048, value=1024, step=64)
    sim_time = st.sidebar.slider("Simulation Time (seconds)", min_value=2.0, max_value=30.0, value=10.0, step=1.0)
    trace_cwnd = st.sidebar.checkbox("Enable Cwnd Tracing", value=True)

    run_btn = st.sidebar.button("🚀 Run Live Simulation", type="primary")

    st.subheader("Live Simulation Execution")
    st.write(f"Configure parameters in the sidebar and execute the real compiled NS-3.42 binary via subprocess.")

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

        with st.spinner("Executing discrete-event simulation in NS-3..."):
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
                cwnd_data["Cwnd_KB"] = cwnd_data["Cwnd"] / 1024.0
                st.line_chart(cwnd_data, x="Time", y="Cwnd_KB")
        else:
            st.error(f"Simulation failed with exit code {res.returncode}:\n{res.stderr}\n{res.stdout}")
