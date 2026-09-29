# Performance Analysis of TCP and UDP Under Network Congestion Using NS-3

**Course:** Computer Networks (24CS53) — IPCC Academic Project

---

## Problem Statement

Simulate a small NS-3 network where TCP and UDP share a limited-bandwidth
bottleneck link. Vary bandwidth, queue size, traffic mode, UDP rate, and packet
size. Measure packet delivery ratio, packet loss, throughput, delay, jitter, and
TCP congestion-window behavior. Compare TCP vs UDP under normal and congested
conditions.

## Objectives

1. Build a dumbbell topology with a configurable bottleneck link in NS-3.
2. Generate TCP (BulkSend) and UDP (OnOff) traffic through the bottleneck.
3. Collect metrics via FlowMonitor and TCP cwnd tracing.
4. Analyze results with Python (pandas, matplotlib) and visualize on a
   Streamlit dashboard.
5. Run experiments varying queue size, bandwidth, and traffic mode.

## Network Topology

```
TCP Source ─┐                                          ┌─ TCP Destination
            ├─ Router1 ── Bottleneck Link ── Router2 ──┤
UDP Source ─┘                                          └─ UDP Destination
```

### Default Parameters

| Parameter           | Value         |
|---------------------|---------------|
| Normal links        | 10 Mbps, 2 ms |
| Bottleneck link     | 2 Mbps, 10 ms |
| Queue discipline    | DropTail, 50 packets |
| Simulation time     | 20 s          |
| UDP packet size     | 1024 B        |
| UDP data rate       | 2 Mbps        |
| Traffic mode        | tcp-udp       |

## Metrics Collected

- **Packet Delivery Ratio (PDR):** received / transmitted × 100
- **Packet Loss %:** (transmitted − received) / transmitted × 100
- **Throughput (Mbps):** received bytes × 8 / (duration × 10⁶)
- **Average Delay (ms):** delay sum / received packets
- **Average Jitter (ms):** jitter sum / received packets
- **TCP Congestion Window (cwnd):** traced over time via NS-3 callback

## Experiments

| # | Variable           | Values                        | Fixed             |
|---|--------------------|-------------------------------|-------------------|
| 1 | Queue size         | 10, 25, 50, 100 packets      | BW = 2 Mbps       |
| 2 | Bottleneck BW      | 1, 2, 5, 10 Mbps             | Queue = 50        |
| 3 | Traffic mode       | tcp-only, udp-only, tcp-udp   | Default params    |

## Tech Stack

| Component   | Version                        |
|-------------|--------------------------------|
| OS          | Windows 11 + WSL Ubuntu 24.04  |
| NS-3        | *(to be installed)*            |
| C++ compiler| *(to be installed in WSL)*     |
| Python      | 3.12.3 (WSL)                   |
| Git         | 2.43.0 (WSL) / 2.52.0 (Win)   |
| Streamlit   | *(to be installed)*            |

## Deployment Mode

**Saved-results mode:** All experiments are pre-run locally inside WSL.
Result files (XML, CSV, PNG) are committed to the repo. The Streamlit
dashboard deployed on Streamlit Community Cloud browses and visualizes
these saved results over HTTPS — no live NS-3 execution on the cloud host.

## Repository Structure

```
tcp-udp-congestion-analysis-ns3/
├── scratch/congestion-analysis.cc   # NS-3 simulation source
├── python/
│   ├── analyze_results.py           # FlowMonitor XML → CSV
│   ├── plot_graphs.py               # Generate all graphs
│   └── run_experiments.py           # Batch experiment runner
├── app/app.py                       # Streamlit dashboard
├── results/
│   ├── raw/                         # FlowMonitor XML + cwnd CSV
│   └── processed/                   # Cleaned analysis CSV
├── graphs/                          # Generated plot images
├── docs/                            # Report sections
├── scripts/                         # Helper scripts
├── tests/                           # Test scripts
├── requirements.txt
├── README.md
├── PROJECT_STATUS.md
├── .gitignore
└── LICENSE
```

## Installation & Build

*(Will be filled after NS-3 is installed and verified.)*

## How to Run

*(Will be filled after the simulation pipeline is verified.)*

## Result Interpretation

*(Will be filled after experiments are complete.)*

## Troubleshooting

*(Will be filled during development.)*

## Viva Questions

*(Will be added in docs/.)*

## Limitations

- Single bottleneck (dumbbell) topology only.
- Fixed TCP variant (NS-3 default: TcpNewReno or TcpCubic).
- No wireless or real-world traffic patterns.

## Future Scope

- Compare multiple TCP variants (Cubic, Reno, BBR).
- Add background traffic and bursty sources.
- Extend to multi-bottleneck or wireless topologies.
- Real-time dashboard with live NS-3 execution.

## License

MIT License — see [LICENSE](LICENSE).
