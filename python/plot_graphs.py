#!/usr/bin/env python3
"""
plot_graphs.py
Generate publication-quality graphs from the NS-3 simulation results:
1. Queue Size vs Packet Loss (%)
2. Queue Size vs Average Delay (ms)
3. Bottleneck Bandwidth vs Throughput (Mbps)
4. TCP vs UDP Packet Delivery Ratio (PDR %)
5. TCP Congestion Window (Cwnd) vs Time (s)

Each graph includes descriptive titles, axis labels with units, markers, and legends.
"""

import sys
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Style settings for academic report figures
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "lines.linewidth": 2,
    "lines.markersize": 7,
    "grid.alpha": 0.35,
    "grid.linestyle": "--"
})

def safe_numeric(val):
    """Convert string/object to float or np.nan safely."""
    try:
        if val == "N/A" or pd.isna(val):
            return np.nan
        return float(val)
    except Exception:
        return np.nan


def plot_queue_vs_loss(df, output_dir):
    """Plot 1: Queue Size vs Packet Loss (%) for TCP and UDP."""
    exp1 = df[df["Experiment"] == "1_QueueSize"].copy()
    if exp1.empty:
        print("Warning: No Experiment 1 data found for queue_vs_loss.")
        return

    exp1["QueueSize"] = exp1["QueueSize"].astype(int)
    exp1 = exp1.sort_values("QueueSize")

    exp1["TCP_LossPct_num"] = exp1["TCP_LossPct"].apply(safe_numeric)
    exp1["UDP_LossPct_num"] = exp1["UDP_LossPct"].apply(safe_numeric)

    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(exp1["QueueSize"], exp1["TCP_LossPct_num"], "o-", color="#d62728", label="TCP Packet Loss (%)")
    plt.plot(exp1["QueueSize"], exp1["UDP_LossPct_num"], "s--", color="#1f77b4", label="UDP Packet Loss (%)")

    plt.title("Effect of Bottleneck Queue Size on Packet Loss (Bandwidth = 2 Mbps)")
    plt.xlabel("Bottleneck Queue Size (Packets)")
    plt.ylabel("Packet Loss (%)")
    plt.xticks(exp1["QueueSize"].unique())
    plt.grid(True)
    plt.legend(loc="best")
    plt.tight_layout()

    out_file = os.path.join(output_dir, "queue_vs_loss.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")


def plot_queue_vs_delay(df, output_dir):
    """Plot 2: Queue Size vs Average Delay (ms) for TCP and UDP."""
    exp1 = df[df["Experiment"] == "1_QueueSize"].copy()
    if exp1.empty:
        print("Warning: No Experiment 1 data found for queue_vs_delay.")
        return

    exp1["QueueSize"] = exp1["QueueSize"].astype(int)
    exp1 = exp1.sort_values("QueueSize")

    exp1["TCP_Delay_num"] = exp1["TCP_Delay_ms"].apply(safe_numeric)
    exp1["UDP_Delay_num"] = exp1["UDP_Delay_ms"].apply(safe_numeric)

    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(exp1["QueueSize"], exp1["TCP_Delay_num"], "o-", color="#d62728", label="TCP Average Delay (ms)")
    plt.plot(exp1["QueueSize"], exp1["UDP_Delay_num"], "s--", color="#1f77b4", label="UDP Average Delay (ms)")

    plt.title("Effect of Bottleneck Queue Size on End-to-End Delay (Bufferbloat)")
    plt.xlabel("Bottleneck Queue Size (Packets)")
    plt.ylabel("Average Delay (ms)")
    plt.xticks(exp1["QueueSize"].unique())
    plt.grid(True)
    plt.legend(loc="best")
    plt.tight_layout()

    out_file = os.path.join(output_dir, "queue_vs_delay.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")


def plot_bandwidth_vs_throughput(df, output_dir):
    """Plot 3: Bottleneck Bandwidth vs Throughput (Mbps)."""
    exp2 = df[df["Experiment"] == "2_BottleneckBandwidth"].copy()
    if exp2.empty:
        print("Warning: No Experiment 2 data found for bandwidth_vs_throughput.")
        return

    # Extract numeric bandwidth from '1Mbps', '2Mbps', etc.
    exp2["Bw_num"] = exp2["BottleneckBw"].str.replace("Mbps", "").astype(float)
    exp2 = exp2.sort_values("Bw_num")

    exp2["TCP_Thpt_num"] = exp2["TCP_Throughput_Mbps"].apply(safe_numeric)
    exp2["UDP_Thpt_num"] = exp2["UDP_Throughput_Mbps"].apply(safe_numeric)

    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(exp2["Bw_num"], exp2["TCP_Thpt_num"], "o-", color="#2ca02c", label="TCP Throughput (Mbps)")
    plt.plot(exp2["Bw_num"], exp2["UDP_Thpt_num"], "s--", color="#ff7f0e", label="UDP Throughput (Mbps)")
    plt.plot(exp2["Bw_num"], exp2["Bw_num"], ":", color="gray", label="Total Bottleneck Capacity")

    plt.title("Bottleneck Bandwidth vs Achieved Throughput (Queue = 50 Packets)")
    plt.xlabel("Bottleneck Link Bandwidth (Mbps)")
    plt.ylabel("Throughput (Mbps)")
    plt.xticks(exp2["Bw_num"].unique())
    plt.grid(True)
    plt.legend(loc="best")
    plt.tight_layout()

    out_file = os.path.join(output_dir, "bandwidth_vs_throughput.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")


