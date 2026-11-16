# Comprehensive Project Report Audit & Changelog

**Project Title:** Performance Analysis of TCP and UDP Under Network Congestion Using NS-3  
**Course:** Computer Networks (24CS53), Semester V, Section C, AY 2026–2027  
**Institution:** East Point College of Engineering and Technology (EPCET), Bengaluru (VTU)  
**Faculty Guide:** Dr. Rajani K C, Associate Professor, Dept. of CSE  
**Head of Department:** Dr. I. Manimozhi, Professor & HOD, Dept. of CSE  

---

## 1. Executive Summary of Overhaul & Regeneration

This report was completely audited, tightened, and regenerated from the ground-truth simulation codebase and FlowMonitor traces (`scratch/congestion-analysis.cc`, `results/processed/experiments_summary.csv`, `tests/test_analysis.py`). The resulting document conforms strictly to VTU academic specifications, single-column A4 typography, professional mathematical derivations, and unclipped 300 DPI figures.

### Deliverables Generated:
1. `output/TCP_UDP_NS3_Mini_Project_Report.docx` — Fully editable single-column A4 report with native Word tables, headings, and dynamic fields.
2. `output/TCP_UDP_NS3_Mini_Project_Report.pdf` — Submission-ready, 40-page print-quality PDF.
3. `output/CHANGELOG.md` — Detailed audit of all numerical corrections, architectural improvements, and input checklist.

Synchronized duplicate copies are also placed in `C:\output` and `tcp-udp-congestion-analysis-ns3\`.

---

## 2. Complete Numerical Correction & Consistency Ledger

All numbers in the report were cross-checked and verified against `results/processed/experiments_summary.csv`. Every discrepancy from the prior report PDF has been corrected as documented below:

| # | Topic / Metric | Prior Report Value | Verified Correct Value | Source Reference | Reason for Correction |
|---|----------------|-------------------|------------------------|------------------|-----------------------|
| 1 | Bufferbloat Latency (Queue 10p) | "47 ms" / "47.9 ms" | **TCP: 77.855 ms, UDP: 101.378 ms** | `experiments_summary.csv` (Row 1) | Prior report quoted unverified numbers. Data shows TCP starts at 77.86 ms and UDP at 101.38 ms. |
| 2 | Bufferbloat Latency (Queue 100p) | "448.9 ms" / "815 ms" | **TCP: 480.958 ms, UDP: 815.338 ms** | `experiments_summary.csv` (Row 4) | Clearly differentiated TCP latency from UDP latency; prior text conflated protocol delays. |
| 3 | Bufferbloat Inflation % | "800% increase" | **704.2% increase (~8.0x)** | Derived: $(815.338 - 101.378)/101.378$ | An 8.04x growth represents a 704.2% increase, mathematically not 800%. |
| 4 | TCP Cwnd Reduction Dynamic | "cuts/throttles Cwnd exponentially" | **"multiplicatively (halves Cwnd by 50%)"** | RFC 5681, RFC 6582 | Exponential changes apply only to Slow Start growth ($2^k$). Congestion loss triggers multiplicative decrease ($W/2$). |
| 5 | Hypothesis H1 Delay Growth | "delay grows exponentially" | **"delay grows substantially (approximately linearly with buffer size, ~8x / 704.2% increase)"** | Section 3.4, `experiments_summary.csv` | DropTail queuing delay is physically $D_q = (B \times L \times 8)/C$, which scales linearly with queue depth $B$. |
| 6 | Link Utilization at 2 Mbps | "100.0%" (capped) | **102.60% (with clarifying footnote)** | `experiments_summary.csv` (Row 6) | Aggregate throughput is $0.1117 + 1.9403 = 2.0520\text{ Mbps}$ on a 2.0 Mbps link. Footnote added explaining per-flow windowing offsets $(t_{lastRx} - t_{firstTx})$. |
| 7 | Simulator Naming Convention | "NS-3 v3.42" | **"ns-3.42"** | Global Codebase Standard | Standardized to official lowercase hyphenated nomenclature `ns-3.42`. |
| 8 | Institutional Outcome Mapping | "ABET program outcomes" & "CLO1-CLO4" | **"program outcomes PO1-PO5 (NBA/VTU)"** | Section 10.3 | EPCET is affiliated with VTU and accredited by NBA, not ABET. |
| 9 | Path Portability in Table 9.1 | `"/home/yuvan/project"` | **"a symlinked workspace directory"** | Table 9.1 | Removed developer-specific local directory path. |
| 10 | Automated Unit Tests Count | Stated 11, listed 8 | **Exactly 4 unit tests** | `tests/test_analysis.py`, verified via pytest | Matched real pytest suite: `test_parse_ns_time`, `test_missing_xml_file`, `test_zero_packet_flow_guard`, `test_real_flowmon_parsing` (all 4 passed). |
| 11 | Starvation Quantification | General descriptions | **TCP: 1.9851 -> 0.1117 Mbps (94.37% drop); UDP: 1.9946 -> 1.9403 Mbps (2.7% drop)** | `experiments_summary.csv` (Rows 9-11) | Re-verified precise percentage drops directly from FlowMonitor throughput logs. |
| 12 | Figure 8.5 Trace Colors | Text said blue/orange, plot used green/red | **Blue (`#1f77b4`) = Uncontested TCP; Orange (`#ff7f0e`) = Contested TCP** | `graphs/cwnd_vs_time.png` | Re-rendered plot with explicit color palette matching the analytical narrative. |

