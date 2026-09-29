# Project Report - Section 4: Implementation Details

**Course:** Computer Networks (24CS53)  
**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  

---

## 4.1 NS-3 C++ Simulation (`scratch/congestion-analysis.cc`)

### 4.1.1 Command-Line Interface and Validation
The C++ simulation utilizes `ns3::CommandLine` to accept dynamic operational parameters without recompilation:
```cpp
CommandLine cmd(__FILE__);
cmd.AddValue("bottleneckBandwidth", "Bandwidth of bottleneck link", bottleneckBandwidth);
cmd.AddValue("bottleneckDelay", "Delay of bottleneck link", bottleneckDelay);
cmd.AddValue("queueSize", "Queue size of bottleneck link in packets", queueSize);
cmd.AddValue("udpDataRate", "Data rate for UDP OnOff source", udpDataRate);
cmd.AddValue("packetSize", "Packet size in bytes", packetSize);
cmd.AddValue("simulationTime", "Simulation duration in seconds", simulationTime);
cmd.AddValue("trafficMode", "Traffic mode: 'tcp', 'udp', or 'tcp-udp'", trafficMode);
cmd.AddValue("outputPrefix", "Prefix path for output files", outputPrefix);
cmd.AddValue("enableCwndTracing", "Enable TCP cwnd tracing", enableCwndTracing);
cmd.Parse(argc, argv);
```
Parameter validation prevents invalid simulations (e.g., `queueSize < 1`, `packetSize < 64`, `simulationTime <= 1.0`, or unapproved `trafficMode`).

### 4.1.2 Queue Discipline Configuration
To ensure drops occur exclusively at the bottleneck link while maintaining valid root queue discs across all interfaces:
```cpp
// Access links: High capacity buffer (1000 packets)
TrafficControlHelper tchAccess;
tchAccess.SetRootQueueDisc("ns3::FifoQueueDisc", "MaxSize", StringValue("1000p"));
tchAccess.Install(devTcpSrcR1);
tchAccess.Install(devUdpSrcR1);
tchAccess.Install(devR2TcpDst);
tchAccess.Install(devR2UdpDst);

// Bottleneck link: DropTail FIFO queue sized strictly to queueSize
TrafficControlHelper tchBottleneck;
tchBottleneck.SetRootQueueDisc("ns3::FifoQueueDisc", "MaxSize", StringValue(std::to_string(queueSize) + "p"));
tchBottleneck.Install(devR1R2);
```

### 4.1.3 Congestion Window Tracing
The TCP Congestion Window trace source (`ns3::TcpSocketBase::CongestionWindow`) is connected asynchronously via:
```cpp
static void CwndTracer(uint32_t oldVal, uint32_t newVal)
{
    *g_cwndStream->GetStream() << Simulator::Now().GetSeconds() << "," << newVal << "\n";
}

static void ConnectCwndTrace(std::string traceFile, uint32_t nodeId)
{
    AsciiTraceHelper ascii;
    g_cwndStream = ascii.CreateFileStream(traceFile);
    *g_cwndStream->GetStream() << "Time,Cwnd\n";
    std::string path = "/NodeList/" + std::to_string(nodeId) + "/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow";
    Config::ConnectWithoutContextFailSafe(path, MakeCallback(&CwndTracer));
}

// Scheduled 10 microseconds after application start (when socket is allocated)
Simulator::Schedule(Seconds(appStartTime + 0.00001), &ConnectCwndTrace, cwndFile, 0);
```

---

## 4.2 Python Analytics and Plotting Pipeline

1. **`analyze_results.py`:**
   - Parses the XML document produced by `ns3::FlowMonitorHelper`.
   - Maps Flow IDs using `<Ipv4FlowClassifier>` into forward TCP, forward UDP, and TCP ACK flows.
   - Extracts nanosecond timestamps, byte counts, and packet losses, and returns structured dictionaries with zero-division guards.
2. **`run_experiments.py`:**
   - Coordinates automated batch execution of Experiment 1 (Queue), Experiment 2 (Bandwidth), and Experiment 3 (Traffic Mode).
   - Generates unique file prefixes for every run (`results/raw/exp1_queue_10p`, etc.).
   - Consolidates results into `results/processed/experiments_summary.csv`.
3. **`plot_graphs.py`:**
   - Generates high-resolution publication figures (300 DPI) for queue vs loss, queue vs delay, bandwidth vs throughput, PDR comparison, and cwnd vs time.

---

## 4.3 Streamlit Interactive Dashboard (`app/app.py`)
- **Saved Results Browser:** Primary cloud mode. Visualizes shipped artifacts (`.xml`, `.csv`, `.png`) without requiring a C++ compiler or NS-3 install.
- **Live NS-3 Simulation Runner:** Local WSL/Linux mode. Employs `subprocess.run` with list arguments (never shell string) and timeouts to trigger on-demand NS-3 runs directly from the UI.