def plot_tcp_vs_udp_pdr(df, output_dir):
    """Plot 4: TCP vs UDP Packet Delivery Ratio (PDR %) across traffic modes."""
    exp3 = df[df["Experiment"] == "3_TrafficMode"].copy()
    if exp3.empty:
        print("Warning: No Experiment 3 data found for tcp_vs_udp_pdr.")
        return

    mode_order = ["tcp", "udp", "tcp-udp"]
    exp3["TrafficMode"] = pd.Categorical(exp3["TrafficMode"], categories=mode_order, ordered=True)
    exp3 = exp3.sort_values("TrafficMode")

    exp3["TCP_PDR_num"] = exp3["TCP_PDR"].apply(safe_numeric)
    exp3["UDP_PDR_num"] = exp3["UDP_PDR"].apply(safe_numeric)

    x = np.arange(len(mode_order))
    width = 0.35

    plt.figure(figsize=(8, 5), dpi=300)
    rects1 = plt.bar(x - width/2, exp3["TCP_PDR_num"].fillna(0), width, label="TCP PDR (%)", color="#1f77b4")
    rects2 = plt.bar(x + width/2, exp3["UDP_PDR_num"].fillna(0), width, label="UDP PDR (%)", color="#ff7f0e")

    plt.title("Comparison of Packet Delivery Ratio Across Traffic Modes")
    plt.xlabel("Traffic Mode")
    plt.ylabel("Packet Delivery Ratio (%)")
    plt.xticks(x, ["TCP Only", "UDP Only", "TCP + UDP (Contention)"])
    plt.ylim(0, 115)
    plt.grid(True, axis="y")
    plt.legend(loc="upper right")

    # Add text labels on bars
    for rect in rects1:
        h = rect.get_height()
        if h > 0:
            plt.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
    for rect in rects2:
        h = rect.get_height()
        if h > 0:
            plt.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tcp_vs_udp_pdr.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")


def plot_cwnd_vs_time(raw_dir, output_dir):
    """Plot 5: TCP Congestion Window (Cwnd) vs Time (s) for TCP Alone vs TCP+UDP Contention."""
    tcp_alone_file = os.path.join(raw_dir, "exp3_mode_tcp-cwnd.csv")
    tcp_contention_file = os.path.join(raw_dir, "exp3_mode_tcp-udp-cwnd.csv")

    if not os.path.exists(tcp_alone_file) or not os.path.exists(tcp_contention_file):
        print("Warning: One or more cwnd files missing for cwnd_vs_time plot.")
        return

    df_alone = pd.read_csv(tcp_alone_file)
    df_contention = pd.read_csv(tcp_contention_file)

    plt.figure(figsize=(10, 5), dpi=300)
    plt.plot(df_alone["Time"], df_alone["Cwnd"] / 1024, label="TCP Alone (No UDP Contention)", color="#2ca02c", alpha=0.9)
    plt.plot(df_contention["Time"], df_contention["Cwnd"] / 1024, label="TCP Sharing Link with 2 Mbps UDP", color="#d62728", alpha=0.85)

    plt.title("TCP Congestion Window Evolution: Uncontested vs UDP Contention")
    plt.xlabel("Simulation Time (Seconds)")
    plt.ylabel("Congestion Window (Kilobytes)")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()

    out_file = os.path.join(output_dir, "cwnd_vs_time.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    summary_file = os.path.join(base_dir, "results", "processed", "experiments_summary.csv")
    raw_dir = os.path.join(base_dir, "results", "raw")
    output_dir = os.path.join(base_dir, "graphs")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(summary_file):
        print(f"Error: Summary file '{summary_file}' not found. Run run_experiments.py first.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(summary_file)
    print("Generating analysis graphs...")
    plot_queue_vs_loss(df, output_dir)
    plot_queue_vs_delay(df, output_dir)
    plot_bandwidth_vs_throughput(df, output_dir)
    plot_tcp_vs_udp_pdr(df, output_dir)
    plot_cwnd_vs_time(raw_dir, output_dir)
    print("All graphs successfully generated in:", output_dir)


if __name__ == "__main__":
    main()
