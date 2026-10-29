# Banking & Financial Performance Analytics

An end-to-end portfolio project by **Kavali Harshavardhan** using Python, SQLite, Excel, and Power BI build assets. All data is **synthetic**, generated reproducibly with seed 81. Reporting year: 2025. Currency: INR.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Portfolio dashboard](<outputs/charts/dashboard.png>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Download and open [Banking_Dashboard.html](outputs/Banking_Dashboard.html) in a browser for the offline dashboard. [Excel workbook](outputs/Banking_Analytics.xlsx) and [PDF report](outputs/Banking_Analytics_Report.pdf) are also included.

## Key Features

- Primary/foreign keys and grain are explicit. SQL preaggregates facts before joining to avoid multiplying balances by transaction counts.
- Stocks use the latest month-end; income and transactions sum over the reporting period. Monthly balances are never summed into an annual portfolio balance.
- Bank income is modeled separately from customer transaction amounts.
- Outstanding principal reconciles to original principal less principal paid. Deposits reconcile to opening balances plus signed transactions.
- All nine pipeline checks pass. `outputs/validation.json` and the standalone validator preserve the evidence.
- KPI definitions and assumptions are documented in `docs/KPI_DICTIONARY.md` and `docs/DATA_DICTIONARY.md`.

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

Source layout and component inventory (asset not present in this checkout). A runtime architecture diagram remains a follow-up task.

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/Banking-Financial-Performance-Analytics.git
cd Banking-Financial-Performance-Analytics
```

Install Python 3.11+ and open this folder in VS Code. Open Terminal > New Terminal.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/pipeline.py
python tests/validate.py
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/pipeline.py
python tests/validate.py
```

The Python pipeline regenerates data, SQLite, query results, charts, PDF, and HTML. The bundled Excel is a finished deliverable; refreshing the Python pipeline does not overwrite the Excel workbook. Reimport the CSV summaries into Excel when changing the simulation. The optional workbook builder requires the ChatGPT artifact runtime, rather than an ordinary Python installation.

## Challenges & Solutions

**Repository organization:** this project uses `src/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

An end-to-end portfolio project by **Kavali Harshavardhan** using Python, SQLite, Excel, and Power BI build assets. All data is **synthetic**, generated reproducibly with seed 81. Reporting year: 2025. Currency: INR.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `sql/` | SQL schema and analysis |
| `powerbi/` | Power BI build assets |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Banking-Financial-Performance-Analytics/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

