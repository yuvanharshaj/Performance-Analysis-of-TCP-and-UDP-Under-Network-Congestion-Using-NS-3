# Project Report - Section 3: System Design

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  

---

## 3.1 Network Topology
The system models a classic **dumbbell (bottleneck) topology** consisting of 6 nodes:
- **Node 0 ($N_0$):** TCP Source (BulkSend sender)
- **Node 1 ($N_1$):** UDP Source (OnOff constant-rate sender)
- **Node 2 ($N_2$):** Ingress Gateway Router (Router 1)
- **Node 3 ($N_3$):** Egress Gateway Router (Router 2)
- **Node 4 ($N_4$):** TCP Destination (PacketSink on port 50000)
- **Node 5 ($N_5$):** UDP Destination (PacketSink on port 50001)

### Topology Schematic
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

---

## 3.2 Link Configurations and Addressing Scheme

| Link Segment | Endpoints | Data Rate | Propagation Delay | Subnet IP Range | Queue Discipline |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TCP Access (In)** | $N_0 \leftrightarrow N_2$ | 10 Mbps | 2 ms | `10.1.1.0/24` | FIFO (1000 packets) |
| **UDP Access (In)** | $N_1 \leftrightarrow N_2$ | 10 Mbps | 2 ms | `10.1.2.0/24` | FIFO (1000 packets) |
| **Bottleneck Link** | $N_2 \leftrightarrow N_3$ | **1 - 10 Mbps** | **10 ms** | `10.1.3.0/24` | **DropTail FIFO (10-100 packets)** |
| **TCP Access (Out)**| $N_3 \leftrightarrow N_4$ | 10 Mbps | 2 ms | `10.1.4.0/24` | FIFO (1000 packets) |
| **UDP Access (Out)**| $N_3 \leftrightarrow N_5$ | 10 Mbps | 2 ms | `10.1.5.0/24` | FIFO (1000 packets) |

---

## 3.3 Traffic Application Parameters

### TCP Flow Specification
- **Sender Application:** `ns3::BulkSendApplication` (transfers unbounded byte stream as fast as allowed by TCP congestion window).
- **Socket Factory:** `ns3::TcpSocketFactory` (default TCP NewReno / Linux Reno).
- **Destination Sink:** `ns3::PacketSink` listening on port `50000`.
- **Application Active Window:** Starts at $t = 1.0\text{ s}$, stops at $t = 20.0\text{ s}$.
- **Segment Size:** Configurable (default: 1024 bytes).

### UDP Flow Specification
- **Sender Application:** `ns3::OnOffApplication` configured in deterministic CBR mode:
  - `OnTime`: Constant 1.0 s
  - `OffTime`: Constant 0.0 s
  - `DataRate`: Configurable (default: 2 Mbps)
- **Socket Factory:** `ns3::UdpSocketFactory`.
- **Destination Sink:** `ns3::PacketSink` listening on port `50001`.
- **Application Active Window:** Starts at $t = 1.0\text{ s}$, stops at $t = 20.0\text{ s}$.
- **Packet Size:** Configurable (default: 1024 bytes).

---

## 3.4 Mathematical Metric Formulations

All computed metrics incorporate strict divide-by-zero handling:

1. **Packet Delivery Ratio (PDR %):**
   $$\text{PDR} = \begin{cases} \left(\frac{RxPackets}{TxPackets}\right) \times 100, & \text{if } TxPackets > 0 \\ \text{"N/A"}, & \text{otherwise} \end{cases}$$

2. **Packet Loss Percentage (%):**
   $$\text{Loss \%} = \begin{cases} \left(\frac{TxPackets - RxPackets}{TxPackets}\right) \times 100, & \text{if } TxPackets > 0 \\ \text{"N/A"}, & \text{otherwise} \end{cases}$$

3. **Throughput (Mbps):**
   $$\text{Throughput} = \begin{cases} \frac{RxBytes \times 8}{(t_{\text{lastRx}} - t_{\text{firstTx}}) \times 10^6}, & \text{if } RxPackets > 0 \land \Delta t > 0 \\ 0.0, & \text{if } RxPackets = 0 \\ \text{"N/A"}, & \text{otherwise} \end{cases}$$

4. **Average End-to-End Delay (ms):**
   $$\overline{Delay} = \begin{cases} \frac{\sum Delay}{RxPackets \times 10^6}, & \text{if } RxPackets > 0 \\ \text{"N/A"}, & \text{otherwise} \end{cases}$$

5. **Average Jitter (ms):**
   $$\overline{Jitter} = \begin{cases} \frac{\sum Jitter}{RxPackets \times 10^6}, & \text{if } RxPackets > 0 \\ \text{"N/A"}, & \text{otherwise} \end{cases}$$
