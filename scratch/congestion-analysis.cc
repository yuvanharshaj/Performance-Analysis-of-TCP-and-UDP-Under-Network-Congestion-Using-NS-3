#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/traffic-control-module.h"

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <cstdlib>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("CongestionAnalysis");

// Global stream and state for cwnd tracing
static Ptr<OutputStreamWrapper> g_cwndStream;
static bool g_cwndTraced = false;

static void CwndTracer(uint32_t oldVal, uint32_t newVal)
{
    g_cwndTraced = true;
    *g_cwndStream->GetStream() << Simulator::Now().GetSeconds() << "," << newVal << "\n";
}

static void ConnectCwndTrace(std::string traceFile, uint32_t nodeId)
{
    AsciiTraceHelper ascii;
    g_cwndStream = ascii.CreateFileStream(traceFile);
    *g_cwndStream->GetStream() << "Time,Cwnd\n";

    std::string path = "/NodeList/" + std::to_string(nodeId) + "/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow";
    bool success = Config::ConnectWithoutContextFailSafe(path, MakeCallback(&CwndTracer));
    if (success)
    {
        NS_LOG_INFO("Successfully connected Cwnd trace to " << path);
    }
    else
    {
        NS_LOG_WARN("Could not connect Cwnd trace at " << path);
    }
}

