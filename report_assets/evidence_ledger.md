# Evidence Ledger: Network Congestion Performance Analysis

This ledger documents the definitive source, exact file location, column/row reference, and verification status for all quantitative performance metrics, link topologies, and empirical simulation values presented in the project report.

| Report Value | Metric Description | Source File / Path | Row / Column or URL | Date Checked | Verification Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| 6 Nodes | Total nodes in dumbbell topology (2 sources, 2 routers, 2 destinations) | `scratch/congestion-analysis.cc` | Line 127 | 2026-11-16 | VERIFIED |
| 10 Mbps | Access link bandwidth (Node 0/1 to R1, R2 to Node 4/5) | `scratch/congestion-analysis.cc` | Line 138 | 2026-11-16 | VERIFIED |
| 2 ms | Access link one-way propagation delay | `scratch/congestion-analysis.cc` | Line 139 | 2026-11-16 | VERIFIED |
| 1000 p | Access link DropTail queue capacity (drop-free access) | `scratch/congestion-analysis.cc` | Line 161 | 2026-11-16 | VERIFIED |
| 10 ms | Bottleneck link one-way propagation delay | `scratch/congestion-analysis.cc` | Line 51, 144 | 2026-11-16 | VERIFIED |
| DropTail (FifoQueueDisc) | Bottleneck queue discipline | `scratch/congestion-analysis.cc` | Line 145, 169 | 2026-11-16 | VERIFIED |
| 1024 Bytes | Application packet payload size | `scratch/congestion-analysis.cc` | Line 54, 212, 239 | 2026-11-16 | VERIFIED |
| 1.0 s | Application traffic start time | `scratch/congestion-analysis.cc` | Line 195, 214, 243 | 2026-11-16 | VERIFIED |
| 20.0 s | Simulation stop time (19.0 s active duration) | `scratch/congestion-analysis.cc` | Line 55, 196, 252 | 2026-11-16 | VERIFIED |
| 50000 | TCP Sink destination listening port | `scratch/congestion-analysis.cc` | Line 193 | 2026-11-16 | VERIFIED |
| 50001 | UDP Sink destination listening port | `scratch/congestion-analysis.cc` | Line 194 | 2026-11-16 | VERIFIED |
| 10.1.1.0/24 | TCP Sender to Router 1 subnet | `scratch/congestion-analysis.cc` | Line 175 | 2026-11-16 | VERIFIED |
| 10.1.2.0/24 | UDP Sender to Router 1 subnet | `scratch/congestion-analysis.cc` | Line 178 | 2026-11-16 | VERIFIED |
| 10.1.3.0/24 | Router 1 to Router 2 bottleneck subnet | `scratch/congestion-analysis.cc` | Line 181 | 2026-11-16 | VERIFIED |
| 10.1.4.0/24 | Router 2 to TCP Receiver subnet | `scratch/congestion-analysis.cc` | Line 184 | 2026-11-16 | VERIFIED |
| 10.1.5.0/24 | Router 2 to UDP Receiver subnet | `scratch/congestion-analysis.cc` | Line 187 | 2026-11-16 | VERIFIED |
| 165 pkts | exp1_queue_10p (1_QueueSize) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 80 pkts | exp1_queue_10p (1_QueueSize) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 85 pkts | exp1_queue_10p (1_QueueSize) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 48.48% | exp1_queue_10p (1_QueueSize) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 51.52% | exp1_queue_10p (1_QueueSize) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.0365 Mbps | exp1_queue_10p (1_QueueSize) TCP Throughput | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 77.855 ms | exp1_queue_10p (1_QueueSize) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 2.399 ms | exp1_queue_10p (1_QueueSize) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 0, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp1_queue_10p (1_QueueSize) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4482 pkts | exp1_queue_10p (1_QueueSize) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 156 pkts | exp1_queue_10p (1_QueueSize) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 96.64% | exp1_queue_10p (1_QueueSize) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 3.36% | exp1_queue_10p (1_QueueSize) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9753 Mbps | exp1_queue_10p (1_QueueSize) UDP Throughput | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 101.378 ms | exp1_queue_10p (1_QueueSize) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.257 ms | exp1_queue_10p (1_QueueSize) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 0, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 427 pkts | exp1_queue_25p (1_QueueSize) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 342 pkts | exp1_queue_25p (1_QueueSize) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 85 pkts | exp1_queue_25p (1_QueueSize) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 80.09% | exp1_queue_25p (1_QueueSize) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 19.91% | exp1_queue_25p (1_QueueSize) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.0804 Mbps | exp1_queue_25p (1_QueueSize) TCP Throughput | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 71.970 ms | exp1_queue_25p (1_QueueSize) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 3.054 ms | exp1_queue_25p (1_QueueSize) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 1, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp1_queue_25p (1_QueueSize) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4487 pkts | exp1_queue_25p (1_QueueSize) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 151 pkts | exp1_queue_25p (1_QueueSize) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 96.74% | exp1_queue_25p (1_QueueSize) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 3.26% | exp1_queue_25p (1_QueueSize) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9644 Mbps | exp1_queue_25p (1_QueueSize) UDP Throughput | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 225.857 ms | exp1_queue_25p (1_QueueSize) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.283 ms | exp1_queue_25p (1_QueueSize) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 1, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 330 pkts | exp1_queue_50p (1_QueueSize) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 226 pkts | exp1_queue_50p (1_QueueSize) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 104 pkts | exp1_queue_50p (1_QueueSize) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 68.48% | exp1_queue_50p (1_QueueSize) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 31.52% | exp1_queue_50p (1_QueueSize) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.1117 Mbps | exp1_queue_50p (1_QueueSize) TCP Throughput | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 264.346 ms | exp1_queue_50p (1_QueueSize) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 2.460 ms | exp1_queue_50p (1_QueueSize) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 2, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp1_queue_50p (1_QueueSize) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4480 pkts | exp1_queue_50p (1_QueueSize) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 158 pkts | exp1_queue_50p (1_QueueSize) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 96.59% | exp1_queue_50p (1_QueueSize) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 3.41% | exp1_queue_50p (1_QueueSize) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9403 Mbps | exp1_queue_50p (1_QueueSize) UDP Throughput | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 429.205 ms | exp1_queue_50p (1_QueueSize) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.320 ms | exp1_queue_50p (1_QueueSize) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 2, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 501 pkts | exp1_queue_100p (1_QueueSize) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 384 pkts | exp1_queue_100p (1_QueueSize) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 117 pkts | exp1_queue_100p (1_QueueSize) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 76.65% | exp1_queue_100p (1_QueueSize) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 23.35% | exp1_queue_100p (1_QueueSize) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.1118 Mbps | exp1_queue_100p (1_QueueSize) TCP Throughput | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 480.958 ms | exp1_queue_100p (1_QueueSize) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 2.571 ms | exp1_queue_100p (1_QueueSize) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 3, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp1_queue_100p (1_QueueSize) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4492 pkts | exp1_queue_100p (1_QueueSize) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 146 pkts | exp1_queue_100p (1_QueueSize) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 96.85% | exp1_queue_100p (1_QueueSize) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 3.15% | exp1_queue_100p (1_QueueSize) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9040 Mbps | exp1_queue_100p (1_QueueSize) UDP Throughput | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 815.338 ms | exp1_queue_100p (1_QueueSize) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.386 ms | exp1_queue_100p (1_QueueSize) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 3, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 127 pkts | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 78 pkts | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 46 pkts | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 61.42% | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 38.58% | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.0179 Mbps | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Throughput | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 372.314 ms | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 21.951 ms | exp2_bw_1Mbps (2_BottleneckBandwidth) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 4, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 2317 pkts | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 2321 pkts | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 49.96% | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 50.04% | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 0.9819 Mbps | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Throughput | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 839.253 ms | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.803 ms | exp2_bw_1Mbps (2_BottleneckBandwidth) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 4, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 330 pkts | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 226 pkts | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 104 pkts | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 68.48% | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 31.52% | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.1117 Mbps | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Throughput | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 264.346 ms | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 2.460 ms | exp2_bw_2Mbps (2_BottleneckBandwidth) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 5, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4480 pkts | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 158 pkts | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 96.59% | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 3.41% | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9403 Mbps | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Throughput | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 429.205 ms | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.320 ms | exp2_bw_2Mbps (2_BottleneckBandwidth) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 5, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 11578 pkts | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 11479 pkts | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 99 pkts | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 99.14% | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 0.86% | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 2.8073 Mbps | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Throughput | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 103.127 ms | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 1.181 ms | exp2_bw_5Mbps (2_BottleneckBandwidth) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 6, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4613 pkts | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 25 pkts | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 99.46% | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 0.54% | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 2.0329 Mbps | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Throughput | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 99.962 ms | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.643 ms | exp2_bw_5Mbps (2_BottleneckBandwidth) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 6, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 32065 pkts | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 32053 pkts | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 12 pkts | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 99.96% | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 0.04% | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 7.8760 Mbps | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Throughput | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 58.073 ms | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.607 ms | exp2_bw_10Mbps (2_BottleneckBandwidth) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 7, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4634 pkts | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 4 pkts | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 99.91% | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 0.09% | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 2.0482 Mbps | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Throughput | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 58.480 ms | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.191 ms | exp2_bw_10Mbps (2_BottleneckBandwidth) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 7, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 8284 pkts | exp3_mode_tcp (3_TrafficMode) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 8270 pkts | exp3_mode_tcp (3_TrafficMode) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 14 pkts | exp3_mode_tcp (3_TrafficMode) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 99.83% | exp3_mode_tcp (3_TrafficMode) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 0.17% | exp3_mode_tcp (3_TrafficMode) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9851 Mbps | exp3_mode_tcp (3_TrafficMode) TCP Throughput | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 212.340 ms | exp3_mode_tcp (3_TrafficMode) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 2.261 ms | exp3_mode_tcp (3_TrafficMode) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 8, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp3_mode_udp (3_TrafficMode) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4606 pkts | exp3_mode_udp (3_TrafficMode) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 32 pkts | exp3_mode_udp (3_TrafficMode) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 99.31% | exp3_mode_udp (3_TrafficMode) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 0.69% | exp3_mode_udp (3_TrafficMode) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9946 Mbps | exp3_mode_udp (3_TrafficMode) UDP Throughput | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 280.176 ms | exp3_mode_udp (3_TrafficMode) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.147 ms | exp3_mode_udp (3_TrafficMode) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 9, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 330 pkts | exp3_mode_tcp-udp (3_TrafficMode) TCP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_Tx' | 2026-11-16 | VERIFIED |
| 226 pkts | exp3_mode_tcp-udp (3_TrafficMode) TCP Received Packets | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_Rx' | 2026-11-16 | VERIFIED |
| 104 pkts | exp3_mode_tcp-udp (3_TrafficMode) TCP Lost Packets | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_Lost' | 2026-11-16 | VERIFIED |
| 68.48% | exp3_mode_tcp-udp (3_TrafficMode) TCP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_PDR' | 2026-11-16 | VERIFIED |
| 31.52% | exp3_mode_tcp-udp (3_TrafficMode) TCP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_LossPct' | 2026-11-16 | VERIFIED |
| 0.1117 Mbps | exp3_mode_tcp-udp (3_TrafficMode) TCP Throughput | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 264.346 ms | exp3_mode_tcp-udp (3_TrafficMode) TCP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_Delay_ms' | 2026-11-16 | VERIFIED |
| 2.460 ms | exp3_mode_tcp-udp (3_TrafficMode) TCP Average Jitter | `results/processed/experiments_summary.csv` | Row 10, Col 'TCP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 4638 pkts | exp3_mode_tcp-udp (3_TrafficMode) UDP Transmitted Packets | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_Tx' | 2026-11-16 | VERIFIED |
| 4480 pkts | exp3_mode_tcp-udp (3_TrafficMode) UDP Received Packets | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_Rx' | 2026-11-16 | VERIFIED |
| 158 pkts | exp3_mode_tcp-udp (3_TrafficMode) UDP Lost Packets | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_Lost' | 2026-11-16 | VERIFIED |
| 96.59% | exp3_mode_tcp-udp (3_TrafficMode) UDP Packet Delivery Ratio | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_PDR' | 2026-11-16 | VERIFIED |
| 3.41% | exp3_mode_tcp-udp (3_TrafficMode) UDP Packet Loss Percentage | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_LossPct' | 2026-11-16 | VERIFIED |
| 1.9403 Mbps | exp3_mode_tcp-udp (3_TrafficMode) UDP Throughput | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_Throughput_Mbps' | 2026-11-16 | VERIFIED |
| 429.205 ms | exp3_mode_tcp-udp (3_TrafficMode) UDP Average End-to-End Delay | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_Delay_ms' | 2026-11-16 | VERIFIED |
| 0.320 ms | exp3_mode_tcp-udp (3_TrafficMode) UDP Average Jitter | `results/processed/experiments_summary.csv` | Row 10, Col 'UDP_Jitter_ms' | 2026-11-16 | VERIFIED |
| 684 | Pre-simulated parameter permutations in web simulator | `https://tcp-udp-congestion-ns3.vercel.app/` | Landing hero text | 2026-11-16 | VERIFIED |
| 11 | Interactive educational learning missions | `https://tcp-udp-congestion-ns3.vercel.app/` | Mission progress panel | 2026-11-16 | VERIFIED |
| 1.992 Mbps | Web App Exp A: TCP Delivered Goodput under 20 Mbps link | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment A Card | 2026-11-16 | VERIFIED |
| 1.997 Mbps | Web App Exp A: UDP Delivered Goodput under 20 Mbps link | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment A Card | 2026-11-16 | VERIFIED |
| 12.60 ms | Web App Exp A: TCP One-Way Delay under 20 Mbps link | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment A Card | 2026-11-16 | VERIFIED |
| 12.59 ms | Web App Exp A: UDP One-Way Delay under 20 Mbps link | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment A Card | 2026-11-16 | VERIFIED |
| 4.850 Mbps | Web App Exp B: UDP Delivered Goodput at 8 Mbps offered load | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment B Table | 2026-11-16 | VERIFIED |
| 38.7% | Web App Exp B: UDP Packet Loss at 8 Mbps offered load | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment B Table | 2026-11-16 | VERIFIED |
| 98.3 ms | Web App Exp B: UDP One-Way Delay at 8 Mbps offered load | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment B Table | 2026-11-16 | VERIFIED |
| 3,401 | Web App Exp B: Queue drops at 8 Mbps offered load | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment B Table | 2026-11-16 | VERIFIED |
| 4.72 Mbps | Web App Exp C: TCP Bulk Delivered Goodput | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment C Card | 2026-11-16 | VERIFIED |
| 100 KiB | Web App Exp C: TCP Peak Congestion Window (Cwnd) | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment C Card | 2026-11-16 | VERIFIED |
| 35 | Web App Exp C: TCP Queue Drops at Router A | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment C Card | 2026-11-16 | VERIFIED |
| 1.85 Mbps | Web App Exp D: TCP Goodput under Competition with 3 Mbps UDP | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment D Card | 2026-11-16 | VERIFIED |
| 2.96 Mbps | Web App Exp D: UDP Goodput under Competition with TCP | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment D Card | 2026-11-16 | VERIFIED |
| 0.4% | Web App Exp D: UDP Packet Loss under Competition | `https://tcp-udp-congestion-ns3.vercel.app/#report` | Experiment D Card | 2026-11-16 | VERIFIED |