# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`README.md`](<../README.md>)
- [`data`](<../data>)
- [`data/clean`](<../data/clean>)
- [`data/clean/account_snapshots.csv`](<../data/clean/account_snapshots.csv>)
- [`data/clean/accounts.csv`](<../data/clean/accounts.csv>)
- [`data/clean/branch_financials.csv`](<../data/clean/branch_financials.csv>)
- [`data/clean/branches.csv`](<../data/clean/branches.csv>)
- [`data/clean/customers.csv`](<../data/clean/customers.csv>)
- [`data/clean/loan_snapshots.csv`](<../data/clean/loan_snapshots.csv>)
- [`data/clean/loans.csv`](<../data/clean/loans.csv>)
- [`data/clean/repayments.csv`](<../data/clean/repayments.csv>)
- [`data/clean/transactions.csv`](<../data/clean/transactions.csv>)
- [`data/quarantine`](<../data/quarantine>)
- [`data/quarantine/transactions.csv`](<../data/quarantine/transactions.csv>)
- [`data/raw`](<../data/raw>)
- [`data/raw/account_snapshots.csv`](<../data/raw/account_snapshots.csv>)
- [`data/raw/accounts.csv`](<../data/raw/accounts.csv>)
- [`data/raw/branches.csv`](<../data/raw/branches.csv>)
- [`data/raw/customers.csv`](<../data/raw/customers.csv>)
- [`data/raw/loan_snapshots.csv`](<../data/raw/loan_snapshots.csv>)
- [`data/raw/loans.csv`](<../data/raw/loans.csv>)
- [`data/raw/repayments.csv`](<../data/raw/repayments.csv>)
- [`data/raw/transactions.csv`](<../data/raw/transactions.csv>)
- [`docs`](<../docs>)
- [`docs/DATA_DICTIONARY.md`](<../docs/DATA_DICTIONARY.md>)
- [`docs/GITHUB_SETUP.md`](<../docs/GITHUB_SETUP.md>)
- [`docs/INTERVIEW_AND_RESUME.md`](<../docs/INTERVIEW_AND_RESUME.md>)
- [`docs/KPI_DICTIONARY.md`](<../docs/KPI_DICTIONARY.md>)
- [`docs/business_report.md`](<../docs/business_report.md>)
- [`notebooks`](<../notebooks>)
- [`notebooks/Banking_EDA.ipynb`](<../notebooks/Banking_EDA.ipynb>)
- [`outputs`](<../outputs>)
- [`outputs/Banking_Analytics.xlsx`](<../outputs/Banking_Analytics.xlsx>)
- [`outputs/Banking_Analytics_Report.pdf`](<../outputs/Banking_Analytics_Report.pdf>)
- [`outputs/Banking_Dashboard.html`](<../outputs/Banking_Dashboard.html>)
- [`outputs/banking.db`](<../outputs/banking.db>)
- [`outputs/charts`](<../outputs/charts>)
- [`outputs/charts/customer_eda.png`](<../outputs/charts/customer_eda.png>)
- [`outputs/charts/dashboard.png`](<../outputs/charts/dashboard.png>)
- [`outputs/cleaning_audit.json`](<../outputs/cleaning_audit.json>)
- [`outputs/dashboard_data.json`](<../outputs/dashboard_data.json>)
- [`outputs/kpis.json`](<../outputs/kpis.json>)
- [`outputs/sql_results`](<../outputs/sql_results>)
- [`outputs/sql_results/branch_performance.csv`](<../outputs/sql_results/branch_performance.csv>)
- [`outputs/sql_results/channel_mix.csv`](<../outputs/sql_results/channel_mix.csv>)
- [`outputs/sql_results/delinquency_buckets.csv`](<../outputs/sql_results/delinquency_buckets.csv>)
- [`outputs/sql_results/loan_type_performance.csv`](<../outputs/sql_results/loan_type_performance.csv>)
- [`outputs/sql_results/monthly_performance.csv`](<../outputs/sql_results/monthly_performance.csv>)
- [`outputs/sql_results/monthly_transaction_growth.csv`](<../outputs/sql_results/monthly_transaction_growth.csv>)
- [`outputs/sql_results/occupation_segments.csv`](<../outputs/sql_results/occupation_segments.csv>)
- [`outputs/sql_results/repayment_collection.csv`](<../outputs/sql_results/repayment_collection.csv>)
- [`outputs/sql_results/risk_by_score.csv`](<../outputs/sql_results/risk_by_score.csv>)
- [`outputs/sql_results/top_deposit_customers.csv`](<../outputs/sql_results/top_deposit_customers.csv>)
- [`outputs/validation.json`](<../outputs/validation.json>)
- [`outputs/verification_notes.json`](<../outputs/verification_notes.json>)
- [`outputs/workbook_data.json`](<../outputs/workbook_data.json>)
- [`powerbi`](<../powerbi>)
- [`powerbi/BUILD_GUIDE.md`](<../powerbi/BUILD_GUIDE.md>)
- [`powerbi/dates.csv`](<../powerbi/dates.csv>)
- [`powerbi/load_csv.pq`](<../powerbi/load_csv.pq>)
- [`powerbi/measures.dax`](<../powerbi/measures.dax>)
- [`powerbi/theme.json`](<../powerbi/theme.json>)
- [`requirements.txt`](<../requirements.txt>)
- [`sql`](<../sql>)
- [`sql/analysis.sql`](<../sql/analysis.sql>)
- [`sql/schema.sql`](<../sql/schema.sql>)
- [`src`](<../src>)
- [`src/dashboard_template.html`](<../src/dashboard_template.html>)
- [`src/pipeline.py`](<../src/pipeline.py>)
- [`tests`](<../tests>)
- [`tests/validate.py`](<../tests/validate.py>)
- [`tools`](<../tools>)
- [`tools/build_workbook.mjs`](<../tools/build_workbook.mjs>)
