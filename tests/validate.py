"""Independent checks against delivered SQLite data. Run from project root."""
from pathlib import Path
import sqlite3, json, math

ROOT=Path(__file__).resolve().parents[1]
con=sqlite3.connect(ROOT/'outputs/banking.db')
def scalar(sql): return con.execute(sql).fetchone()[0]
def close(a,b): assert math.isclose(a,b,abs_tol=.02), (a,b)
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert scalar('SELECT COUNT(*) FROM transactions')==40000
deposits=scalar("SELECT SUM(balance) FROM account_snapshots WHERE snapshot_date='2025-12-31'")
close(deposits,scalar('SELECT SUM(opening_balance) FROM accounts')+scalar('SELECT SUM(signed_amount) FROM transactions'))
outstanding=scalar("SELECT SUM(outstanding) FROM loan_snapshots WHERE snapshot_date='2025-12-31'")
close(outstanding,scalar('SELECT SUM(original_principal) FROM loans')-scalar('SELECT SUM(principal_paid) FROM repayments'))
assert scalar('SELECT MIN(balance) FROM account_snapshots')>=0
assert scalar('SELECT COUNT(*) FROM account_snapshots')==38400
assert scalar('SELECT COUNT(*) FROM loan_snapshots')==14400
assert scalar('SELECT COUNT(*) FROM loan_snapshots WHERE days_past_due<0 OR days_past_due>365')==0
k=json.loads((ROOT/'outputs/kpis.json').read_text())
close(k['deposit_balance'],deposits);close(k['loan_outstanding'],outstanding)
close(k['operating_profit'],scalar('SELECT SUM(interest_income-interest_expense+fee_income-operating_expense) FROM branch_financials'))
for month, in con.execute('SELECT DISTINCT snapshot_date FROM account_snapshots'):
    close(scalar(f"SELECT SUM(balance) FROM account_snapshots WHERE snapshot_date='{month}'"),scalar('SELECT SUM(opening_balance) FROM accounts')+scalar(f"SELECT SUM(signed_amount) FROM transactions WHERE transaction_date<='{month}'"))
    close(scalar(f"SELECT SUM(outstanding) FROM loan_snapshots WHERE snapshot_date='{month}'"),scalar('SELECT SUM(original_principal) FROM loans')-scalar(f"SELECT SUM(principal_paid) FROM repayments WHERE payment_date<='{month}'"))
con.close()
print('PASS: keys, row counts, all 12 monthly account/loan roll-forwards, KPI totals and financial reconciliation')
