#!/usr/bin/env python3
"""
analyze_results.py
Parse NS-3 FlowMonitor XML results and compute network performance metrics:
- Packet Delivery Ratio (PDR %)
- Packet Loss (%)
- Throughput (Mbps)
- Average Delay (ms)
- Average Jitter (ms)

Guards against divide-by-zero by outputting 'N/A' (never NaN or crash).
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd


def parse_ns_time(val_str):
    """
    Parse NS-3 time strings like '+1.01432e+09ns', '1e+09ns', '+0.0ns', or raw floats.
    Returns time in seconds as float.
    """
    if not val_str:
        return 0.0
    val_str = str(val_str).strip()
    if val_str.startswith('+'):
        val_str = val_str[1:]
    if val_str.endswith('ns'):
        return float(val_str[:-2]) / 1e9
    if val_str.endswith('ms'):
        return float(val_str[:-2]) / 1e3
    if val_str.endswith('s'):
        return float(val_str[:-1])
    return float(val_str)


def parse_flowmon_xml(xml_file_path):
    """
    Parse an NS-3 FlowMonitor XML file and return a list of flow metric dictionaries.
    Gracefully handles missing or malformed files and zero-packet flows.
    """
    if not os.path.exists(xml_file_path):
        print(f"Error: File '{xml_file_path}' does not exist.", file=sys.stderr)
        return []

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML file '{xml_file_path}': {e}", file=sys.stderr)
        return []

    # Map FlowId to Classifier details (Source, Destination, Protocol, Ports)
    classifiers = {}
    classifier_elem = root.find("Ipv4FlowClassifier")
    if classifier_elem is not None:
        for flow in classifier_elem.findall("Flow"):
            flow_id = flow.get("flowId")
            src_addr = flow.get("sourceAddress")
            dst_addr = flow.get("destinationAddress")
            proto_num = flow.get("protocol")
            src_port = flow.get("sourcePort")
            dst_port = flow.get("destinationPort")

            # Map protocol number
            proto_name = "UNKNOWN"
            if proto_num == "6":
                proto_name = "TCP"
            elif proto_num == "17":
                proto_name = "UDP"

            classifiers[flow_id] = {
                "source": src_addr,
                "destination": dst_addr,
                "protocol": proto_name,
                "src_port": src_port,
                "dst_port": dst_port
            }

    flow_stats = []
    flow_stats_elem = root.find("FlowStats")
    if flow_stats_elem is not None:
        for flow in flow_stats_elem.findall("Flow"):
            flow_id = flow.get("flowId")
            tx_packets = int(flow.get("txPackets", 0))
            rx_packets = int(flow.get("rxPackets", 0))
            tx_bytes = int(flow.get("txBytes", 0))
            rx_bytes = int(flow.get("rxBytes", 0))
            lost_packets = int(flow.get("lostPackets", 0))

            t_first_tx = parse_ns_time(flow.get("timeFirstTxPacket", "0"))
            t_last_rx = parse_ns_time(flow.get("timeLastRxPacket", "0"))
            t_first_rx = parse_ns_time(flow.get("timeFirstRxPacket", "0"))

            # delaySum and jitterSum in seconds
            delay_sum_sec = parse_ns_time(flow.get("delaySum", "0"))
            jitter_sum_sec = parse_ns_time(flow.get("jitterSum", "0"))

            # Calculate duration for throughput
            if rx_packets > 0 and t_last_rx > t_first_tx:
                duration = t_last_rx - t_first_tx
            else:
                duration = 0.0

            # Guarded metric calculations
            if tx_packets > 0:
                pdr = round((rx_packets / tx_packets) * 100.0, 2)
                packet_loss_pct = round(((tx_packets - rx_packets) / tx_packets) * 100.0, 2)
            else:
                pdr = "N/A"
                packet_loss_pct = "N/A"

            if duration > 0.0 and rx_bytes > 0:
                throughput_mbps = round((rx_bytes * 8.0) / (duration * 1e6), 4)
            else:
                throughput_mbps = 0.0 if rx_packets == 0 else "N/A"

            if rx_packets > 0:
                avg_delay_ms = round((delay_sum_sec * 1000.0) / rx_packets, 3)
                avg_jitter_ms = round((jitter_sum_sec * 1000.0) / rx_packets, 3)
            else:
                avg_delay_ms = "N/A"
                avg_jitter_ms = "N/A"

            clf = classifiers.get(flow_id, {
                "source": "N/A", "destination": "N/A", "protocol": "N/A", "src_port": "N/A", "dst_port": "N/A"
            })

            flow_type = "Forward"
            # In our topology, port 50000 is TCP Sink, 50001 is UDP Sink
            if clf.get("dst_port") in ["50000", "50001"]:
                flow_type = f"{clf['protocol']} Forward"
            elif clf.get("src_port") in ["50000", "50001"]:
                flow_type = f"{clf['protocol']} ACK/Reverse"

            flow_stats.append({
                "FlowID": flow_id,
                "Protocol": clf.get("protocol", "UNKNOWN"),
                "FlowType": flow_type,
                "Source": f"{clf.get('source')}:{clf.get('src_port')}",
                "Destination": f"{clf.get('destination')}:{clf.get('dst_port')}",
                "TxPackets": tx_packets,
                "RxPackets": rx_packets,
                "LostPackets": lost_packets,
                "TxBytes": tx_bytes,
                "RxBytes": rx_bytes,
                "PDR_percent": pdr,
                "PacketLoss_percent": packet_loss_pct,
                "Throughput_Mbps": throughput_mbps,
                "AvgDelay_ms": avg_delay_ms,
                "AvgJitter_ms": avg_jitter_ms,
                "Duration_s": round(duration, 3) if duration > 0 else "N/A"
            })

    return flow_stats


def main():
    parser = argparse.ArgumentParser(description="Parse NS-3 FlowMonitor XML results.")
    parser.add_argument("xml_file", help="Path to input FlowMonitor XML file")
    parser.add_argument("--output", "-o", help="Optional CSV output file path")
    args = parser.parse_args()

    results = parse_flowmon_xml(args.xml_file)
    if not results:
        print("No valid flows found.")
        sys.exit(1)

    df = pd.DataFrame(results)
    print("\n--- Parsed FlowMonitor Metrics ---")
    print(df.to_string(index=False))

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"\nSaved parsed metrics to: {args.output}")


if __name__ == "__main__":
    main()
