# Project Report - Section 7: Conclusion & Academic Summary

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  

---

## 7.1 Conclusion
This project systematically designed, implemented, and empirically evaluated the performance of TCP and UDP transport protocols under congested network conditions using the **NS-3 discrete-event network simulator**.

Through rigorous parametric experiments across varying bottleneck queue sizes, bottleneck bandwidth capacities, and traffic contention modes, several fundamental networking principles were conclusively verified:

1. **TCP Friendliness vs. UDP Inelasticity:** TCP's Additive Increase Multiplicative Decrease (AIMD) congestion control algorithm backs off exponentially when packet drops occur. In contrast, UDP sends at an unresponsive constant rate, monopolizing up to 98% of the shared bottleneck capacity and causing severe TCP starvation in standard DropTail queues.
2. **Bufferbloat Identification:** Increasing the bottleneck queue capacity from 10 packets to 100 packets increased average packet delay nearly ten-fold (from 47.9 ms to 448.9 ms) without solving throughput unfairness, providing empirical proof of bufferbloat.
3. **Bandwidth Headroom & Elasticity:** When bottleneck link capacity exceeds the inelastic UDP demand (e.g. at 5 Mbps and 10 Mbps), TCP dynamically expands its congestion window, efficiently absorbing all surplus bandwidth with minimal packet loss (< 1%).
4. **Reproducibility & Telemetry:** Coupling NS-3 C++ discrete-event simulations with FlowMonitor XML extraction, Python metric parsers, and a Streamlit dashboard produced an end-to-end reproducible research and educational environment.

---

## 7.2 IPCC Project Outcomes Summary
- **ABET / Program Outcomes (POs) Addressed:**
  - PO1 (Engineering Knowledge): Applied transport and network layer protocols, congestion control mathematics, and queuing models.
  - PO2 (Problem Analysis): Modeled and diagnosed bufferbloat, TCP throughput starvation, and congestion window collapse.
  - PO4 (Conduct Investigations of Complex Problems): Configured multi-variable simulation experiments (11 runs) with quantitative statistical evaluation.
  - PO5 (Modern Tool Usage): Utilized NS-3.42, C++20, Python 3, Pandas, Matplotlib, Git, and Streamlit.
