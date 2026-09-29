# Project Report - Section 6: Limitations and Future Scope

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  

---

## 6.1 Limitations of the Current Study

1. **DropTail Queue Exclusivity:** The simulation models classic First-In First-Out (FIFO) DropTail queuing. Modern routers increasingly implement Active Queue Management (AQM) such as CoDel, FQ-CoDel, or RED.
2. **Single Bottleneck Topology:** The network topology assumes a single, isolated bottleneck link. Real-world transit paths often feature multi-hop, fluctuating bottleneck scenarios (parking lot topologies).
3. **Homogeneous TCP Variant:** The experiments primarily utilize TCP NewReno / Linux Reno. Advanced modern congestion control algorithms (such as TCP BBR, Cubic, or Vegas) utilize delay-based or model-based feedback and may behave differently when coexisting with UDP.
4. **Synthetic Traffic Profile:** UDP traffic is modeled as continuous constant-bit-rate (CBR) traffic. Real-world UDP traffic (e.g. Adaptive Bitrate Video over QUIC/UDP, voice with silence suppression) exhibits variable bit rates (VBR).

---

## 6.2 Future Scope

1. **Active Queue Management (AQM) Comparison:**
   Evaluate how modern queuing disciplines (`ns3::FqCoDelQueueDisc`, `ns3::CobaltQueueDisc`, and `ns3::PieQueueDisc`) mitigate bufferbloat and enforce fair bandwidth allocation between TCP and UDP.
2. **TCP Variant Shootout Under UDP Flood:**
   Benchmark TCP Cubic, TCP BBR (Bottleneck Bandwidth and RTT), and TCP Westwood against unresponsive UDP streams.
3. **Explicit Congestion Notification (ECN):**
   Implement RFC 3168 ECN marking to assess whether early congestion signals allow TCP to avoid packet drops and maintain higher throughput during moderate UDP bursts.
4. **Wireless / 5G Bottlenecks:**
   Extend the topology to include wireless links (Wi-Fi 802.11ax or 5G NR cellular) with channel fading and MAC-layer retransmissions to observe cross-layer congestion dynamics.
