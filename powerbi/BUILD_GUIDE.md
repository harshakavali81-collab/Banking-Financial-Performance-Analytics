# Build and validate the native Power BI report

Status: CSVs, DAX measures, theme and Power Query function are prepared. A native `.pbix` has not been authored or tested in this environment. This is the remaining Power BI Desktop step.

## Import

1. Open Power BI Desktop, then Get data > Text/CSV. Import the nine CSVs in `data/clean/` plus `powerbi/dates.csv`. Use lowercase table names matching the filenames, including `dates`.
2. In Transform data, set IDs, tenure and DPD to Whole Number; all date fields to Date; money and rates to Decimal Number; labels to Text. Null payment dates are intentional.
3. Alternatively create a Text parameter `DataFolder`, set it to the absolute clean-data folder (without a final slash), paste `load_csv.pq` as a Blank Query named `LoadCsv`, and invoke `LoadCsv("accounts.csv")` etc. The supplied function imports CSVs; set the field types as above.
4. Close & Apply. Mark `dates` as the date table using its `date` column.

## Relationships

Create these as one-to-many with a single filter direction from the left table to the right. Remove any automatically created relationship not listed here. Do not relate customers.home_branch_id to branches, or transactions.customer_id/branch_id to dimensions: these redundant links would create multiple paths.

| One side | Many side |
|---|---|
| branches.branch_id | accounts.branch_id |
| branches.branch_id | loans.branch_id |
| branches.branch_id | branch_financials.branch_id |
| customers.customer_id | accounts.customer_id |
| customers.customer_id | loans.customer_id |
| accounts.account_id | transactions.account_id |
| accounts.account_id | account_snapshots.account_id |
| loans.loan_id | loan_snapshots.loan_id |
| loans.loan_id | repayments.loan_id |
| dates.date | transactions.transaction_date |
| dates.date | account_snapshots.snapshot_date |
| dates.date | loan_snapshots.snapshot_date |
| dates.date | branch_financials.snapshot_date |
| dates.date | repayments.due_date |

The date relationship for repayments intentionally measures collection against scheduled due-date cohorts. Do not add an active payment-date link. Year/month slicers are supported; the snapshot measures use the latest selected month-end. Do not present daily balance reporting from monthly snapshots.

## Measures and design

Create each measure in `measures.dax` separately through New measure (the whole file is not one expression). Use percentage formatting for rates and INR formatting for money. Import `theme.json` through View > Themes > Browse for themes.

| Page | Cards | Visuals and filters |
|---|---|---|
| Overview | Deposit Balance, Loan Outstanding, Net Interest Income, Operating Profit | Month-end balances by dates.year_month, transaction channels, branch deposits; branch/region/year_month slicers |
| Loan risk | DPD90 Exposure Ratio, DPD90 Loan Rate, Scheduled Collection Ratio | loan type, credit-score bands, DPD buckets; branch and month slicers |
| Branch finance | Operating Income, Operating Expenses, Cost to Income | Branch matrix, monthly operating profit, loan-to-deposit ratio; branch/month slicers |
| Customers | Account Customers, Average Account Balance | Occupation segments, income versus original loan amount; customer filters |

Create a calculated customers column `Score Band = IF(customers[credit_score]<650,"<650",IF(customers[credit_score]<750,"650-749","750+"))`. For DPD buckets, create a loan_snapshots column using 0, 1-29, 30-59, 60-89 and 90+ boundaries and filter its page to a single month-end.

Do not use a customer demographic slicer to imply allocated customer profitability: the finance ledger is at branch-month grain. Customer, loan-type and account-type filters affect the relevant facts, not branch financial totals. State this on the report or use separate pages.

## Reconcile before saving

With all branches and the whole year selected, check Deposit Balance = 523,202,617.11; Loan Outstanding = 899,819,122.17; Transactions = 40,000; Net Interest Income = 72,384,180.86; Operating Profit = 63,144,180.86. Ratios: loan-to-deposit 171.9829%, 90+ DPD exposure 35.9924%. A full-year snapshot card must show December balances, not 12-month sums. Select January alone and verify against `outputs/sql_results/monthly_performance.csv`; select a branch and verify against `branch_performance.csv`. Save as `Banking_Financial_Analytics.pbix` only after these checks.

Microsoft references: [star schema](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema), [relationships](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships), [CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax).
