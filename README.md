
# The Economics of Commercial Fusion

### A Data-Driven Market and Strategic Analysis of Proxima Fusion

**Independent Research Project | Engineering Economics · Energy Strategy · Data Analytics**

## Overview

Commercial nuclear fusion has the potential to become a new source of low-carbon electricity. However, its economic competitiveness remains uncertain due to technological, manufacturing, financial, and commercialization challenges.

This independent research project investigates the emerging commercial fusion industry, using Proxima Fusion as its primary case study.

The research combines competitive intelligence, quantitative market analysis, engineering economics, and strategic decision modeling.

### Central Research Question

> Under which technological, economic, and market conditions can stellarator-based fusion become commercially competitive in Europe, and what strategic positioning should Proxima Fusion pursue?

## Research Objectives

1. Analyze the financing and competitive structure of the commercial fusion industry.
2. Benchmark Proxima Fusion against selected fusion technology companies.
3. Evaluate technological and manufacturing factors influencing commercial reactor economics.
4. Develop Python-based techno-economic models for commercial fusion power plants.
5. Quantify economic uncertainties and evaluate alternative commercialization strategies.

## Companies Under Investigation

- Proxima Fusion — Primary case study
- Type One Energy
- Thea Energy
- Commonwealth Fusion Systems
- Tokamak Energy

## Research Methodology

The project is organized into seven stages:

| Stage | Description | Status |
|---|---|---|
| 1 | Research Design & Hypotheses | Completed |
| 2 | Market Data & Financial Analysis | Initial analysis completed; validation ongoing |
| 3 | Competitive Technology Benchmarking | Planned |
| 4 | Techno-Economic Modeling | Planned |
| 5 | Risk & Monte Carlo Simulation | Planned |
| 6 | Strategic Decision Modeling | Planned |
| 7 | Final Research Report & Dashboard | Planned |

## Current Work

### Financial Data Analysis

A structured dataset has been developed covering:

- Company characteristics
- Selected disclosed investment rounds
- Reported cumulative funding snapshots
- Strategic partnership announcements
- Source and evidence documentation

Python scripts have been implemented for data validation, funding aggregation, historical currency conversion, and comparative visualization.

### Strategic Partnership Analysis

Publicly documented strategic relationships have been classified by primary capability:

- Industrial and manufacturing
- Scientific research and development
- Computing and simulation
- Public-sector support
- Commercial and market access

The analysis is exploratory and does not represent a complete census of industry partnerships.

## Preliminary Research Outputs

### Selected Funding Rounds

![Selected Disclosed Funding](reports/funding_comparison_usd.png)

*Selected publicly disclosed investment rounds, standardized into USD using historical reference rates. These totals do not represent complete company funding histories.*

### Strategic Partnership Capabilities

![Partnership Capabilities](reports/partnership_capabilities.png)

*Selected publicly announced partnerships, classified by primary strategic function. Counts do not measure partnership quality.*

## Technical Stack

**Programming and Data Processing**
- Python
- Pandas
- NumPy

**Visualization**
- Matplotlib

**Research and Documentation**
- Git and GitHub
- Markdown
- CSV-based structured data
- Scientific and corporate source analysis

**Planned Methods**
- LCOE and discounted cash flow modeling
- Sensitivity and scenario analysis
- Monte Carlo simulation
- Multi-criteria decision analysis

## Repository Structure

```text
fusion-energy-strategy-analysis/
├── data/               # Research datasets
├── src/                # Python analysis scripts
├── research/           # Research proposal and chapters
├── reports/            # Analytical figures and reports
├── notebooks/          # Exploratory analysis notebooks
├── README.md
├── requirements.txt
└── .gitignore
```

## Reproducing the Analysis

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd fusion-energy-strategy-analysis
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the existing analyses

```bash
python src/check_dataset.py
python src/audit_funding.py
python src/benchmark_funding.py
python src/funding_comparison.py
python src/partnership_capabilities.py
python src/research_summary.py
```

Some analyses require the processed datasets included in the repository. The currency normalization script additionally retrieves historical exchange rates from the European Central Bank.

## Research Documentation

The initial market financing analysis is available in:

`research/03_market_financing_analysis.md`

The underlying datasets and their associated sources are documented in the `data/` directory.

## Limitations

This research uses publicly available disclosures and selected company announcements.

Funding figures may differ in composition, reporting dates, and completeness.

Technological milestones announced by companies are not treated as independently verified outcomes unless supporting evidence is available.

All scenario-based economic projections will explicitly distinguish assumptions from observed data.

## Disclaimer

This is an independent educational research project.

It is not commissioned, sponsored, or endorsed by Proxima Fusion or any of the other companies discussed.

The research does not constitute investment advice.
```
