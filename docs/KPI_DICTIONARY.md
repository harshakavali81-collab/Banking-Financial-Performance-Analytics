# KPI definitions

All money is INR. Portfolio balances use 31 December 2025. Income and transactions cover January-December 2025. Rates are stored as decimals.

| KPI | Numerator / calculation | Denominator / scope |
|---|---|---|
| Deposit balance | Sum of account month-end balances | One selected month-end only |
| Loan outstanding | Sum of unpaid principal | One selected month-end only |
| Loan-to-deposit ratio | Loan outstanding | Deposit balance, same month-end |
| 90+ DPD exposure ratio | Outstanding on loans with oldest unpaid due date at least 90 days old | Total loan outstanding, same month-end |
| 90+ DPD loan rate | Count of loans with DPD >=90 | Count of loans, same month-end |
| Deposit growth | Closing deposits minus opening deposits | Opening deposits on 1 January 2025 |
| Transaction value | Sum of absolute transaction amounts | Includes in/out movements; not bank revenue |
| Digital transaction share | Mobile + Internet transaction count | All transaction count |
| Net interest income | Cash interest received minus simulated interest expense | Reporting period |
| Operating income | Net interest income plus fees | Reporting period |
| Operating profit | Operating income minus operating expenses | Before provisions and tax |
| Cost-to-income ratio | Operating expenses | Net interest income plus fees |
| Scheduled collection ratio | Principal paid plus interest paid | Principal due plus interest due in selected due-date month |
| Weighted loan interest rate | Sum(outstanding x annual interest rate) | Total outstanding at month-end |

Fees equal INR 18 per transaction. Deposit expense uses a 3.5% annual rate applied to average monthly opening/closing balances. Branch wholesale funding uses an 8% annual rate on positive loan-minus-deposit funding gaps. Operating expenses are INR 70,000 + INR 75 per account + INR 9 per transaction per branch-month. These are synthetic assumptions, not external estimates.
