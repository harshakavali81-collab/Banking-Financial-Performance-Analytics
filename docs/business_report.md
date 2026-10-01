# Banking & Financial Performance Analytics

Synthetic portfolio. Reporting year: 2025. Snapshot: 31 December 2025. Currency: INR.

## Findings

- Chennai Central has the largest deposit balance: INR 7.02 crore, 13.4% of the portfolio.
- Deposits changed -0.5% from the 1 January opening balance to 31 December.
- Mobile and Internet account for 71.7% of annual transactions.
- The <650 score band has the highest 90+ DPD loan rate (52.6%, 266 loans). This pattern is partly programmed into the simulation.
- 90+ DPD balances represent 36.0% of outstanding loans. This is an analytical proxy, not a regulatory NPA classification.
- Annual management operating profit before credit losses and tax is INR 6.31 crore.

## Recommendations

- Prioritize a collections review of 90+ DPD loans, recording recoveries and arrears before interpreting risk trends.
- Review funding needs alongside the loan-to-deposit ratio. Wholesale funding expense is explicitly modeled for branches with a funding gap.
- Compare branch operating costs and income before reallocating resources. Test any proposed change against real operational constraints.
- Replace simulated patterns with appropriately anonymized real data before making a banking decision.

## Data quality

{
  "raw_transactions": 40115,
  "exact_duplicates_removed": 100,
  "transactions_quarantined": 15,
  "clean_transactions": 40000,
  "channel_aliases_normalized": 40,
  "missing_occupations_labelled_unknown": 20
}

## Limits

All customers, transactions and results are generated with seed 81. The loan schedule uses equal principal installments, not fixed-EMI amortization. Missed installments remain unpaid through year-end; later scheduled payments do not clear older arrears. Interest income is cash received. Deposit cost uses average opening/closing monthly balances and a 3.5% annual rate. Wholesale funding uses an 8% annual rate for positive branch loan-minus-deposit gaps. Fees are separately simulated at INR 18 per transaction. Operating profit excludes credit-loss provisions and tax. Fee and deposit-interest postings are outside the customer transaction ledger. No financial prediction or regulatory compliance is claimed.
