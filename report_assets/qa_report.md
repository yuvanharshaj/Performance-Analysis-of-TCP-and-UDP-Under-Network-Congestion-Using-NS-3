# Quality Assurance Report: Performance Analysis of TCP and UDP Under Network Congestion Using NS-3

**Date of QA Evaluation:** 2026-11-16
**Artifacts Evaluated:**
- DOCX Report: `c:\Users\yuvan\OneDrive\Documents\CN PROJECT\tcp-udp-congestion-analysis-ns3\Performance_Analysis_of_TCP_and_UDP_Final_Report.docx`
- PDF Report: `c:\Users\yuvan\OneDrive\Documents\CN PROJECT\tcp-udp-congestion-analysis-ns3\Performance_Analysis_of_TCP_and_UDP_Final_Report.pdf`
- Master Repository: `yuvanharshaj/Performance-Analysis-of-TCP-and-UDP-Under-Network-Congestion-Using-NS-3`

## 1. Automated Verification Checks

| Check Item | Specification Rule | Observed Value | Verification Status |
| :--- | :--- | :--- | :---: |
| **PDF Total Page Count** | Strictly in [35, 42] pages | **36 Pages** | **PASS** |
| **Student Names Field** | MUST REMAIN 100% BLANK | '' (Empty string) | **PASS** |
| **Student USN Field** | MUST REMAIN 100% BLANK | '' (Empty string) | **PASS** |
| **Course Code & Section** | 24CS53, Section C | Code: '24CS53', Sec: 'C' | **PASS** |
| **Academic Year & Scheme** | 2026–27 | '2026 – 27' | **PASS** |
| **Faculty Guide Details** | Dr. Rajani K C, Assoc. Prof, EPCET | 'Dr. Rajani K C', 'Associate Professor', 'Computer Science & Engineering, EPCET' | **PASS** |
| **Project Evaluation Rubric** | Preserved exactly (40 Marks total) | Total Marks: 40 | **PASS** |
| **Page Margins (Body)** | Left 1.5", Right 1.0", Top 1.0", Bottom 1.0" | Left 1.5", Right 1.0", Top 1.0", Bottom 1.0" | **PASS** |
| **Body Font & Spacing** | Times New Roman, 12pt, 1.5 lines, Justified | Verified in styles & paragraph formats | **PASS** |
| **Heading Hierarchy** | H1 16pt bold, H2 14pt bold, H3 12pt bold | Verified in XML attributes | **PASS** |
| **Table of Contents Sync** | Page 2 INDEX table matches PDF pages | 10/10 Chapters Synchronized | **PASS** |

## 2. Table of Contents (INDEX) Synchronization Matrix

| Chapter No. | Chapter Title | INDEX Table Page | Verified PDF Page | Alignment Status |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Introduction | Page 4 | Page 4 | **MATCH** |
| 2 | Literature Survey | Page 7 | Page 7 | **MATCH** |
| 3 | Problem statement and Objectives | Page 9 | Page 9 | **MATCH** |
| 4 | Existing System and Proposed System | Page 11 | Page 11 | **MATCH** |
| 5 | System Architecture and Design | Page 13 | Page 13 | **MATCH** |
| 6 | Technologies, Tools and Protocols Used | Page 19 | Page 19 | **MATCH** |
| 7 | Implementation and Working Procedure | Page 21 | Page 21 | **MATCH** |
| 8 | Results, Output and Performance Analysis | Page 25 | Page 25 | **MATCH** |
| 9 | Applications, Advantages and Challenges | Page 32 | Page 32 | **MATCH** |
| 10 | Conclusion and Future Scope | Page 33 | Page 33 | **MATCH** |

## 3. Structural Inventory

- **Total Chapters:** 10 Chapters + References + Appendices (A through D)
- **Total Data Tables:** 15 tables (including front matter tables and empirical result tables)
- **Total Numbered Figures:** 16 figures (system architecture, topology, bufferbloat timeline, AIMD state machine, web architecture, 5 analytical simulation plots, and 2 web app live screenshots)
- **Total Code Excerpts:** 16 listings (C++ parameter handling, topology setup, TCP application, UDP application, Cwnd trace hook, Python parsing, shell execution)

## 4. Non-Negotiable Rules Audit

1. **Zero Fabrication:** Every numeric value corresponds exactly to `results/processed/experiments_summary.csv`, raw FlowMonitor XMLs, Cwnd CSVs, or the live application `https://tcp-udp-congestion-ns3.vercel.app/`.
2. **Evidence Ledger Complete:** All 60+ quantitative metrics are cataloged with source file paths and row/column references in `report_assets/evidence_ledger.md`.
3. **Discrepancy Audit Logged:** Parameter variations between repository simulation duration (19s) and web app lightweight JSON duration (9s) are formally documented in `report_assets/discrepancies.md`.
4. **Preservation of Institutional Integrity:** EPCET branding, Department of CSE, Faculty Guide Dr. Rajani K C, Course 24CS53, and the 40-mark evaluation rubric remain completely intact and unaltered.
5. **Student Fields Strictly Blank:** Neither dummy values nor student names/USNs have been inserted; all designated blank fields are preserved for student completion.

## 5. Visual Quality Assessment

- **Front Matter (Pages 1–3):** Clean cover page, unblemished institutional logos, formatted INDEX table with centered page numbers, and intact evaluation rubric.
- **Body Typography:** Times New Roman body text with 1.5 line spacing, justified alignment, clean hyphenation-free margins.
- **Visual Rhythm:** Balanced distribution of text, equation blocks, structured comparison tables, and centered 300 DPI vector-styled diagrams.
- **Table Formatting:** Alternating row shading (`#FDFEFE` and `#F4F6F6`), bold navy headers (`#102040`), centered numerical alignments, repeat headers enabled, and no awkward mid-row page splits (`w:cantSplit`).
- **Page Numbering:** Running headers right-aligned in italics; running footers right-aligned displaying `Computer Networks (24CS53) | Page X` dynamically rendered via Word OMML fields.

**Overall QA Verdict: APPROVED FOR ACADEMIC SUBMISSION AND REPOSITORY DEPLOYMENT.**