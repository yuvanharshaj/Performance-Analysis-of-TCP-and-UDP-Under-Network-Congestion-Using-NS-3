# Project Report - Section 5: Experimental Results and Analysis

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  

---

## 5.1 Experiment 1: Effect of Bottleneck Queue Size

**Conditions:** Bottleneck Bandwidth = 2 Mbps, Delay = 10 ms, UDP Rate = 2 Mbps, Packet Size = 1024 B, Duration = 20 s.

| Queue Size (pkts) | TCP Loss (%) | UDP Loss (%) | TCP Throughput (Mbps) | UDP Throughput (Mbps) | TCP Avg Delay (ms) | UDP Avg Delay (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | 51.52% | 3.36% | 0.0365 | 1.9753 | 47.93 | 49.30 |
| **25** | 19.91% | 3.26% | 0.0804 | 1.9644 | 114.73 | 118.66 |
| **50** | 31.52% | 3.41% | 0.1117 | 1.9403 | 215.34 | 229.62 |
| **100**| 23.35% | 3.15% | 0.1118 | 1.9040 | 419.68 | 448.91 |

### Key Findings & Academic Interpretation:
1. **TCP Starvation:** With UDP sending at 2 Mbps over a 2 Mbps bottleneck, UDP monopolizes ~95-98% of total capacity. TCP is severely throttled due to packet losses causing repeated multiplicative decreases.
2. **Bufferbloat:** As queue size increases from 10 to 100 packets, average queuing delay grows nearly tenfold (from 47 ms to ~420 ms). While larger queues provide a slight throughput benefit to TCP, they induce severe latency penalties without resolving the fundamental contention unfairness.

---

## 5.2 Experiment 2: Effect of Bottleneck Bandwidth

**Conditions:** Queue Size = 50 packets, Delay = 10 ms, UDP Rate = 2 Mbps, Packet Size = 1024 B, Duration = 20 s.

| Bottleneck Bandwidth | TCP Throughput (Mbps) | UDP Throughput (Mbps) | Total Utilization | TCP Loss (%) | UDP Loss (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Mbps** | 0.0179 | 0.9819 | ~1.00 Mbps (100%) | 38.58% | 50.04% |
| **2 Mbps** | 0.1117 | 1.9403 | ~2.05 Mbps (100%) | 31.52% | 3.41% |
| **5 Mbps** | 2.8073 | 2.0329 | ~4.84 Mbps (96.8%)| 0.86% | 0.54% |
| **10 Mbps**| 7.8760 | 2.0482 | ~9.92 Mbps (99.2%)| 0.04% | 0.09% |

### Key Findings & Academic Interpretation:
1. **Severe Congestion (1 Mbps):** When link bandwidth is half of the UDP transmission rate, UDP suffers 50% packet loss, and TCP is almost completely starved (0.0179 Mbps).
2. **Transition to Ample Capacity (5 Mbps & 10 Mbps):** Once bottleneck bandwidth exceeds the 2 Mbps UDP demand, UDP throughput caps at ~2.04 Mbps (its source generation rate). TCP's AIMD algorithm dynamically expands its congestion window to claim all residual bandwidth (2.81 Mbps on a 5 Mbps link, 7.88 Mbps on a 10 Mbps link) with virtually zero packet loss.

---

## 5.3 Experiment 3: Traffic Mode Comparison

**Conditions:** Bottleneck Bandwidth = 2 Mbps, Queue Size = 50 packets, Delay = 10 ms, Duration = 20 s.

| Traffic Mode | TCP Throughput (Mbps) | UDP Throughput (Mbps) | TCP PDR (%) | UDP PDR (%) | TCP Loss (%) | UDP Loss (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TCP Only** | **1.9851** | *N/A* | **99.83%** | *N/A* | **0.17%** | *N/A* |
| **UDP Only** | *N/A* | **1.9946** | *N/A* | **99.31%** | *N/A* | **0.69%** |
| **TCP + UDP** | **0.1117** | **1.9403** | **68.48%** | **96.59%** | **31.52%** | **3.41%** |

### Key Findings & Academic Interpretation:
- **TCP Alone:** In the absence of unresponsive traffic, TCP achieves near-perfect link utilization (1.985 Mbps on a 2 Mbps link, 99.25% efficiency) with only 0.17% loss.
- **UDP Alone:** UDP transmits steadily at 1.995 Mbps with 0.69% loss.
- **TCP + UDP Contention:** When combined, UDP throughput remains unaffected (1.940 Mbps), while TCP throughput collapses by 94.4% (from 1.985 Mbps down to 0.112 Mbps). This demonstrates why Active Queue Management (AQM) and Fair Queuing are critical in modern routers.

---

## 5.4 TCP Congestion Window (Cwnd) Dynamic Analysis

Examining `graphs/cwnd_vs_time.png`:
- **Uncontested TCP:** Exhibits smooth, regular sawtooth patterns characteristic of AIMD. The window grows linearly during Congestion Avoidance and drops cleanly by 50% upon packet loss, recovering quickly.
- **TCP Under UDP Contention:** The window is repeatedly forced down to minimum values (often 1 SMSS / 1024 bytes) due to frequent drops and timeouts induced by the unresponsive UDP packet flood, preventing TCP from sustaining high throughput.
