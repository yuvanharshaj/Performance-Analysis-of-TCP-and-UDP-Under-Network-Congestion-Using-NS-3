#!/usr/bin/env python3
"""
run_experiments.py
Automates running the NS-3 simulation experiments:
1. Queue Size Variation: 10, 25, 50, 100 packets (Bandwidth = 2Mbps)
2. Bottleneck Bandwidth Variation: 1Mbps, 2Mbps, 5Mbps, 10Mbps (Queue = 50 packets)
3. Traffic Mode Comparison: TCP-only, UDP-only, TCP+UDP (Bandwidth = 2Mbps, Queue = 50 packets)

Logs each command + pass/fail, writes a consolidated summary CSV to results/processed/experiments_summary.csv.
"""

import sys
import os
import subprocess
import shutil
import pandas as pd
from analyze_results import parse_flowmon_xml


def get_ns3_binary_cmd():
    """
    Detect whether we are running inside WSL/Linux or Windows,
    and return the command prefix to execute the compiled NS-3 binary.
    """
    linux_binary = "/home/yuvan/ns-allinone-3.42/ns-3.42/build/scratch/ns3.42-congestion-analysis-default"
    lib_path = "/home/yuvan/ns-allinone-3.42/ns-3.42/build/lib"

    if sys.platform.startswith("linux"):
        if os.path.exists(linux_binary):
            return ["env", f"LD_LIBRARY_PATH={lib_path}", linux_binary], False
        else:
            raise RuntimeError(f"NS-3 binary not found at {linux_binary}")
    elif sys.platform == "win32":
        # Check if WSL is available
        wsl_check = shutil.which("wsl")
        if wsl_check:
            return ["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-c"], True
        else:
            raise RuntimeError("WSL is required to execute NS-3 on Windows.")
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")


