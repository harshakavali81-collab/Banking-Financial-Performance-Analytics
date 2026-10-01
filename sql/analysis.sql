-- SQLite queries. Monetary columns are INR; ratios are decimals.
-- QUERY: branch_performance
WITH deposits AS (
 SELECT a.branch_id,SUM(s.balance) deposit_balance,COUNT(DISTINCT a.customer_id) account_customers
 FROM account_snapshots s JOIN accounts a USING(account_id)
 WHERE s.snapshot_date='2025-12-31' GROUP BY a.branch_id
), loan_balances AS (
 SELECT l.branch_id,SUM(s.outstanding) loan_outstanding,
 SUM(CASE WHEN s.days_past_due>=90 THEN s.outstanding ELSE 0 END) dpd90_outstanding
 FROM loan_snapshots s JOIN loans l USING(loan_id)
 WHERE s.snapshot_date='2025-12-31' GROUP BY l.branch_id
), finance AS (
 SELECT branch_id,SUM(interest_income-interest_expense) net_interest_income,
 SUM(fee_income) fee_income,SUM(operating_expense) operating_expense,
 SUM(interest_income-interest_expense+fee_income-operating_expense) operating_profit
 FROM branch_financials GROUP BY branch_id
)
SELECT b.*,d.deposit_balance,d.account_customers,l.loan_outstanding,l.dpd90_outstanding,
 l.loan_outstanding/NULLIF(d.deposit_balance,0) loan_to_deposit_ratio,
 l.dpd90_outstanding/NULLIF(l.loan_outstanding,0) dpd90_exposure_ratio,
 f.net_interest_income,f.fee_income,f.operating_expense,f.operating_profit
FROM branches b JOIN deposits d USING(branch_id) JOIN loan_balances l USING(branch_id) JOIN finance f USING(branch_id);

-- QUERY: monthly_performance
WITH d AS (SELECT snapshot_date,SUM(balance) deposit_balance FROM account_snapshots GROUP BY snapshot_date),
l AS (SELECT snapshot_date,SUM(outstanding) loan_outstanding,SUM(CASE WHEN days_past_due>=90 THEN outstanding ELSE 0 END) dpd90_outstanding FROM loan_snapshots GROUP BY snapshot_date),
f AS (SELECT snapshot_date,SUM(interest_income) interest_income,SUM(interest_expense) interest_expense,SUM(fee_income) fee_income,SUM(operating_expense) operating_expense FROM branch_financials GROUP BY snapshot_date)
SELECT SUBSTR(d.snapshot_date,1,7) month,d.snapshot_date,d.deposit_balance,l.loan_outstanding,l.dpd90_outstanding,
f.interest_income,f.interest_expense,f.fee_income,f.operating_expense,
f.interest_income-f.interest_expense net_interest_income,
f.interest_income-f.interest_expense+f.fee_income-f.operating_expense operating_profit
FROM d JOIN l USING(snapshot_date) JOIN f USING(snapshot_date) ORDER BY snapshot_date;

-- QUERY: risk_by_score
WITH risk AS (SELECT s.*,CASE WHEN c.credit_score<650 THEN '<650' WHEN c.credit_score<750 THEN '650-749' ELSE '750+' END score_band
FROM loan_snapshots s JOIN loans l USING(loan_id) JOIN customers c USING(customer_id) WHERE s.snapshot_date='2025-12-31')
SELECT score_band,COUNT(*) loan_count,SUM(outstanding) outstanding,
SUM(CASE WHEN days_past_due>=90 THEN 1 ELSE 0 END) dpd90_count,
AVG(CASE WHEN days_past_due>=90 THEN 1.0 ELSE 0.0 END) dpd90_loan_rate,
SUM(CASE WHEN days_past_due>=90 THEN outstanding ELSE 0 END)/NULLIF(SUM(outstanding),0) dpd90_exposure_ratio
FROM risk GROUP BY score_band ORDER BY CASE score_band WHEN '<650' THEN 1 WHEN '650-749' THEN 2 ELSE 3 END;

-- QUERY: channel_mix
SELECT channel,COUNT(*) transaction_count,SUM(amount) transaction_value,
COUNT(*)*1.0/(SELECT COUNT(*) FROM transactions) transaction_share
FROM transactions GROUP BY channel ORDER BY transaction_count DESC;

-- QUERY: loan_type_performance
SELECT l.loan_type,COUNT(*) loan_count,SUM(l.original_principal) original_principal,SUM(s.outstanding) outstanding,
SUM(CASE WHEN s.days_past_due>=90 THEN s.outstanding ELSE 0 END)/SUM(s.outstanding) dpd90_exposure_ratio,
SUM(s.outstanding*l.annual_interest_rate)/SUM(s.outstanding) weighted_interest_rate
FROM loans l JOIN loan_snapshots s USING(loan_id) WHERE s.snapshot_date='2025-12-31' GROUP BY l.loan_type;

-- QUERY: top_deposit_customers
SELECT c.customer_id,c.customer_name,SUM(s.balance) deposit_balance,
DENSE_RANK() OVER(ORDER BY SUM(s.balance) DESC) balance_rank
FROM customers c JOIN accounts a USING(customer_id) JOIN account_snapshots s USING(account_id)
WHERE s.snapshot_date='2025-12-31' GROUP BY c.customer_id,c.customer_name ORDER BY deposit_balance DESC LIMIT 20;

-- QUERY: monthly_transaction_growth
WITH m AS (SELECT SUBSTR(transaction_date,1,7) month,COUNT(*) transaction_count,SUM(amount) transaction_value FROM transactions GROUP BY month),
p AS (SELECT *,LAG(transaction_count) OVER(ORDER BY month) previous_count FROM m)
SELECT *,transaction_count*1.0/NULLIF(previous_count,0)-1 monthly_count_growth FROM p ORDER BY month;

-- QUERY: repayment_collection
SELECT SUBSTR(due_date,1,7) month,SUM(principal_due+interest_due) scheduled_due,SUM(principal_paid+interest_paid) amount_collected,
SUM(principal_paid+interest_paid)/SUM(principal_due+interest_due) scheduled_collection_ratio
FROM repayments GROUP BY month ORDER BY month;

-- QUERY: delinquency_buckets
SELECT CASE WHEN days_past_due=0 THEN 'Current' WHEN days_past_due<30 THEN '1-29' WHEN days_past_due<60 THEN '30-59' WHEN days_past_due<90 THEN '60-89' ELSE '90+' END dpd_bucket,
COUNT(*) loan_count,SUM(outstanding) outstanding FROM loan_snapshots WHERE snapshot_date='2025-12-31' GROUP BY dpd_bucket;

-- QUERY: occupation_segments
SELECT c.occupation,COUNT(DISTINCT c.customer_id) customers,SUM(s.balance) deposit_balance
FROM customers c JOIN accounts a USING(customer_id) JOIN account_snapshots s USING(account_id)
WHERE s.snapshot_date='2025-12-31' GROUP BY c.occupation;
