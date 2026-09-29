# Project Report - Section 1: Introduction

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  
**Project Type:** Academic IPCC (Integrated Professional Core Course) Project  

---

## 1.1 Motivation
In modern packet-switched communication networks, the Internet Protocol (IP) serves as the universal network layer. However, the transport layer determines how user applications interact with network resources. The two dominant transport protocols:
1. **Transmission Control Protocol (TCP):** A connection-oriented, reliable protocol incorporating closed-loop feedback mechanisms for flow and congestion control (RFC 793, RFC 5681).
2. **User Datagram Protocol (UDP):** A connectionless, lightweight, unreliable transport mechanism with no built-in congestion feedback (RFC 768).

In real-world networks—such as campus networks, edge routers, and broadband gateways—TCP traffic (web browsing, secure file transfers, media streaming) and UDP traffic (VoIP, video conferencing, live streaming, DNS) converge and compete over shared links with constrained capacities (bottlenecks).

When bottleneck routers experience congestion, their queues fill up. Because UDP flows do not reduce their transmission rate upon packet drop, they aggressively fill network buffers. In contrast, TCP flows detect packet loss and back off exponentially. This phenomenon often leads to severe **TCP throughput starvation** and excessive queuing delays, known as **bufferbloat**. Understanding these dynamics empirically is fundamental to computer network engineering.

---

## 1.2 Problem Statement
Simulate a dumbbell topology in the NS-3 discrete-event network simulator where TCP and UDP traffic streams concurrently traverse a limited-capacity bottleneck point-to-point link. Systematically evaluate and compare the network performance of TCP and UDP by varying:
1. **Bottleneck Queue Size:** 10, 25, 50, and 100 packets.
2. **Bottleneck Bandwidth:** 1 Mbps, 2 Mbps, 5 Mbps, and 10 Mbps.
3. **Traffic Competition Mode:** TCP-only, UDP-only, and TCP+UDP concurrent contention.

Quantitatively measure and analyze key Quality of Service (QoS) metrics:
- **Packet Delivery Ratio (PDR %)**
- **Packet Loss Percentage (%)**
- **Throughput (Mbps)**
- **Average End-to-End Delay (ms)**
- **Average Jitter (ms)**
- **TCP Congestion Window (Cwnd) Dynamic Behavior**

---

## 1.3 Project Objectives
1. **Network Modeling:** Construct a modular, reproducible 6-node dumbbell topology in NS-3 using C++ point-to-point links, IPv4 addressing, and global static routing.
2. **Congestion & Queue Management:** Enforce drop-tail (FIFO) queuing on the bottleneck link while eliminating artificial traffic shaping on edge access links.
3. **Traffic Generation:** Deploy continuous `BulkSendApplication` (TCP Reno/NewReno) and rate-controlled `OnOffApplication` (UDP) sources.
4. **Fine-Grained Telemetry:** Capture packet-level metrics using `ns-3::FlowMonitor` and real-time TCP state transitions via socket trace sources (`CongestionWindow`).
5. **Data Pipeline & Interactive Dashboard:** Build automated Python analysis scripts (`analyze_results.py`, `plot_graphs.py`, `run_experiments.py`) and a Streamlit dashboard with dual operation modes (Saved Results for cloud deployment and Live Simulation for local testing).