def to_wsl_path(win_path):
    """
    Convert a Windows path inside the project repository to /home/yuvan/project/...
    to completely avoid spaces in paths.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rel_path = os.path.relpath(os.path.abspath(win_path), base_dir)
    rel_path_posix = rel_path.replace("\\", "/")
    return f"/home/yuvan/project/{rel_path_posix}"


def run_single_simulation(params, output_prefix):
    """
    Run one NS-3 simulation with specified parameters.
    Returns (success: bool, flowmon_xml_path: str, cwnd_csv_path: str)
    """
    cmd_prefix, is_wsl_wrapper = get_ns3_binary_cmd()

    # Paths in host OS
    flowmon_xml_host = f"{output_prefix}-flowmon.xml"
    cwnd_csv_host = f"{output_prefix}-cwnd.csv"

    # Make parent dirs on host
    os.makedirs(os.path.dirname(os.path.abspath(output_prefix)), exist_ok=True)

    # Determine target prefix path for the binary
    if is_wsl_wrapper:
        target_prefix = to_wsl_path(output_prefix)
        binary_cmd = f"LD_LIBRARY_PATH=/home/yuvan/ns-allinone-3.42/ns-3.42/build/lib /home/yuvan/ns-allinone-3.42/ns-3.42/build/scratch/ns3.42-congestion-analysis-default"
        args_str = (
            f" --bottleneckBandwidth={params.get('bottleneckBandwidth', '2Mbps')}"
            f" --bottleneckDelay={params.get('bottleneckDelay', '10ms')}"
            f" --queueSize={params.get('queueSize', 50)}"
            f" --udpDataRate={params.get('udpDataRate', '2Mbps')}"
            f" --packetSize={params.get('packetSize', 1024)}"
            f" --simulationTime={params.get('simulationTime', 20.0)}"
            f" --trafficMode={params.get('trafficMode', 'tcp-udp')}"
            f" --outputPrefix={target_prefix}"
            f" --enableCwndTracing={str(params.get('enableCwndTracing', True)).lower()}"
        )
        full_cmd = ["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-c", binary_cmd + args_str]
    else:
        full_cmd = cmd_prefix + [
            f"--bottleneckBandwidth={params.get('bottleneckBandwidth', '2Mbps')}",
            f"--bottleneckDelay={params.get('bottleneckDelay', '10ms')}",
            f"--queueSize={params.get('queueSize', 50)}",
            f"--udpDataRate={params.get('udpDataRate', '2Mbps')}",
            f"--packetSize={params.get('packetSize', 1024)}",
            f"--simulationTime={params.get('simulationTime', 20.0)}",
            f"--trafficMode={params.get('trafficMode', 'tcp-udp')}",
            f"--outputPrefix={output_prefix}",
            f"--enableCwndTracing={str(params.get('enableCwndTracing', True)).lower()}"
        ]

    print(f"Running: {' '.join(full_cmd[:4])} ... [Prefix: {output_prefix}]")
    result = subprocess.run(full_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FAILED (Exit Code {result.returncode}):\n{result.stderr}\n{result.stdout}", file=sys.stderr)
        return False, flowmon_xml_host, cwnd_csv_host

    if not os.path.exists(flowmon_xml_host):
        print(f"FAILED: Expected FlowMonitor output '{flowmon_xml_host}' was not created.", file=sys.stderr)
        return False, flowmon_xml_host, cwnd_csv_host

    return True, flowmon_xml_host, cwnd_csv_host


def extract_summary_record(exp_name, run_id, params, flow_stats):
    """
    Extract aggregated TCP and UDP metrics from the parsed flow statistics.
    """
    rec = {
        "Experiment": exp_name,
        "RunID": run_id,
        "TrafficMode": params.get("trafficMode", "tcp-udp"),
        "BottleneckBw": params.get("bottleneckBandwidth", "2Mbps"),
        "BottleneckDelay": params.get("bottleneckDelay", "10ms"),
        "QueueSize": params.get("queueSize", 50),
        "UdpRate": params.get("udpDataRate", "2Mbps"),
        "PacketSize": params.get("packetSize", 1024),
        "SimTime": params.get("simulationTime", 20.0),
        # TCP metrics
        "TCP_Tx": "N/A", "TCP_Rx": "N/A", "TCP_Lost": "N/A",
        "TCP_PDR": "N/A", "TCP_LossPct": "N/A", "TCP_Throughput_Mbps": "N/A",
        "TCP_Delay_ms": "N/A", "TCP_Jitter_ms": "N/A",
        # UDP metrics
        "UDP_Tx": "N/A", "UDP_Rx": "N/A", "UDP_Lost": "N/A",
        "UDP_PDR": "N/A", "UDP_LossPct": "N/A", "UDP_Throughput_Mbps": "N/A",
        "UDP_Delay_ms": "N/A", "UDP_Jitter_ms": "N/A",
        "Status": "PASS"
    }

    for f in flow_stats:
        flow_type = f.get("FlowType", "")
        proto = f.get("Protocol", "")
        if "TCP Forward" in flow_type or (proto == "TCP" and "ACK" not in flow_type):
            rec["TCP_Tx"] = f.get("TxPackets", "N/A")
            rec["TCP_Rx"] = f.get("RxPackets", "N/A")
            rec["TCP_Lost"] = f.get("LostPackets", "N/A")
            rec["TCP_PDR"] = f.get("PDR_percent", "N/A")
            rec["TCP_LossPct"] = f.get("PacketLoss_percent", "N/A")
            rec["TCP_Throughput_Mbps"] = f.get("Throughput_Mbps", "N/A")
            rec["TCP_Delay_ms"] = f.get("AvgDelay_ms", "N/A")
            rec["TCP_Jitter_ms"] = f.get("AvgJitter_ms", "N/A")
        elif "UDP Forward" in flow_type or proto == "UDP":
            rec["UDP_Tx"] = f.get("TxPackets", "N/A")
            rec["UDP_Rx"] = f.get("RxPackets", "N/A")
            rec["UDP_Lost"] = f.get("LostPackets", "N/A")
            rec["UDP_PDR"] = f.get("PDR_percent", "N/A")
            rec["UDP_LossPct"] = f.get("PacketLoss_percent", "N/A")
            rec["UDP_Throughput_Mbps"] = f.get("Throughput_Mbps", "N/A")
            rec["UDP_Delay_ms"] = f.get("AvgDelay_ms", "N/A")
            rec["UDP_Jitter_ms"] = f.get("AvgJitter_ms", "N/A")

    return rec


def run_all_experiments():
    """
    Executes the 3 required experiment sets:
    1. Queue Size Variation: 10, 25, 50, 100 packets
    2. Bottleneck Bandwidth Variation: 1Mbps, 2Mbps, 5Mbps, 10Mbps
    3. Traffic Mode Comparison: TCP, UDP, TCP+UDP
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_raw = os.path.join(base_dir, "results", "raw")
    results_proc = os.path.join(base_dir, "results", "processed")
    os.makedirs(results_raw, exist_ok=True)
    os.makedirs(results_proc, exist_ok=True)

    summary_records = []

    print("\n========================================================")
    print("STARTING NS-3 EXPERIMENT SUITE")
    print("========================================================\n")

    # -------------------------------------------------------------------------
    # Experiment 1: Queue Size Variation (10, 25, 50, 100 packets)
    # -------------------------------------------------------------------------
    print(">>> Experiment 1: Queue Size Variation (Bandwidth = 2Mbps fixed) <<<")
    queue_sizes = [10, 25, 50, 100]
    for q in queue_sizes:
        run_id = f"exp1_queue_{q}p"
        output_prefix = os.path.join(results_raw, run_id)
        params = {
            "bottleneckBandwidth": "2Mbps",
            "bottleneckDelay": "10ms",
            "queueSize": q,
            "udpDataRate": "2Mbps",
            "packetSize": 1024,
            "simulationTime": 20.0,
            "trafficMode": "tcp-udp",
            "enableCwndTracing": True
        }
        success, flowmon_xml, cwnd_csv = run_single_simulation(params, output_prefix)
        if not success:
            print(f"ABORTING: Experiment 1 run {run_id} failed!")
            sys.exit(1)
        flows = parse_flowmon_xml(flowmon_xml)
        rec = extract_summary_record("1_QueueSize", run_id, params, flows)
        summary_records.append(rec)
        print(f"  [PASS] {run_id} -> TCP PDR: {rec['TCP_PDR']}%, UDP PDR: {rec['UDP_PDR']}%, TCP Throughput: {rec['TCP_Throughput_Mbps']} Mbps\n")

    # -------------------------------------------------------------------------
    # Experiment 2: Bottleneck Bandwidth Variation (1, 2, 5, 10 Mbps)
    # -------------------------------------------------------------------------
    print(">>> Experiment 2: Bottleneck Bandwidth Variation (Queue = 50 packets fixed) <<<")
    bandwidths = ["1Mbps", "2Mbps", "5Mbps", "10Mbps"]
    for bw in bandwidths:
        run_id = f"exp2_bw_{bw}"
        output_prefix = os.path.join(results_raw, run_id)
        params = {
            "bottleneckBandwidth": bw,
            "bottleneckDelay": "10ms",
            "queueSize": 50,
            "udpDataRate": "2Mbps",
            "packetSize": 1024,
            "simulationTime": 20.0,
            "trafficMode": "tcp-udp",
            "enableCwndTracing": True
        }
        success, flowmon_xml, cwnd_csv = run_single_simulation(params, output_prefix)
        if not success:
            print(f"ABORTING: Experiment 2 run {run_id} failed!")
            sys.exit(1)
        flows = parse_flowmon_xml(flowmon_xml)
        rec = extract_summary_record("2_BottleneckBandwidth", run_id, params, flows)
        summary_records.append(rec)
        print(f"  [PASS] {run_id} -> TCP Throughput: {rec['TCP_Throughput_Mbps']} Mbps, UDP Throughput: {rec['UDP_Throughput_Mbps']} Mbps\n")

    # -------------------------------------------------------------------------
    # Experiment 3: Traffic Mode Comparison (TCP-only, UDP-only, TCP+UDP)
    # -------------------------------------------------------------------------
    print(">>> Experiment 3: Traffic Mode Comparison (Queue = 50, BW = 2Mbps) <<<")
    modes = ["tcp", "udp", "tcp-udp"]
    for mode in modes:
        run_id = f"exp3_mode_{mode}"
        output_prefix = os.path.join(results_raw, run_id)
        params = {
            "bottleneckBandwidth": "2Mbps",
            "bottleneckDelay": "10ms",
            "queueSize": 50,
            "udpDataRate": "2Mbps",
            "packetSize": 1024,
            "simulationTime": 20.0,
            "trafficMode": mode,
            "enableCwndTracing": True
        }
        success, flowmon_xml, cwnd_csv = run_single_simulation(params, output_prefix)
        if not success:
            print(f"ABORTING: Experiment 3 run {run_id} failed!")
            sys.exit(1)
        flows = parse_flowmon_xml(flowmon_xml)
        rec = extract_summary_record("3_TrafficMode", run_id, params, flows)
        summary_records.append(rec)
        print(f"  [PASS] {run_id} -> Mode: {mode}, TCP Thpt: {rec['TCP_Throughput_Mbps']}, UDP Thpt: {rec['UDP_Throughput_Mbps']}\n")

    summary_df = pd.DataFrame(summary_records)
    summary_csv = os.path.join(results_proc, "experiments_summary.csv")
    summary_df.to_csv(summary_csv, index=False)
    print("========================================================")
    print(f"ALL EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print(f"Consolidated Summary written to: {summary_csv}")
    print("========================================================")
    print("\nSummary Table:")
    print(summary_df[["Experiment", "RunID", "TrafficMode", "BottleneckBw", "QueueSize", "TCP_Throughput_Mbps", "UDP_Throughput_Mbps", "TCP_LossPct", "UDP_LossPct"]].to_string(index=False))


if __name__ == "__main__":
    run_all_experiments()
