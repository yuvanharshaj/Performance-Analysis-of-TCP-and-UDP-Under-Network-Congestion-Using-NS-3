# Performance Analysis of TCP and UDP Under Network Congestion Using NS-3

**Course:** Computer Networks (24CS53) | Academic IPCC Project  
**Author:** Student Implementation & Research  
**Simulator:** Network Simulator 3 (NS-3 v3.42) | C++20 | Python 3 | Streamlit  

[![NS-3 Version](https://img.shields.io/badge/NS--3-3.42-blue.svg)](https://www.nsnam.org/)
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Problem Statement
In computer networks, the transport layer determines how application data flows across constrained infrastructure. When connection-oriented, congestion-controlled **TCP** traffic and connectionless, unresponsive **UDP** traffic share a common, limited-capacity **bottleneck link**, significant contention occurs. 

This project simulates a dumbbell network topology in **NS-3** to systematically vary bottleneck bandwidth, queue buffer capacity, traffic competition modes, UDP rates, and packet sizes. We quantitatively evaluate:
- **Packet Delivery Ratio (PDR %)**
- **Packet Loss Percentage (%)**
- **Throughput (Mbps)**
- **Average End-to-End Delay (ms)**
- **Average Jitter (ms)**
- **TCP Congestion Window (Cwnd) Dynamic Behavior**

---

## 2. Project Objectives
1. **Model Realistic Bottleneck:** Implement a 6-node dumbbell topology in NS-3 C++ with edge links (10 Mbps, 2 ms) and a constrained bottleneck link (1–10 Mbps, 10 ms).
2. **Strict Queue Control:** Configure DropTail (FIFO) queuing on the bottleneck router and prevent edge-link buffer drops.
3. **Trace Dynamic Behavior:** Monitor packet-level flow statistics using `FlowMonitor` and real-time socket-level `CongestionWindow` evolution.
4. **Automated Analysis & Visualization:** Parse raw XML data into clean metrics, generate publication-grade graphs, and deploy an interactive Streamlit web dashboard.

---

## 3. Network Topology & Defaults
```text
TCP Source (N0) ────┐                                                  ┌──── TCP Destination (N4)
  10.1.1.1          │                                                  │       10.1.4.2
               [10Mbps, 2ms]                                      [10Mbps, 2ms]
                    │                                                  │
                    ▼                                                  ▼
             Router 1 (N2) ══════════ Bottleneck Link ══════════ Router 2 (N3)
                                      10.1.3.0/24
                                      Bandwidth: 1 - 10 Mbps
                    ▲                 Delay: 10 ms                     ▲
                    │                 Queue: DropTail (10-100 pkts)    │
               [10Mbps, 2ms]                                      [10Mbps, 2ms]
                    │                                                  │
UDP Source (N1) ────┘                                                  └──── UDP Destination (N5)
  10.1.2.1                                                             10.1.5.2
```

- **Normal / Access Links:** 10 Mbps data rate, 2 ms propagation delay
- **Bottleneck Link:** 2 Mbps default (1, 2, 5, 10 Mbps evaluated), 10 ms delay
- **Queue Management:** DropTail (FIFO), default 50 packets (10, 25, 50, 100 evaluated)
- **Simulation Duration:** 20.0 seconds default
- **Traffic Applications:**
  - **TCP:** `ns3::BulkSendApplication` (unbounded continuous byte stream) $\rightarrow$ `ns3::PacketSink` (port 50000)
  - **UDP:** `ns3::OnOffApplication` (constant rate 2 Mbps, 1024 B packets) $\rightarrow$ `ns3::PacketSink` (port 50001)

---

## 4. Repository Structure
```text
tcp-udp-congestion-analysis-ns3/
├── scratch/
│   ├── congestion-analysis.cc     # Main C++ NS-3 simulation model
│   └── test-connectivity.cc       # 2-node connectivity verification test
├── python/
│   ├── analyze_results.py         # Parses FlowMonitor XML to CSV with zero-guards
│   ├── plot_graphs.py             # Generates all 5 publication-quality graphs
│   └── run_experiments.py         # Automated runner for all 3 experiment sets
├── app/
│   └── app.py                     # Interactive Streamlit dashboard
├── results/
│   ├── raw/                       # FlowMonitor XML and Cwnd CSV outputs
│   └── processed/                 # Consolidated metrics summary CSV
├── graphs/                        # High-resolution (300 DPI) generated plots
├── docs/                          # Detailed academic report sections (01 to 07)
├── scripts/
│   ├── run_all.sh                 # Full simulation & plotting pipeline script
│   └── run_dashboard.bat          # Windows one-click dashboard launcher
├── tests/
│   └── test_analysis.py           # Automated unit tests (safe guards & parsing)
├── requirements.txt               # Python package dependencies
├── README.md                      # Comprehensive academic project documentation
├── PROJECT_STATUS.md              # Milestone tracking & verified command logs
└── LICENSE                        # MIT License
```

---

## 5. Installation & Build Instructions

### Prerequisites
- **Linux / Ubuntu 22.04+ (or Windows 11 with WSL2 Ubuntu 24.04)**
- **GCC / G++ 13+** with C++20 support, **CMake 3.28+**, **Ninja / GNU Make**
- **Python 3.10+** with `pip`

### Step 1: Install Dependencies
On Ubuntu / WSL:
```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake ninja-build git python3 python3-pip python3-pandas python3-numpy python3-matplotlib
```
On Windows:
```bash
pip install -r requirements.txt
```

### Step 2: Build NS-3 Simulation
Ensure NS-3 v3.42 is installed at `/home/yuvan/ns-allinone-3.42/ns-3.42/`:
```bash
# Link or copy scratch program
cp scratch/congestion-analysis.cc /home/yuvan/ns-allinone-3.42/ns-3.42/scratch/

# Build scratch target
cd /home/yuvan/ns-allinone-3.42/ns-3.42
./ns3 build scratch/congestion-analysis
```

### Step 3: Run Full Experiment Battery
Execute all 11 experiment runs automatically:
```bash
python python/run_experiments.py
```
This runs:
1. **Experiment 1 (Queue Variation):** 10, 25, 50, 100 packets
2. **Experiment 2 (Bandwidth Variation):** 1, 2, 5, 10 Mbps
3. **Experiment 3 (Traffic Mode):** TCP-only, UDP-only, TCP+UDP

### Step 4: Generate Publication Figures
```bash
python python/plot_graphs.py
```
Figures are saved to `graphs/`.

### Step 5: Launch Streamlit Web Dashboard
```bash
python -m streamlit run app/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 6. Experimental Results & Interpretation

The consolidated experimental summary (`results/processed/experiments_summary.csv`):

| Experiment | Run ID | Mode | Bottleneck BW | Queue Size | TCP Thpt (Mbps) | UDP Thpt (Mbps) | TCP Loss % | UDP Loss % |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Queue Size** | `exp1_queue_10p` | tcp-udp | 2 Mbps | 10 pkts | 0.0365 | 1.9753 | **51.52%** | 3.36% |
| **1. Queue Size** | `exp1_queue_25p` | tcp-udp | 2 Mbps | 25 pkts | 0.0804 | 1.9644 | 19.91% | 3.26% |
| **1. Queue Size** | `exp1_queue_50p` | tcp-udp | 2 Mbps | 50 pkts | 0.1117 | 1.9403 | 31.52% | 3.41% |
| **1. Queue Size** | `exp1_queue_100p`| tcp-udp | 2 Mbps | 100 pkts| 0.1118 | 1.9040 | 23.35% | 3.15% |
| **2. Bandwidth** | `exp2_bw_1Mbps` | tcp-udp | **1 Mbps** | 50 pkts | 0.0179 | 0.9819 | 38.58% | **50.04%** |
| **2. Bandwidth** | `exp2_bw_2Mbps` | tcp-udp | **2 Mbps** | 50 pkts | 0.1117 | 1.9403 | 31.52% | 3.41% |
| **2. Bandwidth** | `exp2_bw_5Mbps` | tcp-udp | **5 Mbps** | 50 pkts | **2.8073** | 2.0329 | 0.86% | 0.54% |
| **2. Bandwidth** | `exp2_bw_10Mbps`| tcp-udp | **10 Mbps**| 50 pkts | **7.8760** | 2.0482 | 0.04% | 0.09% |
| **3. Traffic Mode**| `exp3_mode_tcp` | tcp | 2 Mbps | 50 pkts | **1.9851** | *N/A* | **0.17%** | *N/A* |
| **3. Traffic Mode**| `exp3_mode_udp` | udp | 2 Mbps | 50 pkts | *N/A* | **1.9946** | *N/A* | **0.69%** |
| **3. Traffic Mode**| `exp3_mode_tcp-udp`| tcp-udp | 2 Mbps | 50 pkts | **0.1117** | **1.9403** | **31.52%** | 3.41% |

### Key Academic Findings
1. **TCP Starvation:** Under a 2 Mbps bottleneck, UDP sends continuously at 2 Mbps without backoff. TCP detects drops, cuts its congestion window, and achieves only 0.1117 Mbps throughput (a 94.4% drop compared to TCP alone).
2. **Bufferbloat:** Increasing queue capacity from 10 to 100 packets increased queuing delay from 47.9 ms to 448.9 ms without restoring fairness.
3. **Capacity Absorption:** Above 2 Mbps (at 5 Mbps and 10 Mbps), UDP reaches its transmission cap (~2.04 Mbps), allowing TCP to dynamically absorb all spare capacity (7.88 Mbps on 10 Mbps link) with near-zero loss (0.04%).

---

## 7. Cloud Deployment Notes (Streamlit Community Cloud)

> **Important Deployment Architecture:**  
> The dashboard is pre-configured to run in **Saved-Results Mode** for deployment to **Streamlit Community Cloud** (or any cloud container without a C++ toolchain or NS-3 installed).  
> All simulation runs are pre-computed locally, verified with real command output, and shipped directly within the repository in `results/raw/`, `results/processed/`, and `graphs/`.  
> On Streamlit Cloud:
> - The web app opens directly into the **Saved Results Browser**.
> - Users can interactively browse all 11 experiment runs, view dynamic charts, inspect metric cards, and download `.xml`, `.csv`, and `.png` artifacts over HTTPS.
> - No local NS-3 compilation or execution is attempted on the cloud host.

---

## 8. Troubleshooting Guide

| Issue / Error | Root Cause | Solution |
| :--- | :--- | :--- |
| `No root queue disc installed on device` | `TrafficControlLayer::Send` in NS-3.42 requires a root queue disc. | Use `tch.SetRootQueueDisc("ns3::FifoQueueDisc", "MaxSize", StringValue("50p"));` instead of `tch.Uninstall()`. |
| `streamlit is not recognized` | Streamlit installed in user scripts directory not in Windows PATH. | Launch via `python -m streamlit run app/app.py`. |
| `ImageMixin.image() got an unexpected keyword argument 'use_column_width'` | Deprecated keyword in Streamlit >= 1.30. | Use `use_container_width=True`. |
| Path spacing issues with WSL | Spaces in Windows directory paths (e.g. `CN PROJECT`). | Use symlink `/home/yuvan/project` pointing to workspace root inside WSL. |

---

## 9. Comprehensive Academic Viva Questions & Answers

**Q1: What is the fundamental difference between TCP and UDP flow control?**  
*Answer:* TCP implements closed-loop flow control (via receiver advertised window, `rwnd`) and congestion control (via congestion window, `cwnd`). UDP has no flow or congestion control; it injects datagrams directly into the IP layer as fast as the application generates them.

**Q2: What is AIMD, and how does it guarantee stability?**  
*Answer:* Additive Increase Multiplicative Decrease (AIMD). In congestion avoidance, TCP increases $Cwnd$ by 1 SMSS per RTT (additive increase) and halves $Cwnd$ upon packet loss (multiplicative decrease). Chiu & Jain (1989) proved mathematically that AIMD converges to fair and efficient equilibrium on shared bottleneck links.

**Q3: Why does TCP suffer severe throughput starvation when competing with UDP in a DropTail queue?**  
*Answer:* In a DropTail queue, all incoming packets share a single buffer. When buffer capacity is exceeded, new packets are dropped regardless of protocol. UDP does not reduce its transmission rate, so its packets continue filling the queue. TCP detects drops, throttles its $Cwnd$ exponentially, and yields bandwidth to the unresponsive UDP stream.

**Q4: What is Bufferbloat, and how does this project demonstrate it?**  
*Answer:* Bufferbloat occurs when oversized router buffers queue large numbers of packets, drastically increasing latency without improving throughput. In Experiment 1, increasing queue size from 10 to 100 packets increased average delay from 47.9 ms to 448.9 ms (a ~9x increase) while TCP throughput barely changed (0.036 Mbps to 0.111 Mbps).

**Q5: What is the role of FlowMonitor in NS-3?**  
*Answer:* `FlowMonitor` is an NS-3 architectural framework that passively snoops IP packets at network interfaces, computes per-flow performance statistics (delay, jitter, tx/rx bytes, tx/rx packets, lost packets), and serializes them to XML without altering simulation timing.

**Q6: How can routers prevent TCP starvation caused by unresponsive UDP flows?**  
*Answer:* By deploying Active Queue Management (AQM) such as Fair Queuing (FQ-CoDel, DRR, or WFQ), which isolates traffic into per-flow queues so unresponsive flows cannot overflow buffers allocated to responsive TCP flows.

---

## 10. Limitations & Future Scope

### Limitations
- Evaluates DropTail FIFO; does not model AQM (CoDel/RED) in the core battery.
- Single bottleneck topology; does not model multiple transit bottlenecks.
- Evaluates TCP NewReno; does not test delay-based algorithms like TCP BBR.

### Future Scope
- Benchmark Active Queue Management (FQ-CoDel, PIE) against DropTail.
- Incorporate TCP BBR and TCP Cubic under high-rate UDP contention.
- Evaluate RFC 3168 Explicit Congestion Notification (ECN) marking.
- Model multi-hop parking-lot topologies and wireless 5G/Wi-Fi bottleneck links.

---

## 11. License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
