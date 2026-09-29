# PROJECT STATUS

**Project:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  
**Course:** Computer Networks (24CS53) | Academic IPCC Project  
**Last Updated:** 2026-09-29  

---

## 1. Verified Environment Specifications

| Component | Exact Detected Version | Location / Host | Status |
| :--- | :--- | :--- | :---: |
| **Host OS** | Windows 11 Home (Build 10.0.26100) | Windows Host | ✅ Verified |
| **WSL Distro** | Ubuntu 24.04.4 LTS (Linux 5.15.167.4-microsoft-standard-WSL2) | WSL2 Subsystem | ✅ Verified |
| **C++ Compiler** | GCC / G++ 13.3.0 (`x86_64-linux-gnu`) with C++20 | WSL Ubuntu 24.04 | ✅ Verified |
| **Build System** | CMake 3.28.3, GNU Make 4.4.1 | WSL Ubuntu 24.04 | ✅ Verified |
| **NS-3 Version** | **NS-3.42** (`ns-allinone-3.42/ns-3.42`) | `/home/yuvan/ns-allinone-3.42/ns-3.42` | ✅ Built & Verified |
| **Python (WSL)**| Python 3.12.3 (numpy 1.26.4, pandas 2.1.4, matplotlib 3.6.3) | `/usr/bin/python3` in WSL | ✅ Verified |
| **Python (Win)**| Python 3.13.0 (pandas 3.0.2, numpy 2.4.4, matplotlib 3.10.8) | Windows Path | ✅ Verified |
| **Streamlit** | Streamlit v1.64.0 | Windows Python Environment | ✅ Tested & Active |
| **Git** | Git 2.43.0 (WSL) / 2.52.0 (Windows) | Git VCS | ✅ Verified |

---

## 2. Step-by-Step Testing & Verification Milestones

| Step # | Milestone / Stage Description | Verification Command & Actual Output | Status |
| :---: | :--- | :--- | :---: |
| **1** | Inspect environment (OS, compiler, Python, NS-3) | System detection confirmed Ubuntu 24.04, G++ 13.3, NS-3.42, Python 3.12/3.13 | ✅ **DONE** |
| **2** | Verify NS-3 smallest example | `./ns3 run hello-simulator` $\rightarrow$ `Hello Simulator` (Exit 0)<br>`./ns3 run first` $\rightarrow$ client sent 1024B, server received 1024B (Exit 0) | ✅ **DONE** |
| **3** | Minimal scratch compile + 2-node connectivity | `./ns3 run test-connectivity` $\rightarrow$ `TEST_CONNECTIVITY_SUCCESS` (Exit 0) | ✅ **DONE** |
| **4** | Full topology (6 nodes) + IPv4 routing | `congestion-analysis.cc` compiled with 5 subnets and global routing | ✅ **DONE** |
| **5** | Add TCP flow $\rightarrow$ confirm received | `scratch/congestion-analysis-default --trafficMode=tcp` $\rightarrow$ 1922 packets received | ✅ **DONE** |
| **6** | Add UDP flow $\rightarrow$ confirm received | `scratch/congestion-analysis-default --trafficMode=udp` $\rightarrow$ 1.995 Mbps received | ✅ **DONE** |
| **7** | Add bottleneck $\rightarrow$ confirm drops occur | `FifoQueueDisc` (DropTail) installed; 50 packets lost under contention | ✅ **DONE** |
| **8** | Add FlowMonitor $\rightarrow$ confirm XML output | `results/raw/test_tcp_udp-flowmon.xml` (30,132 bytes) parsed successfully | ✅ **DONE** |
| **9** | Add Cwnd tracing $\rightarrow$ confirm non-empty data | `results/raw/test_tcp_udp-cwnd.csv` confirmed non-empty (`Time,Cwnd` records) | ✅ **DONE** |
| **10** | Python analysis $\rightarrow$ generate graphs | `plot_graphs.py` generated 5 PNG plots (300 DPI) in `graphs/` | ✅ **DONE** |
| **11** | Launch Streamlit app $\rightarrow$ verify dashboard | Streamlit server tested on `http://localhost:8501` (HTTP Status: 200) | ✅ **DONE** |
| **12** | Run all 3 required experiments | `run_experiments.py` executed 11 simulation runs, wrote `experiments_summary.csv` | ✅ **DONE** |
| **13** | Review outputs & prepare academic docs | Generated comprehensive docs in `docs/` (01 to 07) and full `README.md` | ✅ **DONE** |

---

## 3. Experimental Data Summary

All 11 required experiment runs are executed, verified, and saved in `results/raw/` and `results/processed/experiments_summary.csv`:

```text
Experiment 1: Queue Size Variation (Bandwidth = 2 Mbps fixed)
- 10 packets  : TCP PDR = 48.48%, UDP PDR = 96.64%, TCP Thpt = 0.0365 Mbps, TCP Loss = 51.52%
- 25 packets  : TCP PDR = 80.09%, UDP PDR = 96.74%, TCP Thpt = 0.0804 Mbps, TCP Loss = 19.91%
- 50 packets  : TCP PDR = 68.48%, UDP PDR = 96.59%, TCP Thpt = 0.1117 Mbps, TCP Loss = 31.52%
- 100 packets : TCP PDR = 76.65%, UDP PDR = 96.85%, TCP Thpt = 0.1118 Mbps, TCP Loss = 23.35%

Experiment 2: Bottleneck Bandwidth Variation (Queue = 50 packets fixed)
- 1 Mbps  : TCP Thpt = 0.0179 Mbps, UDP Thpt = 0.9819 Mbps (Severe congestion; UDP loss = 50.04%)
- 2 Mbps  : TCP Thpt = 0.1117 Mbps, UDP Thpt = 1.9403 Mbps (Contention; TCP loss = 31.52%)
- 5 Mbps  : TCP Thpt = 2.8073 Mbps, UDP Thpt = 2.0329 Mbps (Capacity surplus; TCP loss = 0.86%)
- 10 Mbps : TCP Thpt = 7.8760 Mbps, UDP Thpt = 2.0482 Mbps (Full absorption; TCP loss = 0.04%)

Experiment 3: Traffic Mode Comparison (Queue = 50 packets, Bandwidth = 2 Mbps)
- TCP Only  : TCP Thpt = 1.9851 Mbps (99.25% link utilization), Loss = 0.17%
- UDP Only  : UDP Thpt = 1.9946 Mbps, Loss = 0.69%
- TCP + UDP : TCP Thpt = 0.1117 Mbps (Starvation), UDP Thpt = 1.9403 Mbps, TCP Loss = 31.52%
```

---

## 4. Git Commits & Version History

| Commit | Hash | Description |
| :---: | :---: | :--- |
| 1 | `init` | Project initialization, directory scaffold, license, and requirements |
| 2 | `ns3-setup` | NS-3.42 build verification and 2-node connectivity scratch test |
| 3 | `sim-pipeline`| Full congestion analysis C++ simulation with DropTail queue and Cwnd tracing |
| 4 | `analytics` | FlowMonitor parser (`analyze_results.py`) and plot generator (`plot_graphs.py`) |
| 5 | `experiments`| Automated experiment suite execution (`run_experiments.py`) and summary CSV |
| 6 | `dashboard` | Streamlit web application (`app/app.py`) with Saved-Results cloud compatibility |
| 7 | `docs-complete`| Full academic documentation (docs/ 01-07), tests, and comprehensive README |