---

## 3. Structural, Layout & Typography Enhancements

1. **Page Budget & Geometry:**
   - Single-column A4 layout throughout ($8.27" \times 11.69"$).
   - Margins: strictly Left 1.25", Top 1.0", Bottom 1.0", Right 1.0".
   - Total document length calibrated to exactly **40 pages**, strictly within the requested [35, 40] page university mini-project specification.
2. **Page Numbering Architecture:**
   - Front matter (Cover, INDEX, Rubrics, Certificate, Declaration, Acknowledgement, Abstract, List of Figures, List of Tables) contained in preliminary sections.
   - Body Section starts on a new page at **Chapter 1: Introduction**, resetting the dynamic page numbering field to **Page 1**.
   - Footer formatted with `"Computer Networks (24CS53)"` on the left and dynamic `"Page X"` on the right.
   - Header formatted with `"Performance Analysis of TCP and UDP Under Network Congestion Using ns-3.42"` right-aligned in 8.5 pt italic.
3. **Table Formatting & Anti-Clipping:**
   - All captions placed **ABOVE** the table in 10 pt bold Times New Roman.
   - Enabled XML table header repeat on page breaks (`w:tblHeader`) and row-split prevention (`w:cantSplit`).
   - Table 2.1: Allocated dedicated 0.65" width to the "Year" column, eliminating the broken `"198"` / `"1"` word wraps.
   - Table 8.3: Optimized all 9 column widths, eliminating vertical single-character cell text and awkward wrapping on `"TCP+UDP Contention"`.
   - Table 8.4: Split into **Table 8.4a (Consolidated TCP Performance Metrics)** and **Table 8.4b (Consolidated UDP Performance Metrics)** across all 11 runs, allowing row labels like `exp1_queue_10p` to remain unbroken on a single line.
4. **Figure Re-rendering & Integration:**
   - All 11 figures regenerated at 300 DPI using Matplotlib with exact bounding box padding (`bbox_inches="tight"`).
   - Removed baked-in duplicate title headers from images; added standardized caption blocks **BELOW** each figure.
   - Figures 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 8.1–8.5, and D.1–D.4 scaled proportionally to fit printable margins without right-edge clipping.
5. **Organizational Re-structuring:**
   - Moved the 10-question technical Viva Voce preparation guide out of Chapter 10 into a dedicated **Appendix B: Viva Voce Preparation**.
   - Inserted formal academic **Certificate**, **Declaration**, **Acknowledgement**, **Abstract** (174 words), **List of Figures**, and **List of Tables** into the Front Matter.
   - Maintained Chapter 10 strictly focused on technical summary, NBA/VTU outcomes, and future scope.

---

## 4. Needs My Input (Checklist for Student)

Please review the following items before submitting your hardcopy / final digital dossier:

- [ ] **Student Names & USN:** The fields `[STUDENT NAME(S)]` and `[USN(S)]` have been left as clean placeholders on the Cover Page (Table 1), Certificate Page, and Declaration Page. Fill in your name(s) and USN(s).
- [ ] **Section:** Preset to `"C"`. Verify if this matches your enrolled class section.
- [ ] **Course Learning Outcomes (CLOs):** Section 10.3 references program outcomes PO1–PO5 under NBA/VTU criteria. If your faculty guide requires explicit CLO-to-module mappings (e.g., CLO1 to CLO4), confirm the exact wording against the official EPCET 24CS53 syllabus.
- [ ] **Signatures:** Obtain physical or digital signatures from:
  1. Faculty Guide: **Dr. Rajani K C** (Associate Professor, Dept. of CSE)
  2. Head of Department: **Dr. I. Manimozhi** (Professor & HOD, Dept. of CSE)
  3. Principal, East Point College of Engineering and Technology