int main(int argc, char *argv[])
{
    // Default parameters
    std::string bottleneckBandwidth = "2Mbps";
    std::string bottleneckDelay = "10ms";
    uint32_t queueSize = 50;
    std::string udpDataRate = "2Mbps";
    uint32_t packetSize = 1024;
    double simulationTime = 20.0;
    std::string trafficMode = "tcp-udp";
    std::string outputPrefix = "results/raw/run_default";
    bool enableCwndTracing = true;

    // Command-line parser
    CommandLine cmd(__FILE__);
    cmd.AddValue("bottleneckBandwidth", "Bandwidth of bottleneck link (e.g. 2Mbps)", bottleneckBandwidth);
    cmd.AddValue("bottleneckDelay", "Delay of bottleneck link (e.g. 10ms)", bottleneckDelay);
    cmd.AddValue("queueSize", "Queue size of bottleneck link in packets (e.g. 50)", queueSize);
    cmd.AddValue("udpDataRate", "Data rate for UDP OnOff source (e.g. 2Mbps)", udpDataRate);
    cmd.AddValue("packetSize", "Packet size in bytes (e.g. 1024)", packetSize);
    cmd.AddValue("simulationTime", "Total simulation duration in seconds (e.g. 20.0)", simulationTime);
    cmd.AddValue("trafficMode", "Traffic mode: 'tcp', 'udp', or 'tcp-udp'", trafficMode);
    cmd.AddValue("outputPrefix", "Prefix path for output files (e.g. results/raw/run1)", outputPrefix);
    cmd.AddValue("enableCwndTracing", "Enable TCP cwnd tracing (true/false)", enableCwndTracing);
    cmd.Parse(argc, argv);

    // Validation
    if (trafficMode != "tcp" && trafficMode != "udp" && trafficMode != "tcp-udp")
    {
        std::cerr << "ERROR: Invalid trafficMode '" << trafficMode << "'. Must be 'tcp', 'udp', or 'tcp-udp'." << std::endl;
        return 1;
    }
    if (queueSize < 1)
    {
        std::cerr << "ERROR: queueSize must be at least 1 packet." << std::endl;
        return 1;
    }
    if (packetSize < 64)
    {
        std::cerr << "ERROR: packetSize must be at least 64 bytes." << std::endl;
        return 1;
    }
    if (simulationTime <= 1.0)
    {
        std::cerr << "ERROR: simulationTime must be greater than 1.0 second." << std::endl;
        return 1;
    }

    // Ensure output directories exist
    std::filesystem::path p(outputPrefix);
    if (p.has_parent_path())
    {
        std::filesystem::create_directories(p.parent_path());
    }

    Time::SetResolution(Time::NS);

    std::cout << "========================================================\n"
              << "NS-3 TCP/UDP Congestion Simulation\n"
              << "--------------------------------------------------------\n"
              << "Traffic Mode         : " << trafficMode << "\n"
              << "Bottleneck Bandwidth : " << bottleneckBandwidth << "\n"
              << "Bottleneck Delay     : " << bottleneckDelay << "\n"
              << "Queue Size (packets) : " << queueSize << "\n"
              << "UDP Data Rate        : " << udpDataRate << "\n"
              << "Packet Size (bytes)  : " << packetSize << "\n"
              << "Simulation Time (s)  : " << simulationTime << "\n"
              << "Output Prefix        : " << outputPrefix << "\n"
              << "Cwnd Tracing         : " << (enableCwndTracing ? "Enabled" : "Disabled") << "\n"
              << "========================================================" << std::endl;

    // Topology:
    // Node 0: TCP Source
    // Node 1: UDP Source
    // Node 2: Router 1
    // Node 3: Router 2
    // Node 4: TCP Destination
    // Node 5: UDP Destination

    NodeContainer nodes;
    nodes.Create(6);

    Ptr<Node> tcpSrc = nodes.Get(0);
    Ptr<Node> udpSrc = nodes.Get(1);
    Ptr<Node> router1 = nodes.Get(2);
    Ptr<Node> router2 = nodes.Get(3);
    Ptr<Node> tcpDst = nodes.Get(4);
    Ptr<Node> udpDst = nodes.Get(5);

    // Access links: 10Mbps, 2ms delay
    PointToPointHelper accessLink;
    accessLink.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    accessLink.SetChannelAttribute("Delay", StringValue("2ms"));

    // Bottleneck link: configurable bandwidth and delay, DropTail queue
    PointToPointHelper bottleneckLink;
    bottleneckLink.SetDeviceAttribute("DataRate", StringValue(bottleneckBandwidth));
    bottleneckLink.SetChannelAttribute("Delay", StringValue(bottleneckDelay));
    bottleneckLink.SetQueue("ns3::DropTailQueue", "MaxSize", StringValue(std::to_string(queueSize) + "p"));

    // Install NetDevices
    NetDeviceContainer devTcpSrcR1 = accessLink.Install(tcpSrc, router1);
    NetDeviceContainer devUdpSrcR1 = accessLink.Install(udpSrc, router1);
    NetDeviceContainer devR1R2 = bottleneckLink.Install(router1, router2);
    NetDeviceContainer devR2TcpDst = accessLink.Install(router2, tcpDst);
    NetDeviceContainer devR2UdpDst = accessLink.Install(router2, udpDst);

    // Install Internet stack
    InternetStackHelper stack;
    stack.Install(nodes);

    // Configure Traffic Control (FIFO / DropTail QueueDisc)
    // Access links: large queue (1000p) so drops only happen on the bottleneck
    TrafficControlHelper tchAccess;
    tchAccess.SetRootQueueDisc("ns3::FifoQueueDisc", "MaxSize", StringValue("1000p"));
    tchAccess.Install(devTcpSrcR1);
    tchAccess.Install(devUdpSrcR1);
    tchAccess.Install(devR2TcpDst);
    tchAccess.Install(devR2UdpDst);

    // Bottleneck link: DropTail (FIFO) with user-configured queueSize packets
    TrafficControlHelper tchBottleneck;
    tchBottleneck.SetRootQueueDisc("ns3::FifoQueueDisc", "MaxSize", StringValue(std::to_string(queueSize) + "p"));
    tchBottleneck.Install(devR1R2);

    // Assign IP addresses
    Ipv4AddressHelper address;

    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer ifTcpSrcR1 = address.Assign(devTcpSrcR1);

    address.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer ifUdpSrcR1 = address.Assign(devUdpSrcR1);

    address.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer ifR1R2 = address.Assign(devR1R2);

    address.SetBase("10.1.4.0", "255.255.255.0");
    Ipv4InterfaceContainer ifR2TcpDst = address.Assign(devR2TcpDst);

    address.SetBase("10.1.5.0", "255.255.255.0");
    Ipv4InterfaceContainer ifR2UdpDst = address.Assign(devR2UdpDst);

    // Populate routing tables
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    uint16_t tcpPort = 50000;
    uint16_t udpPort = 50001;
    double appStartTime = 1.0;
    double appStopTime = simulationTime;

    // TCP Applications
    if (trafficMode == "tcp" || trafficMode == "tcp-udp")
    {
        // Destination Sink
        Address tcpSinkAddress(InetSocketAddress(Ipv4Address::GetAny(), tcpPort));
        PacketSinkHelper tcpSinkHelper("ns3::TcpSocketFactory", tcpSinkAddress);
        ApplicationContainer tcpSinkApp = tcpSinkHelper.Install(tcpDst);
        tcpSinkApp.Start(Seconds(0.0));
        tcpSinkApp.Stop(Seconds(simulationTime + 1.0));

        // Source BulkSend
        Address tcpRemoteAddress(InetSocketAddress(ifR2TcpDst.GetAddress(1), tcpPort));
        BulkSendHelper tcpSourceHelper("ns3::TcpSocketFactory", tcpRemoteAddress);
        tcpSourceHelper.SetAttribute("MaxBytes", UintegerValue(0)); // Unlimited
        tcpSourceHelper.SetAttribute("SendSize", UintegerValue(packetSize));
        ApplicationContainer tcpSourceApp = tcpSourceHelper.Install(tcpSrc);
        tcpSourceApp.Start(Seconds(appStartTime));
        tcpSourceApp.Stop(Seconds(appStopTime));

        // Trace cwnd
        if (enableCwndTracing)
        {
            std::string cwndFile = outputPrefix + "-cwnd.csv";
            Simulator::Schedule(Seconds(appStartTime + 0.00001), &ConnectCwndTrace, cwndFile, 0);
        }
    }

    // UDP Applications
    if (trafficMode == "udp" || trafficMode == "tcp-udp")
    {
        // Destination Sink
        Address udpSinkAddress(InetSocketAddress(Ipv4Address::GetAny(), udpPort));
        PacketSinkHelper udpSinkHelper("ns3::UdpSocketFactory", udpSinkAddress);
        ApplicationContainer udpSinkApp = udpSinkHelper.Install(udpDst);
        udpSinkApp.Start(Seconds(0.0));
        udpSinkApp.Stop(Seconds(simulationTime + 1.0));

        // Source OnOff
        Address udpRemoteAddress(InetSocketAddress(ifR2UdpDst.GetAddress(1), udpPort));
        OnOffHelper udpSourceHelper("ns3::UdpSocketFactory", udpRemoteAddress);
        udpSourceHelper.SetAttribute("DataRate", DataRateValue(DataRate(udpDataRate)));
        udpSourceHelper.SetAttribute("PacketSize", UintegerValue(packetSize));
        udpSourceHelper.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"));
        udpSourceHelper.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
        ApplicationContainer udpSourceApp = udpSourceHelper.Install(udpSrc);
        udpSourceApp.Start(Seconds(appStartTime));
        udpSourceApp.Stop(Seconds(appStopTime));
    }

    // FlowMonitor
    FlowMonitorHelper flowmonHelper;
    Ptr<FlowMonitor> flowMonitor = flowmonHelper.InstallAll();

    // Run simulation
    Simulator::Stop(Seconds(simulationTime + 1.0));
    Simulator::Run();

    // Serialize FlowMonitor results
    flowMonitor->CheckForLostPackets();
    std::string flowmonFile = outputPrefix + "-flowmon.xml";
    flowMonitor->SerializeToXmlFile(flowmonFile, true, true);

    Simulator::Destroy();

    std::cout << "Simulation completed successfully.\n"
              << "FlowMonitor output: " << flowmonFile << "\n";
    if (enableCwndTracing && (trafficMode == "tcp" || trafficMode == "tcp-udp"))
    {
        std::cout << "Cwnd trace output: " << outputPrefix + "-cwnd.csv" << "\n";
    }
    std::cout << "SIMULATION_SUCCESS" << std::endl;

    return 0;
}
