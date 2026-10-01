# Work with this GitHub project

Repository: https://github.com/harshakavali81-collab/Banking-Financial-Performance-Analytics

## Clone and reproduce

```bash
git clone https://github.com/harshakavali81-collab/Banking-Financial-Performance-Analytics.git
cd Banking-Financial-Performance-Analytics
python -m venv .venv
```

Activate the environment using the operating-system steps in README.md, then run:

```bash
python -m pip install -r requirements.txt
python src/pipeline.py
python tests/validate.py
```

## Update your work

After reviewing and validating your changes:

```bash
git add .
git commit -m "Update banking analytics"
git push origin main
```

Use GitHub's credential manager or sign-in prompt. Never place a personal access token in a committed file.

## Recruiter review

Start with README.md and the dashboard preview. Download outputs/Banking_Analytics.xlsx and outputs/Banking_Analytics_Report.pdf. Open outputs/Banking_Dashboard.html locally in Chrome or Edge. The powerbi folder includes CSV import, DAX, theme and build instructions; native Power BI Desktop authoring remains to be done.
