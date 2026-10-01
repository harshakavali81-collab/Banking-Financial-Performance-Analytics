# Interview and resume notes

Use these after running the project and understanding its assumptions. Do not claim the Power BI report is finished until you build and test it in Desktop.

## Resume bullets

- Developed a synthetic banking analytics pipeline using Python, Pandas and SQLite to clean 40,000 transactions and analyze 2,500 customers, 3,200 accounts and 1,200 loans.
- Built an interactive dashboard and formula-based Excel analysis of deposits, loan exposure, branch profitability and transaction channels, with nine reconciliations validating data and financial totals.

After completing the Power BI build, you can add: Built a Power BI model with monthly snapshot measures, branch filters and loan risk visuals using DAX and Power Query.

## 60-second explanation

I built a banking performance analytics portfolio project using synthetic data. The goal was to compare deposit balances, outstanding loans, branch performance and credit risk. I cleaned duplicate transactions, normalized channel names and quarantined invalid records. I loaded the clean tables into SQLite and used joins, CTEs, grouping and window functions for ten analyses. Python generated EDA charts, KPIs and an offline dashboard. I also prepared an Excel workbook and Power BI build assets. A key design decision was separating month-end balances from annual transaction flows to avoid double counting. Nine checks reconcile the data and totals. All findings describe simulated data, and the loan model has documented limitations.

## Questions you should be able to answer

1. Why is transaction value not bank revenue? It includes customers moving their own funds. Income comes from the separate interest and fee ledger.
2. Why not sum month-end balances? The same principal appears in multiple snapshots. Portfolio size requires a single selected snapshot.
3. How did you prevent join fan-out? Aggregate deposits, loans and financial flows separately by branch before joining the summaries.
4. What is DPD? Calendar days since the oldest unpaid installment. In this simulation, missed installments are never cured.
5. Is the 90+ DPD metric NPA? It is a clearly labeled project proxy. Real classification needs the applicable product rules, recovery history and regulatory policy.
6. How did you validate the project? Account ledger roll-forward, loan principal roll-forward, branch-to-total reconciliation, foreign keys, row accounting, balance and DPD bounds.
7. What would you improve? Realistic amortization and arrears recovery, accrual accounting, actual funding allocations, data privacy controls and an automated monthly refresh.
8. Does credit score cause default here? No causal claim is justified. The missing-payment probability is partly derived from credit score in the generator.
