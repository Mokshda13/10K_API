Intelligent SEC 10-K Data Extraction Pipeline
Overview
This project presents a scalable and automated data extraction pipeline that transforms unstructured and structured SEC 10-K filings into standardized, query-ready financial datasets. It was developed as part of a research initiative in collaboration with CIBC and Purdue University to address the high costs, inefficiencies, and inconsistencies associated with traditional financial data sourcing methods.

Key Features
Multi-Format Ingestion: Supports both unstructured (TXT/PDF/HTML) and structured (XBRL/XML) 10-K filings via the SEC EDGAR system.

Two-Stage LLM Architecture: Implements a dual-prompt strategy to first extract financial tables and then refine and standardize them.

Metric Standardization: Maps diverse financial metric names to a unified schema for consistent cross-company and multi-year analysis.

Industry Mapping: Uses CIK-to-SIC code mapping for sector-level comparisons and industry filtering.

Human-in-the-Loop QA: Flags low-confidence outputs for manual verification to ensure high data integrity.

SQL-Compatible Output: Cleaned and validated data is stored in a relational format for querying and downstream analytics.

Cost-Efficient: End-to-end processing cost is reduced by over 90% compared to manual or Bloomberg-assisted approaches.

Directory Structure
graphql
Copy
Edit
mokshda13-10k_api/
│
├── requirements.txt                # Python dependencies
├── data/
│   ├── mapping/
│   │   ├── company_tickers.csv    # CIK-ticker mapping
│   │   └── sic_codes.csv          # CIK-SIC mapping
│
├── notebook/
│   └── EDGAR.ipynb                # Exploration and experimentation notebook
│
└── src/
    ├── datadownloader.py          # Downloads and extracts 10-K filings
    ├── getciks.py                 # Fetches CIK codes and SIC codes
    ├── main.py                    # Main script for pipeline execution
Use Case
Smaller financial institutions often lack access to comprehensive financial databases. This tool bridges that gap by enabling low-cost, high-accuracy extraction of financial data directly from public filings, enabling improved regulatory monitoring, forecasting, and modeling.

Technologies Used
Python (pandas, numpy, requests)

Azure Virtual Machine (for batch extraction tasks)

Large Language Models (OpenAI GPT-4o, o3-mini, DeepSeek R1)

SQL Server / Databricks for data storage

Markdown + prompt engineering for LLM input optimization

Acknowledgments
Developed by Mayank Bambal and Mokshda Sharma under the guidance of Prof. Gary Mercado Velasco, with collaboration from CIBC USA.

