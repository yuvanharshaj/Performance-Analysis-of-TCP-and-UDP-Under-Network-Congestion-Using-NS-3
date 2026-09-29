# Project Report - Section 2: Literature Survey

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  

---

## 2.1 Transport Layer Paradigms

### 2.1.1 Transmission Control Protocol (TCP)
TCP is defined in RFC 793, with modern congestion control standards codified in RFC 5681 (Allman, Paxson, Blanton). TCP guarantees reliable, in-order byte-stream delivery using positive acknowledgments (ACKs), sequence numbering, and retransmission timers.

TCP's congestion control architecture operates via four core algorithms:
1. **Slow Start:** Exponential growth of the Congestion Window ($Cwnd \leftarrow Cwnd + SMSS$ per incoming ACK) until reaching the Slow Start Threshold ($ssthresh$).
2. **Congestion Avoidance:** Additive Increase Multiplicative Decrease (AIMD). Once $Cwnd \ge ssthresh$, $Cwnd$ increases linearly ($\approx 1 \text{ SMSS}$ per Round Trip Time):
   $$Cwnd \leftarrow Cwnd + \frac{SMSS \times SMSS}{Cwnd}$$
3. **Fast Retransmit:** Immediate retransmission of missing segments upon detecting 3 duplicate ACKs without waiting for a retransmission timeout (RTO).
4. **Fast Recovery:** Halving the congestion window and setting $ssthresh \leftarrow \max\left(\frac{\text{FlightSize}}{2}, 2 \times SMSS\right)$, maintaining packet flow in the pipe.

### 2.1.2 User Datagram Protocol (UDP)
UDP (RFC 768) provides a minimal transport service consisting of port multiplexing and an optional checksum. UDP does not establish a connection, maintain state, perform packet retransmissions, or regulate its transmission rate according to downstream buffer occupancy. Consequently, UDP is termed **unresponsive traffic**.

---

## 2.2 TCP vs UDP Interaction Over Bottleneck Links

When responsive (TCP) and unresponsive (UDP) traffic coexist:
1. **Unfairness & Starvation:** Because UDP continues transmitting at a fixed rate regardless of link congestion, packets occupying bottleneck buffers are predominantly UDP. TCP encounters drops, reduces its $Cwnd$, and enters backoff. This leads to **TCP starvation** in DropTail FIFO environments (Floyd & Fall, 1999, *Promoting the Use of End-to-End Congestion Control in the Internet*).
2. **Bufferbloat Phenomenon:** Coined by Gettys and Nichols (ACM Queue, 2011), bufferbloat refers to excessive latency introduced by oversized router buffers. DropTail queues hold hundreds of packets before dropping, delaying TCP's congestion feedback signal and causing end-to-end RTTs to spike by hundreds of milliseconds.

---

## 2.3 Role of Discrete-Event Network Simulation (NS-3)

Testing congestion phenomena in physical production testbeds is prohibitively expensive, difficult to instrument, and non-deterministic due to external traffic fluctuations.

The **Network Simulator 3 (NS-3)** is a discrete-event simulator written in C++ and Python (Henderson et al., *Network Simulations with the ns-3 Simulator*). In NS-3:
- Real protocol implementations (including full Linux TCP state machines, netfilter/traffic-control queuing disciplines, and IP routing) execute deterministically with high fidelity.
- Event scheduling is executed on a virtual timeline ($\Delta t$ simulated independent of wall-clock time).
- `ns-3::FlowMonitor` provides non-invasive, precise packet telemetry across every node in the topology.
